# Makazi Real Estate Platform

## Project Description
A modern real estate platform for property management, rental discovery, and fractional investment in Africa.

## Features
### For Landlords
- Property management dashboard
- Automated rent collection
- Tenant communication tools

### For Tenants
- Verified property discovery
- Secure rent payments
- Direct landlord messaging

### For Investors
- Fractional ownership opportunities
- Investment tracking
- Portfolio management

## Tech Stack
- **Frontend**: React (Web), React Native (Mobile)
- **Backend**: FastAPI (Python)
- **Databases**: MySQL, MongoDB
- **Infrastructure**: Docker, Cloudinary

## Getting Started
### Prerequisites
- Node.js v18+
- pnpm
- Docker

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/2cyprian/Real-estate.git
   cd Real-estate
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Set up environment variables:
   ```bash
   cd backend
   cp .env.example .env
   ```
   Edit `.env` file with your database, JWT secret, and Cloudinary credentials.

4. Start services:
   ```bash
   docker-compose up -d --build
   ```

5. Run development servers:
   ```bash
   pnpm dev
   ```
   This starts:
   - Backend API: http://localhost:8000
   - Web App: http://localhost:3000
   - Mobile App: Metro bundler

### Tech Stack

| Area | Technology |
|------|------------|
| Monorepo | pnpm workspaces + Turborepo |
| Backend | FastAPI, Python 3.10+ |
| Databases | MySQL, MongoDB |
| ORM/ODM | SQLAlchemy, Pymongo |
| Web App | React, Vite, TypeScript |
| Mobile App | React Native, TypeScript |
| Media | Cloudinary |
| Testing | Pytest, Jest & RTL |
| Containerization | Docker & Docker Compose |
| Shared | TypeScript |

### Available Scripts

Run from project root:
- `pnpm dev` - Start all development servers
- `pnpm build` - Build all apps and packages
- `pnpm lint` - Lint all code
- `pnpm test` - Run all tests

App-specific commands:
- `pnpm --filter backend dev` - Start backend only
- `pnpm --filter frontend-web build` - Build web app only

### Project Structure
