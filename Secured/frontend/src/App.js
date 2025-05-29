import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import ResetPassword from "./pages/ResetPassword";
import System from "./pages/System";
import ForgotPassword from "./pages/ForgotPassword";
import Pricing from "./pages/Pricing";
import { Navigate } from "react-router-dom";
import logo from "./images/logo_small.png";
import "./styles/header.css";

function App() {
  return (
    <Router>
      <div>
        <header>
          <img src={logo} alt="Logo" className="logo" />
          <div className="nav-links">
            <div className="right">
              &nbsp;<Link to="/login">Login</Link>
            </div>
            <div className="right">&nbsp;|&nbsp;</div>
            <div className="right">
              <Link to="/register">Register</Link>&nbsp;
            </div>
            <div className="right">&nbsp;|&nbsp;</div>
            <div className="right">
              <Link to="/pricing">Pricing</Link>&nbsp;
            </div>
          </div>
        </header>

        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/system" element={<System />} />
          <Route path="/pricing" element={<Pricing />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
