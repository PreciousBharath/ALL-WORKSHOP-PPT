import { StrictMode, useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

const formatDate = (value) => new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(value));

function App() {
  const [products, setProducts] = useState([]);
  const [selectedId, setSelectedId] = useState('NS-24081');
  const [search, setSearch] = useState('');
  const [activeView, setActiveView] = useState('Overview');
  const [showAdd, setShowAdd] = useState(false);
  const [showEvent, setShowEvent] = useState(false);
  const [notice, setNotice] = useState('');
  const [apiOnline, setApiOnline] = useState(true);
  const [form, setForm] = useState({ name: '', batch: '', category: 'Cardiovascular', quantity: '', destination: '' });
  const [eventForm, setEventForm] = useState({ type: 'Shipped', location: '' });

  const loadProducts = () => fetch(`${API}/products`).then((result) => {
    if (!result.ok) throw new Error('API unavailable');
    return result.json();
  }).then((payload) => { setProducts(payload.data || []); setApiOnline(true); }).catch(() => { setProducts([]); setApiOnline(false); setNotice('API offline. Start MongoDB and restart the server to load live products.'); });
  useEffect(() => { loadProducts(); }, []);

  const filteredProducts = useMemo(() => products.filter((product) => `${product.name} ${product.batch} ${product.id}`.toLowerCase().includes(search.toLowerCase())), [products, search]);
  const selectedProduct = products.find((product) => product.id === selectedId) || filteredProducts[0];
  const counts = useMemo(() => ({ total: products.length, transit: products.filter((product) => product.status === 'In transit').length, hold: products.filter((product) => product.status === 'Quality hold').length }), [products]);

  const submitProduct = async (event) => {
    event.preventDefault();
    const result = await fetch(`${API}/products`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
    const payload = await result.json();
    if (!result.ok) return setNotice(payload.message);
    setProducts((current) => [payload.data, ...current]); setSelectedId(payload.data.id); setShowAdd(false); setForm({ name: '', batch: '', category: 'Cardiovascular', quantity: '', destination: '' }); setNotice('Product registered successfully.');
  };

  const submitEvent = async (event) => {
    event.preventDefault();
    const result = await fetch(`${API}/products/${selectedProduct.id}/events`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(eventForm) });
    const payload = await result.json();
    if (!result.ok) return setNotice(payload.message);
    setProducts((current) => current.map((product) => product.id === payload.data.id ? payload.data : product)); setShowEvent(false); setEventForm({ type: 'Shipped', location: '' }); setNotice('Ledger event recorded.');
  };

  const verifyProduct = async () => {
    const result = await fetch(`${API}/verify/${selectedProduct.id}`); const payload = await result.json();
    setNotice(payload.data?.verified ? `Verified: ${payload.data.verificationId}` : `Review required: ${payload.message || 'product is on hold'}`);
  };

  return (
    <div className="app-shell">
      <aside className="sidebar"><div className="brand"><span className="brand-mark">+</span><span>Northstar<br /><b>Ledger</b></span></div><div className="workspace-label">WORKSPACE</div><nav>{['Overview', 'Products', 'Shipments', 'Verification'].map((item) => <button className={activeView === item ? 'nav-item active' : 'nav-item'} onClick={() => setActiveView(item)} key={item}><span>{item === 'Overview' ? '◈' : item === 'Products' ? '▦' : item === 'Shipments' ? '↗' : '⌁'}</span>{item}</button>)}</nav><div className="sidebar-foot"><div className="user-chip"><span className="avatar">AC</span><span><b>Avery Chen</b><small>Manufacturer</small></span><span className="dots">•••</span></div><div className="connection"><span className={apiOnline ? 'status-dot' : 'status-dot offline'} /> API {apiOnline ? 'online' : 'offline'}</div></div></aside>
      <main className="main-content"><header className="topbar"><div><p className="eyebrow">Northstar Therapeutics / Operations</p><h1>{activeView}</h1></div><div className="top-actions"><button className="icon-button" aria-label="Notifications">♧<i /></button><button className="outline-button" onClick={() => setShowEvent(true)}>Record event <span>+</span></button><button className="primary-button" onClick={() => setShowAdd(true)}>Register product <span>+</span></button></div></header>
        {notice && <div className="notice" role="status">{notice}<button onClick={() => setNotice('')}>×</button></div>}
        <section className="stats-grid"><Stat label="Products tracked" value={counts.total} detail="Across 3 facilities" tone="blue" /><Stat label="In transit" value={counts.transit} detail="1 arriving this week" tone="orange" /><Stat label="Quality holds" value={counts.hold} detail="Requires attention" tone="red" /><Stat label="Verification rate" value="99.8%" detail="+0.4% this month" tone="green" /></section>
        <section className="content-grid"><div className="panel product-panel"><div className="panel-header"><div><p className="eyebrow">Live inventory</p><h2>Tracked products</h2></div><button className="filter-button">Filter <span>⌄</span></button></div><div className="search-box"><span>⌕</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by product, batch or ID" /></div><div className="product-list">{filteredProducts.map((product) => <button className={selectedProduct?.id === product.id ? 'product-row selected' : 'product-row'} key={product.id} onClick={() => setSelectedId(product.id)}><span className="product-icon">{product.name.slice(0, 1)}</span><span className="product-info"><b>{product.name}</b><small>{product.batch} · {product.quantity.toLocaleString()} units</small></span><Status status={product.status} /><span className="row-arrow">›</span></button>)}</div></div>
          {selectedProduct && <div className="panel detail-panel"><div className="detail-heading"><div><p className="eyebrow">Product record</p><h2>{selectedProduct.name}</h2><p className="muted">{selectedProduct.id} · {selectedProduct.category}</p></div><span className={selectedProduct.status === 'Quality hold' ? 'large-status hold' : 'large-status'}>{selectedProduct.status}</span></div><div className="detail-meta"><div><span>Batch number</span><b>{selectedProduct.batch}</b></div><div><span>Quantity</span><b>{selectedProduct.quantity.toLocaleString()} units</b></div><div><span>Destination</span><b>{selectedProduct.destination}</b></div></div><div className="verification-card"><span className="verify-icon">✓</span><div><b>Ledger verified</b><p>Record integrity confirmed · SHA-256</p></div><button onClick={verifyProduct}>Verify now</button></div><div className="timeline-header"><h3>Chain of custody</h3><span>{selectedProduct.events.length} events</span></div><div className="timeline">{[...selectedProduct.events].reverse().map((event, index) => <div className="timeline-item" key={event.id}><span className={index === 0 ? 'timeline-dot current' : 'timeline-dot'} /><div><b>{event.type}</b><p>{event.location} · {event.actor}</p><small>{formatDate(event.timestamp)}</small></div></div>)}</div></div>}
        </section>
      </main>
      {showAdd && <Modal title="Register a product" close={() => setShowAdd(false)}><form onSubmit={submitProduct} className="form-grid"><Field label="Product name" value={form.name} onChange={(value) => setForm({ ...form, name: value })} placeholder="e.g. Cardiovex 20mg" /><Field label="Batch number" value={form.batch} onChange={(value) => setForm({ ...form, batch: value })} placeholder="e.g. CVX-26-001" /><Field label="Category" value={form.category} onChange={(value) => setForm({ ...form, category: value })} select options={['Cardiovascular', 'Neurology', 'Immunology', 'Oncology']} /><Field label="Quantity" value={form.quantity} onChange={(value) => setForm({ ...form, quantity: value })} placeholder="0" type="number" /><Field label="Destination" value={form.destination} onChange={(value) => setForm({ ...form, destination: value })} placeholder="Receiving facility" wide /><button className="primary-button submit-button">Register on ledger <span>→</span></button></form></Modal>}
      {showEvent && selectedProduct && <Modal title={`Update ${selectedProduct.name}`} close={() => setShowEvent(false)}><form onSubmit={submitEvent} className="form-grid"><Field label="Event" value={eventForm.type} onChange={(value) => setEventForm({ ...eventForm, type: value })} select options={['Quality checked', 'Shipped', 'In transit', 'Delivered', 'Quality hold']} /><Field label="Location" value={eventForm.location} onChange={(value) => setEventForm({ ...eventForm, location: value })} placeholder="Current facility or city" wide /><button className="primary-button submit-button">Record event <span>→</span></button></form></Modal>}
    </div>
  );
}

function Stat({ label, value, detail, tone }) { return <div className="stat-card"><span className={`stat-icon ${tone}`}>✦</span><div><span>{label}</span><strong>{value}</strong><small>{detail}</small></div></div>; }
function Status({ status }) { return <span className={`status-pill ${status === 'Quality hold' ? 'hold' : status === 'Delivered' ? 'delivered' : 'transit'}`}><i />{status}</span>; }
function Field({ label, value, onChange, placeholder, type = 'text', select, options, wide }) { return <label className={wide ? 'field wide' : 'field'}>{label}{select ? <select value={value} onChange={(event) => onChange(event.target.value)}>{options.map((option) => <option key={option}>{option}</option>)}</select> : <input type={type} value={value} onChange={(event) => onChange(event.target.value)} placeholder={placeholder} required />}</label>; }
function Modal({ title, close, children }) { return <div className="modal-backdrop" onMouseDown={(event) => event.target === event.currentTarget && close()}><section className="modal"><button className="modal-close" onClick={close}>×</button><p className="eyebrow">Ledger action</p><h2>{title}</h2>{children}</section></div>; }

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
