import mongoose from 'mongoose';

const eventSchema = new mongoose.Schema({
  type: { type: String, required: true },
  location: { type: String, required: true },
  actor: { type: String, required: true },
  timestamp: { type: Date, default: Date.now },
}, { _id: true });

const productSchema = new mongoose.Schema({
  productId: { type: String, required: true, unique: true, index: true },
  name: { type: String, required: true, trim: true },
  batch: { type: String, required: true, unique: true, trim: true },
  category: { type: String, required: true },
  quantity: { type: Number, required: true, min: 1 },
  manufacturer: { type: String, required: true },
  origin: { type: String, required: true },
  destination: { type: String, required: true },
  status: { type: String, default: 'Manufactured' },
  events: { type: [eventSchema], default: [] },
}, { timestamps: true, versionKey: false });

export const Product = mongoose.models.Product || mongoose.model('Product', productSchema);
