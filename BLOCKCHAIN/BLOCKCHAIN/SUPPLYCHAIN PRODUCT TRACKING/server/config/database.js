import mongoose from 'mongoose';

export async function connectDatabase() {
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/pharma_supply_chain', {
    serverSelectionTimeoutMS: 5000,
    maxPoolSize: 10,
  });
  console.log('MongoDB connected');
}

export async function closeDatabase() {
  await mongoose.disconnect();
}
