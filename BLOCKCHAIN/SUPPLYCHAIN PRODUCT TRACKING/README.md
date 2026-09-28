# Blockchain-Based Pharmaceutical Supply Chain Tracking and Verification System

A production-style academic project for tracking pharmaceutical batches from manufacturer to customer using MongoDB for application data and a Solidity smart contract for tamper-evident supply-chain events.

## First-stage status

This repository currently contains the initial workspace structure, package manifests, environment templates, Hardhat/Vite configuration, and implementation documentation. Feature modules will be implemented incrementally after the scaffold is reviewed.

## Architecture

- `client`: React 19 + Vite + Tailwind CSS user interface, role dashboards, QR scanning/generation, and public verification.
- `server`: Express REST API, JWT authentication, role authorization, Mongoose models, validation, hash generation, and blockchain service integration.
- `blockchain`: Hardhat workspace containing `PharmaSupplyChain.sol`, deployment scripts, and contract tests.
- MongoDB stores operational records and privacy-safe verification logs.
- The blockchain stores product identifiers, deterministic product hashes, ownership, event metadata, recall state, and transaction history.
- IPFS-compatible storage is an optional adapter for document/image references; large or sensitive documents are not stored on-chain.

See [docs/architecture.md](docs/architecture.md), [docs/api.md](docs/api.md), and [docs/deployment.md](docs/deployment.md).

## Prerequisites

- Node.js 20 or newer
- npm 10 or newer
- MongoDB local instance or MongoDB Atlas database
- MetaMask for wallet demonstrations
- Git

## Initial setup

1. Install workspace dependencies:

   ```bash
   npm install
   ```

2. Copy `server/.env.example` to `server/.env` and set a private MongoDB URI, JWT secret, and development blockchain settings.
3. Copy `client/.env.example` to `client/.env`.
4. Copy `blockchain/.env.example` to `blockchain/.env` when deployment variables are needed.
5. Start a local Hardhat node in one terminal:

   ```bash
   npm run chain
   ```

6. Start the API and frontend from the root:

   ```bash
   npm run dev
   ```

The exact contract deployment, API, and demo-data commands will be added with their respective implementation stages.

## Required packages

### Frontend

React, React DOM, Vite, React Router, Axios, Ethers.js, Tailwind CSS, QRCode React, html5-qrcode, Recharts, Lucide React, and Vite/ESLint tooling.

### Backend

Express, Mongoose, dotenv, JSON Web Token, bcryptjs, express-validator, Helmet, CORS, express-rate-limit, Multer, sanitize-html, Axios, and Nano ID. Supertest, Chai, MongoDB Memory Server, Nodemon, and ESLint support development and tests.

### Blockchain

Hardhat, Solidity 0.8.24, Ethers.js, `@nomicfoundation/hardhat-toolbox`, and the Hardhat Ethers plugin.

## Demo accounts

Development-only accounts will be created by the seed stage. Passwords will be documented only after the seed script exists and must never be reused outside the local demo.

## Implementation roadmap

1. **Scaffold review**: confirm workspace scripts, environment names, and local prerequisites.
2. **Smart contract**: implement product registration, ownership transfer, event recording, verification, recall, access control, and emitted events.
3. **Contract tests and deployment**: cover duplicate prevention, authorization, transfer, history, verification, recall, and event emission; add a localhost deployment script.
4. **Backend foundation**: create Express server, configuration, MongoDB connection, consistent errors, security middleware, validation, and health endpoint.
5. **Authentication**: add User model, registration/login, bcrypt hashing, JWT middleware, approval workflow, and role guards.
6. **Product management**: add Product model, deterministic SHA-256 hashing, manufacturer product registration, updates, listing, and recall handling.
7. **Blockchain service**: connect the API to the deployed contract, submit real transactions, and persist returned transaction/block references.
8. **Supply-chain workflows**: add shipment, receive, transfer, sale, history, and role-specific authorization.
9. **Public verification**: calculate and compare hashes, retrieve blockchain history, handle recalled/suspicious/expired products, and log privacy-safe verifications.
10. **Frontend foundation**: add routing, auth state, API client, layout, notifications, loading/error/empty states, and responsive styling.
11. **Role dashboards**: implement admin, manufacturer, distributor, retailer, and customer workflows with tables, charts, QR generation, and timeline views.
12. **Security hardening**: review CORS, rate limits, validation, sanitization, secrets, wallet handling, and information exposure.
13. **Testing and documentation**: add backend API tests, integration checks, architecture/API/deployment docs, and presentation-ready demo data.
14. **End-to-end verification**: install, compile, test, deploy locally, run API/frontend, exercise the full manufacturer-to-customer flow, and fix actual errors.

## Important security note

The MongoDB Atlas URI supplied during setup included a database credential. Rotate that credential in Atlas before using the database, and store the replacement only in an ignored `.env` file. Never place it in source code, README files, screenshots, or blockchain data.
