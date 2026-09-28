# Local Deployment

## Prerequisites

Install Node.js 20+, npm, MongoDB or obtain a MongoDB Atlas database, and MetaMask.

## Environment

Copy the relevant `.env.example` files to ignored `.env` files. Set `MONGODB_URI`, a long random `JWT_SECRET`, `CLIENT_URL`, and the local Hardhat RPC URL. Keep wallet private keys only in local environment files and use throwaway Hardhat accounts.

## Install

From the repository root:

```bash
npm install
```

## Start the local blockchain

```bash
npm run chain
```

Keep this process running. The deployment stage will add the contract deployment command and write the resulting address to the appropriate local environment file.

## Start the application

```bash
npm run dev
```

The Vite client runs on `http://localhost:5173` and the API will run on `http://localhost:5000`.

The API now requires a reachable MongoDB instance before it starts listening. Set `MONGODB_URI` in `server/.env`; demo users and products are inserted into MongoDB on the first successful startup. No application records are kept in process memory.

## MetaMask

Add a custom network using RPC `http://127.0.0.1:8545`, chain ID `31337`, and import only a throwaway private key printed by the local Hardhat node. Never import production keys or share seed phrases.

## Validation checklist

- MongoDB connection succeeds.
- The contract compiles and deployment returns an address.
- Contract tests pass.
- API health endpoint responds.
- A manufacturer can register a product.
- A real transaction hash and block number are saved.
- Distributor and retailer custody transitions are authorized.
- Public verification distinguishes authentic, recalled, and hash-mismatched products.
