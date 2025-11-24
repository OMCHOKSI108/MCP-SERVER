import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { LogoIcon, EyeIcon, EyeOffIcon, AlertIcon } from './Icons';

const Signup = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await axios.post('http://localhost:5000/api/auth/signup', { name, email, password });
      alert('Signup successful! Please log in.');
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.message || 'Signup failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="authCard">

        {/* Header */}
        <div className="header">
          <div className="logoWrapper">
            <LogoIcon />
          </div>
          <h1 className="title">Create account</h1>
          <p className="subtitle">Sign up for your MCP Server Hub workspace</p>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="errorBanner">
            <AlertIcon />
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="form">

          {/* Name */}
          <div className="inputGroup">
            <label htmlFor="name" className="label">Name</label>
            <input
              id="name"
              type="text"
              placeholder="Your full name"
              className={`input ${error ? 'inputError' : ''}`}
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          {/* Email */}
          <div className="inputGroup">
            <label htmlFor="email" className="label">Email</label>
            <input
              id="email"
              type="email"
              placeholder="you@example.com"
              className={`input ${error ? 'inputError' : ''}`}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {/* Password */}
          <div className="inputGroup">
            <label htmlFor="password" className="label">Password</label>
            <div className="inputWrapper">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                placeholder="••••••••"
                className={`input ${error ? 'inputError' : ''}`}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="eyeBtn"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOffIcon /> : <EyeIcon />}
              </button>
            </div>
          </div>

          {/* Button */}
          <button type="submit" className="submitBtn" disabled={isLoading}>
            {isLoading ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        {/* Footer */}
        <div className="footer">
          Already have an account? <a href="#" className="signupLink">Sign in</a>
        </div>

        {/* Trust Context */}
        <p className="trustText">
          MCP Server Hub is a local-first coding assistant. <br />
          Your projects stay on your machine.
        </p>
      </div>
    </div>
  );
};

export default Signup;