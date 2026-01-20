import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './style/index.css'
import App from './App'

import { ToastContainer } from "react-toastify";


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ToastContainer position="top-right" autoClose={5000} />
    <App />
  </StrictMode>
)
