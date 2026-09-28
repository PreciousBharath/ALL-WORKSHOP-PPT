import React, { useState } from 'react';

// Day 23 - Counter App Project using useState Hook

// Main Counter Component
function CounterApp() {
  return (
    <div className="counter-container">
      <h1>Counter Application</h1>
      <div className="counters-grid">
        <SimpleCounter />
        <CounterWithButtons />
        <MultipleCounters />
        <StepCounter />
      </div>
    </div>
  );
}

// Simple Counter - Basic useState example
function SimpleCounter() {
  const [count, setCount] = useState(0);

  return (
    <div className="counter-card">
      <h2>Simple Counter</h2>
      <div className="display">{count}</div>
      <div className="button-group">
        <button onClick={() => setCount(count - 1)}>-</button>
        <button onClick={() => setCount(count + 1)}>+</button>
        <button onClick={() => setCount(0)}>Reset</button>
      </div>
    </div>
  );
}

// Counter with Custom Buttons
function CounterWithButtons() {
  const [count, setCount] = useState(0);

  const increment = () => setCount(count + 1);
  const decrement = () => setCount(count - 1);
  const reset = () => setCount(0);
  const addFive = () => setCount(count + 5);

  return (
    <div className="counter-card">
      <h2>Counter with Custom Buttons</h2>
      <div className="display">{count}</div>
      <div className="button-group">
        <button onClick={decrement}>-1</button>
        <button onClick={increment}>+1</button>
        <button onClick={addFive}>+5</button>
        <button onClick={reset}>Reset</button>
      </div>
    </div>
  );
}

// Multiple Counters
function MultipleCounters() {
  const [count1, setCount1] = useState(0);
  const [count2, setCount2] = useState(0);

  return (
    <div className="counter-card">
      <h2>Multiple Counters</h2>
      <div className="dual-display">
        <div>
          <p>Counter 1</p>
          <div className="display">{count1}</div>
          <div className="button-group">
            <button onClick={() => setCount1(count1 - 1)}>-</button>
            <button onClick={() => setCount1(count1 + 1)}>+</button>
          </div>
        </div>
        <div>
          <p>Counter 2</p>
          <div className="display">{count2}</div>
          <div className="button-group">
            <button onClick={() => setCount2(count2 - 1)}>-</button>
            <button onClick={() => setCount2(count2 + 1)}>+</button>
          </div>
        </div>
      </div>
      <p className="total">Total: {count1 + count2}</p>
    </div>
  );
}

// Step Counter with Input
function StepCounter() {
  const [count, setCount] = useState(0);
  const [step, setStep] = useState(1);

  const increment = () => setCount(count + step);
  const decrement = () => setCount(count - step);

  return (
    <div className="counter-card">
      <h2>Step Counter</h2>
      <div className="form-group">
        <label>Step Value:</label>
        <input 
          type="number" 
          value={step}
          onChange={(e) => setStep(Number(e.target.value))}
          min="1"
        />
      </div>
      <div className="display">{count}</div>
      <div className="button-group">
        <button onClick={decrement}>- {step}</button>
        <button onClick={increment}>+ {step}</button>
        <button onClick={() => setCount(0)}>Reset</button>
      </div>
    </div>
  );
}

// Counter Display Component (Child Component receives props)
function CountDisplay({ count, onIncrement, onDecrement, onReset }) {
  return (
    <div className="counter-card">
      <h2>Props Counter</h2>
      <div className="display">{count}</div>
      <div className="button-group">
        <button onClick={onDecrement}>-</button>
        <button onClick={onIncrement}>+</button>
        <button onClick={onReset}>Reset</button>
      </div>
    </div>
  );
}

// Parent Component that manages state and passes props
function PropsExample() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <h1>Props Example</h1>
      <CountDisplay 
        count={count}
        onIncrement={() => setCount(count + 1)}
        onDecrement={() => setCount(count - 1)}
        onReset={() => setCount(0)}
      />
    </div>
  );
}

export default CounterApp;

/* CSS Styles */
export const styles = `
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

.counter-container {
  max-width: 1200px;
  margin: 0 auto;
}

.counter-container h1 {
  text-align: center;
  color: white;
  margin-bottom: 40px;
  font-size: 32px;
}

.counters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.counter-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.counter-card h2 {
  color: #333;
  margin-bottom: 20px;
  font-size: 20px;
}

.display {
  font-size: 48px;
  font-weight: bold;
  color: #667eea;
  margin: 30px 0;
  padding: 20px;
  background: #f0f0f0;
  border-radius: 8px;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

button {
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: transform 0.2s, box-shadow 0.2s;
  min-width: 60px;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

button:active {
  transform: translateY(0);
}

.dual-display {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.dual-display > div {
  flex: 1;
  min-width: 120px;
}

.dual-display .display {
  font-size: 36px;
  margin: 15px 0;
}

.dual-display .button-group {
  gap: 8px;
}

.dual-display button {
  min-width: 50px;
  padding: 8px 12px;
  font-size: 14px;
}

.total {
  margin-top: 15px;
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: bold;
}

.form-group input {
  padding: 8px;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  width: 100%;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

@media (max-width: 600px) {
  .counters-grid {
    grid-template-columns: 1fr;
  }

  .counter-container h1 {
    font-size: 24px;
  }

  .display {
    font-size: 36px;
  }

  .dual-display {
    flex-direction: column;
  }
}
`;
