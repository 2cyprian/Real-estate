# Real-estate
 Monorepo
Welcome to the official monorepo for Makazi, a modern real estate platform for property management, rental discovery, and fractional investment in Africa. This repository contains the source code for our entire ecosystem.
backend: The FastAPI API that powers the entire platform.
frontend-web: The React web application for Landlords and Property Managers.
mobile: The React Native mobile app for Tenants and Investors.
shared: A shared TypeScript package for types and interfaces, ensuring consistency across the stack.
✨ Features
For Landlords (Web App): A comprehensive dashboard to manage properties, units, tenants, and financials. Automate rent collection and streamline the entire management process.
For Tenants (Mobile App): A secure and intuitive platform to discover verified properties, pay rent, and communicate with landlords.
For Investors (Both Platforms): An accessible way to invest in fractional ownership of high-growth real estate projects.
🚀 Getting Started
This project uses a monorepo structure managed by pnpm (recommended) and Turborepo.
Prerequisites
Node.js (v18 or later)
pnpm (recommended package manager for workspaces)
Docker and Docker Compose
An account with Cloudinary for media storage.
Installation & Setup
Clone the repository:
code
Bash
git clone https://github.com/your-username/makazi-plus.git
cd makazi-plus
Install dependencies from the root:
code
Bash
pnpm install
Set up Backend Environment Variables:
Navigate to the backend/ directory.
Copy the example environment file:
code
Bash
cp .env.example .env
Open the .env file and fill in your configuration for the databases, JWT secret, and Cloudinary credentials.
Start all services:
From the root of the monorepo, run Docker Compose. This will start the FastAPI backend, MySQL database, and MongoDB.
code
Bash
docker-compose up -d --build
The -d flag runs the containers in detached mode.
Run Development Servers:
Turborepo allows you to run all development servers with a single command from the root.
code
Bash
pnpm dev
This will concurrently start:
Backend API: http://localhost:8000 (FastAPI with hot-reloading)
Web App: http://localhost:3000 (React)
Mobile App: Metro bundler for React Native
🛠️ Tech Stack
Area	Technology
Monorepo	pnpm workspaces + Turborepo
Backend	FastAPI, Python 3.10+
Databases	MySQL (Relational), MongoDB (NoSQL)
ORM/ODM	SQLAlchemy (MySQL), Pymongo (MongoDB)
Web App	React, Vite, TypeScript
Mobile App	React Native, TypeScript
Media	Cloudinary for image & video storage
Testing	Pytest (Backend), Jest & RTL (Frontend)
Containerization	Docker & Docker Compose
Shared	TypeScript for shared types and interfaces
⚙️ Available Scripts
All scripts should be run from the root of the monorepo.
pnpm dev: Starts all development servers concurrently.
pnpm build: Builds all apps and packages.
pnpm lint: Lints all apps and packages.
pnpm test: Runs all tests across the entire monorepo.
You can also run scripts for a specific app:
pnpm --filter backend dev: Starts only the backend dev server.
pnpm --filter frontend-web build: Builds only the web app.
📦 Project Structure
code
Code
myapp/
│
├── backend/               # FastAPI backend
│   ├── app/
│   ├── tests/
│   └── .env               # (ignored by git)
│
├── frontend-web/          # React web app
│   └── src/
│
├── mobile/                # React Native app
│   └── src/
│
├── shared/                # Shared logic & types
│   └── models/            # Shared TypeScript interfaces
│
├── package.json           # Root pnpm/Turborepo config
├── turbo.json
└── docker-compose.yml
FastAPI Backend Details
API URL: http://localhost:8000
Interactive API Docs (Swagger): http://localhost:8000/docs
Alternative API Docs (ReDoc): http://localhost:8000/redoc
Running Backend Migrations
To apply database schema changes, you need to run Alembic inside the running backend container.
Find the container ID: docker ps
Run the migration command:
code
Bash
docker exec <backend_container_id> alembic upgrade head
🤝 Contributing
Contributions are welcome! Please follow these steps:
Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Make your changes.
Commit your changes (git commit -m 'feat: Add some amazing feature').
Push to the branch (git push origin feature/your-feature-name).
Open a Pull 