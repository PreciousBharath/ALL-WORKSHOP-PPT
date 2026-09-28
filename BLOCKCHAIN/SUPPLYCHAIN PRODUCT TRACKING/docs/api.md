# API Documentation

The API base URL is `http://localhost:5000/api`. Protected endpoints use `Authorization: Bearer <jwt>`.

## Initial contract

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| POST | `/auth/register` | Public | Register a user; business roles require approval. |
| POST | `/auth/login` | Public | Authenticate and return a JWT. |
| GET | `/auth/me` | JWT | Return the current user profile. |
| POST | `/products` | Manufacturer | Register a product and blockchain record. |
| GET | `/products` | JWT | List products permitted for the current role. |
| GET | `/products/:id` | JWT/Public-safe | View product details. |
| PUT | `/products/:id` | Owner/Admin | Update permitted product fields and integrity hash. |
| POST | `/products/:id/recall` | Admin | Recall a product on-chain and in MongoDB. |
| POST | `/supply-chain/ship` | Manufacturer/Distributor | Create a shipment and record its event. |
| POST | `/supply-chain/receive` | Distributor/Retailer | Accept a shipment and record receipt. |
| POST | `/supply-chain/transfer` | Distributor/Retailer | Transfer custody to the next role. |
| GET | `/supply-chain/:productId/history` | JWT/Public-safe | Return chronological supply-chain history. |
| GET | `/verify/:productId` | Public | Verify hash, recall state, status, and history. |
| GET | `/users` | Admin | List users. |
| PUT | `/users/:id/approve` | Admin | Approve a business user. |
| GET | `/blockchain/product/:productId` | JWT | Read the blockchain product record. |
| GET | `/blockchain/history/:productId` | JWT | Read blockchain events and receipts. |

All responses use `{ success, data, message }` for success and `{ success: false, message }` for errors. Request schemas, examples, and response payloads will be expanded alongside each implemented route.
