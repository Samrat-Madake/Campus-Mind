import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
// import { askQuestion,getPendingTickets } from "./api/client";

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
// askQuestion("What is exploratory data analysis?")
//   .then(console.log)
//   .catch(console.error);

// getPendingTickets()
//   .then(console.log)
//   .catch(console.error);