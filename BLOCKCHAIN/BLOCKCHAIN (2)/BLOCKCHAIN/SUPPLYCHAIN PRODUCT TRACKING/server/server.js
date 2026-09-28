import cors from 'cors';
import crypto from 'node:crypto';
import dotenv from 'dotenv';
import express from 'express';
import helmet from 'helmet';
import { connectDatabase } from './config/database.js';
import { Product } from './models/Product.js';
import { User } from './models/User.js';

dotenv.config();

const app = express();
const port = Number(process.env.PORT) || 5000;
const response = (success, data, message) => ({ success, data, message });
const publicUser = (user) => ({ id: user.id, name: user.name, email: user.email, role: user.role, organization: user.organization });
const publicProduct = (product) => ({ ...product.toObject(), id: product.productId });

app.use(helmet());
app.use(cors({ origin: process.env.CLIENT_URL || 'http://localhost:5173' }));
app.use(express.json());

app.post('/api/auth/login', async (request, result, next) => {
  try {
    const { email, password } = request.body;
    const user = await User.findOne({ email: email?.toLowerCase(), password });
    if (!user) return result.status(401).json(response(false, null, 'Use manufacturer@pharma.test and demo123 for the demo.'));
    const token = Buffer.from(JSON.stringify({ id: user.id, exp: Date.now() + 86400000 })).toString('base64url');
    return result.json(response(true, { token, user: publicUser(user) }, 'Welcome back.'));
  } catch (error) { return next(error); }
});

app.post('/api/auth/register', async (request, result, next) => {
  try {
    const { name, email, password, organization } = request.body;
    if (!name || !email || !password) return result.status(400).json(response(false, null, 'Name, email, and password are required.'));
    const user = await User.create({ name, email, password, organization: organization || 'Independent partner' });
    return result.status(201).json(response(true, { user: publicUser(user) }, 'Account created.'));
  } catch (error) {
    if (error.code === 11000) return result.status(409).json(response(false, null, 'An account with that email already exists.'));
    return next(error);
  }
});

app.get('/api/auth/me', async (_request, result, next) => {
  try {
    const user = await User.findOne({ email: 'manufacturer@pharma.test' });
    return result.json(response(true, { user: publicUser(user) }));
  } catch (error) { return next(error); }
});

app.get('/api/products', async (_request, result, next) => {
  try { return result.json(response(true, (await Product.find().sort({ updatedAt: -1 })).map(publicProduct))); } catch (error) { return next(error); }
});

app.post('/api/products', async (request, result, next) => {
  try {
    const { name, batch, category, quantity, destination } = request.body;
    if (!name || !batch || !category || !quantity) return result.status(400).json(response(false, null, 'Name, batch, category, and quantity are required.'));
    const timestamp = new Date();
    const product = await Product.create({ productId: `NS-${Math.floor(10000 + Math.random() * 89999)}`, name, batch, category, quantity: Number(quantity), manufacturer: 'Northstar Therapeutics', origin: 'Boston, MA', destination: destination || 'Pending assignment', status: 'Manufactured', events: [{ type: 'Manufactured', location: 'Boston, MA', actor: 'Northstar Therapeutics', timestamp }] });
    return result.status(201).json(response(true, publicProduct(product), 'Product registered in MongoDB.'));
  } catch (error) {
    if (error.code === 11000) return result.status(409).json(response(false, null, 'That batch number already exists.'));
    return next(error);
  }
});

app.post('/api/products/:id/events', async (request, result, next) => {
  try {
    const { type, location } = request.body;
    if (!type || !location) return result.status(400).json(response(false, null, 'Event type and location are required.'));
    const product = await Product.findOne({ productId: request.params.id });
    if (!product) return result.status(404).json(response(false, null, 'Product not found.'));
    product.events.push({ type, location, actor: 'Avery Chen', timestamp: new Date() });
    product.status = type;
    await product.save();
    return result.json(response(true, publicProduct(product), 'Supply-chain event stored in MongoDB.'));
  } catch (error) { return next(error); }
});

app.get('/api/verify/:id', async (request, result, next) => {
  try {
    const product = await Product.findOne({ $or: [{ productId: request.params.id }, { batch: request.params.id }] });
    if (!product) return result.status(404).json(response(false, null, 'No matching product was found.'));
    const plainProduct = product.toObject();
    return result.json(response(true, { ...plainProduct, id: plainProduct.productId, verified: product.status !== 'Quality hold', verificationId: `sha256:${crypto.createHash('sha256').update(product.productId).digest('hex').slice(0, 16)}` }));
  } catch (error) { return next(error); }
});

app.get('/api/health', (_request, result) => result.json(response(true, { status: 'ok' }, 'API is healthy')));
app.use((error, _request, result, _next) => result.status(500).json(response(false, null, error.message || 'Internal server error')));

async function seedDemoData() {
  await User.updateOne({ email: 'manufacturer@pharma.test' }, { $setOnInsert: { name: 'Avery Chen', email: 'manufacturer@pharma.test', password: 'demo123', role: 'Manufacturer', organization: 'Northstar Therapeutics' } }, { upsert: true });
  const count = await Product.countDocuments();
  if (count > 0) return;
  const event = (type, location, actor, timestamp) => ({ type, location, actor, timestamp: new Date(timestamp) });
  await Product.insertMany([
    { productId: 'NS-24081', name: 'Cardiovex 20mg', batch: 'CVX-24-081', category: 'Cardiovascular', quantity: 2400, manufacturer: 'Northstar Therapeutics', origin: 'Boston, MA', destination: 'Walgreens Distribution', status: 'In transit', events: [event('Manufactured', 'Boston, MA', 'Northstar Therapeutics', '2026-08-12'), event('Quality checked', 'Boston, MA', 'QC lab 04', '2026-08-13'), event('Shipped', 'Boston, MA', 'Northstar Therapeutics', '2026-08-20')] },
    { productId: 'NS-24062', name: 'Neurocalm 5mg', batch: 'NCM-24-062', category: 'Neurology', quantity: 860, manufacturer: 'Northstar Therapeutics', origin: 'Boston, MA', destination: 'Cedar Health Pharmacy', status: 'Delivered', events: [event('Manufactured', 'Boston, MA', 'Northstar Therapeutics', '2026-08-04'), event('Delivered', 'Cedar Health Pharmacy', 'Cedar Health Pharmacy', '2026-08-18')] },
    { productId: 'NS-24047', name: 'Immunavax 100mcg', batch: 'IMV-24-047', category: 'Immunology', quantity: 1250, manufacturer: 'Northstar Therapeutics', origin: 'Boston, MA', destination: 'Northstar Cold Storage', status: 'Quality hold', events: [event('Manufactured', 'Boston, MA', 'Northstar Therapeutics', '2026-08-01'), event('Quality hold', 'Northstar Cold Storage', 'QC lab 04', '2026-08-17')] },
  ]);
}

if (process.env.NODE_ENV !== 'test') {
  connectDatabase().then(seedDemoData).then(() => app.listen(port, () => console.log(`API listening on http://localhost:${port}`))).catch((error) => { console.error(`MongoDB connection failed: ${error.message}`); process.exitCode = 1; });
}

export { app };
