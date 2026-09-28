# Architecture

## System boundary

The system has three deployable workspaces: a React client, an Express API, and a Hardhat/Solidity blockchain workspace. MongoDB is the operational database. The local Hardhat node is the development ledger.

## Data ownership

MongoDB stores user accounts, product metadata, shipment records, application-facing event records, and privacy-safe verification logs. The smart contract stores only identifiers, deterministic hashes, wallet ownership, timestamps, event types, recall state, and active status. Documents and images use an IPFS-compatible adapter or local fallback and are referenced by content identifier.

## Verification flow

1. A manufacturer submits validated product data.
2. The backend creates a canonical JSON representation and SHA-256 product hash.
3. MongoDB stores the product record and the backend submits the hash and identifiers to the contract.
4. The contract transaction receipt is stored with the application event.
5. The QR code points to `/verify/:productId`.
6. The public API recalculates the current hash, reads the blockchain record/history, and compares hashes.
7. The public page displays verified, suspicious, or recalled state and the chronological timeline.

This hash comparison demonstrates data-integrity verification. It is not a complete real-world anti-counterfeit system.

## Authentication and authorization

Passwords are bcrypt hashes in MongoDB. JWTs authenticate API requests. Role middleware restricts business operations, while public verification exposes only customer-safe fields. Wallet addresses and blockchain permissions are separated from personal data.

## Main modules

- `client/src/components`: reusable navigation, status badges, timelines, tables, QR controls, and form elements.
- `client/src/pages`: public, authentication, and role-specific screens.
- `server/controllers`: request orchestration and response shaping.
- `server/models`: Mongoose schemas and indexes.
- `server/services`: blockchain, hashing, IPFS, and domain services.
- `server/middleware`: JWT, roles, validation, errors, and security.
- `blockchain/contracts`: Solidity source.
- `blockchain/scripts`: local deployment and setup.
- `blockchain/test`: contract behavior tests.
