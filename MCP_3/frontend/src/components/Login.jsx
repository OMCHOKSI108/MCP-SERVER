import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { LogoIcon, EyeIcon, EyeOffIcon, AlertIcon } from './Icons';

const Login = ({ setIsLoggedIn, setUser }) => {
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
      const response = await axios.post('http://localhost:5000/api/auth/login', { email, password });
      localStorage.setItem('token', response.data.token);
      setUser(response.data.user);
      setIsLoggedIn(true);
      if (email === 'omchoksi@gmail.com') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
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
          <h1 className="title">Welcome back</h1>
          <p className="subtitle">Sign in to your MCP Server Hub workspace</p>
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

          {/* Row Actions */}
          <div className="row">
            <label className="checkboxLabel">
              <input type="checkbox" className="checkbox" />
              Remember me
            </label>
            <a href="#" className="link">Forgot password?</a>
          </div>

          {/* Button */}
          <button type="submit" className="submitBtn" disabled={isLoading}>
            {isLoading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        {/* Footer */}
        <div className="footer">
          Don’t have an account? <a href="#" className="signupLink">Sign up</a>
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

export default Login;