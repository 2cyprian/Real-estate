"""create_properties_table

Revision ID: create_properties_table
Revises: e26fa302650c
Create Date: 2025-01-07 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'create_properties_table'
down_revision: Union[str, Sequence[str], None] = 'e26fa302650c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    # Create enums manually if they don't exist
    bind.execute(text("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'property_type_enum') THEN
                CREATE TYPE property_type_enum AS ENUM ('house', 'apartment', 'land', 'commercial');
            END IF;
        END$$;
    """))

    bind.execute(text("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'property_status_enum') THEN
                CREATE TYPE property_status_enum AS ENUM ('available', 'rented', 'sold');
            END IF;
        END$$;
    """))

    # Use existing PostgreSQL ENUM types directly
    property_type_enum = ENUM('house', 'apartment', 'land', 'commercial', name='property_type_enum', create_type=False)
    property_status_enum = ENUM('available', 'rented', 'sold', name='property_status_enum', create_type=False)

    # Create properties table
    op.create_table(
        'properties',
        sa.Column('id', sa.BIGINT(), primary_key=True, autoincrement=True),
        sa.Column('user_id', UUID(as_uuid=True),
                  sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('property_type', property_type_enum, nullable=False),
        sa.Column('price', sa.DECIMAL(precision=15, scale=2), nullable=False),
        sa.Column('status', property_status_enum, nullable=False, server_default='available'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),
        sa.Column('mongo_document_id', sa.String(length=24), unique=True, nullable=True),
    )

    # Add indexes
    op.create_index('ix_properties_user_id', 'properties', ['user_id'])
    op.create_index('ix_properties_property_type', 'properties', ['property_type'])
    op.create_index('ix_properties_price', 'properties', ['price'])
    op.create_index('ix_properties_status', 'properties', ['status'])

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_properties_status', table_name='properties')
    op.drop_index('ix_properties_price', table_name='properties')
    op.drop_index('ix_properties_property_type', table_name='properties')
    op.drop_index('ix_properties_user_id', table_name='properties')
    op.drop_table('properties')
    
    # Drop enums if they exist
    bind = op.get_bind()
    bind.execute(text("DROP TYPE IF EXISTS property_type_enum"))
    bind.execute(text("DROP TYPE IF EXISTS property_status_enum"))
