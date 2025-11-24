import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import AuthLayout from './AuthLayout';
import { authApi } from '../api';
import { User } from '../types';

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const Input = styled.input`
  padding: 12px 16px;
  background: #111827;
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 8px;
  color: #F9FAFB;
  font-size: 14px;
  transition: all 0.2s;

  &:focus {
    outline: none;
    border-color: #6366F1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  }

  &::placeholder {
    color: #9CA3AF;
  }
`;

const CheckboxContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
`;

const Checkbox = styled.input`
  width: 16px;
  height: 16px;
`;

const Label = styled.label`
  font-size: 14px;
  color: #9CA3AF;
`;

const Button = styled.button`
  padding: 12px 16px;
  background: #6366F1;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
  height: 44px;

  &:hover {
    background: #5855EB;
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  }

  &:active {
    transform: scale(0.98);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const LinkText = styled.p`
  text-align: center;
  font-size: 14px;
  color: #9CA3AF;
  margin-top: 24px;

  a {
    color: #6366F1;
    text-decoration: none;
    position: relative;

    &::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 0;
      width: 0;
      height: 1px;
      background: #6366F1;
      transition: width 0.2s;
    }

    &:hover::after {
      width: 100%;
    }
  }
`;

const ErrorBanner = styled.div`
  background: #DC2626;
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 16px;
  animation: slideDown 0.3s ease-out;

  @keyframes slideDown {
    from {
      transform: translateY(-10px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
`;

interface LoginPageProps {
  setIsLoggedIn: (loggedIn: boolean) => void;
  setUser: (user: User) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ setIsLoggedIn, setUser }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authApi.login(email, password);
      const { token, user } = response.data;
      localStorage.setItem('token', token);
      setUser(user);
      setIsLoggedIn(true);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Welcome back" subtitle="Sign in to your SensCoder account">
      {error && <ErrorBanner>{error}</ErrorBanner>}
      <Form onSubmit={handleSubmit}>
        <Input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <CheckboxContainer>
          <Checkbox
            type="checkbox"
            id="remember"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
          />
          <Label htmlFor="remember">Remember me</Label>
        </CheckboxContainer>
        <Button type="submit" disabled={loading}>
          {loading ? 'Signing in...' : 'Sign in'}
        </Button>
      </Form>
      <LinkText>
        Don't have an account? <Link to="/signup">Sign up</Link>
      </LinkText>
    </AuthLayout>
  );
};

export default LoginPage;