# Day 21 - React Setup Instructions

## What is React?
React is a JavaScript library for building user interfaces with reusable components and efficient rendering.

## Installation Methods

### Method 1: Create React App (Recommended for beginners)
```bash
npx create-react-app my-app
cd my-app
npm start
```

### Method 2: Vite (Modern and Fast)
```bash
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev
```

## Project Structure (Create React App)
```
my-app/
├── src/
│   ├── App.js (Main component)
│   ├── App.css
│   ├── index.js (Entry point)
│   └── index.css
├── public/
│   └── index.html
├── package.json
└── .gitignore
```

## Key Concepts

### 1. Components
React applications are built using components. A component is a reusable piece of UI.

```javascript
// Functional Component (Modern)
function Welcome() {
  return <h1>Hello, React!</h1>;
}

export default Welcome;
```

### 2. JSX
JSX is a syntax extension to JavaScript that looks similar to HTML.

```javascript
const name = "John";
const element = <h1>Hello, {name}!</h1>;
```

### 3. Props
Props are used to pass data to components.

```javascript
function Greeting(props) {
  return <h1>Hello, {props.name}!</h1>;
}
```

### 4. Hooks
Hooks are functions that let you use state and other React features.

```javascript
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

## Common Commands

| Command | Description |
|---------|-------------|
| `npm start` | Start development server |
| `npm run build` | Build for production |
| `npm test` | Run tests |
| `npm eject` | Expose configuration (irreversible!) |

## Tips for Learning
1. Start with functional components (class components are deprecated)
2. Learn hooks: useState, useEffect, useContext
3. Practice component composition
4. Use React Developer Tools browser extension
5. Read the official React documentation

## Useful Resources
- [React Official Docs](https://react.dev)
- [Create React App Docs](https://create-react-app.dev)
- [Vite Documentation](https://vitejs.dev)

## Next Steps
After this setup, you'll learn:
- Components and JSX (Day 22)
- Props and State (Day 23)
- useEffect and API calls (Day 24)
- Forms and validation (Day 25)
- React Router (Day 26)
- API Integration (Day 27)
- Context API (Day 28)
- Advanced Hooks (Day 29)
- Capstone Project (Day 30)
