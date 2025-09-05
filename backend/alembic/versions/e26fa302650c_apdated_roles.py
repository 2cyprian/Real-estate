"""apdated roles

Revision ID: e26fa302650c
Revises: 02b3d307db60
Create Date: 2025-09-04 09:29:19.684753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e26fa302650c'
down_revision: Union[str, Sequence[str], None] = '02b3d307db60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Create enum type
    user_role_enum = sa.Enum(
        'owner', 'agent', 'buyer', 'tenant', 'admin',
        name='user_role_enum'
    )
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # 2. Add new column with default
    op.add_column(
        'users',
        sa.Column(
            'role',
            user_role_enum,
            nullable=False,
            server_default='tenant'  # ensures existing rows get a value
        )
    )

    # 3. Update phone_number type
    op.alter_column(
        'users',
        'phone_number',
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=True
    )

    # 4. Drop old column
    op.drop_column('users', 'is_agent')


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Re-add dropped column
    op.add_column(
        'users',
        sa.Column('is_agent', sa.BOOLEAN(), autoincrement=False, nullable=True)
    )

    # 2. Revert phone_number type
    op.alter_column(
        'users',
        'phone_number',
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=True
    )

    # 3. Drop role column
    op.drop_column('users', 'role')

    # 4. Drop enum type
    user_role_enum = sa.Enum(
        'owner', 'agent', 'buyer', 'tenant', 'admin',
        name='user_role_enum'
    )
    user_role_enum.drop(op.get_bind(), checkfirst=True)
