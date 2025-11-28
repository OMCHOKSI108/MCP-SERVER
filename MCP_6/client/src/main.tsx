import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// Minimal basic styles
const style = document.createElement('style');
style.innerHTML = `
  body { margin: 0; font-family: sans-serif; overflow: hidden; }
  #root { width: 100vw; height: 100vh; display: flex; flex-direction: column; }
`;
document.head.appendChild(style);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)