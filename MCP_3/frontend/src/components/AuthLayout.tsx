import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #050816 0%, #0B0F19 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(79, 70, 229, 0.1) 0%, transparent 50%);
    animation: backgroundShift 25s ease-in-out infinite;
  }

  @keyframes backgroundShift {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(10px, -10px) scale(1.02); }
    66% { transform: translate(-10px, 10px) scale(0.98); }
  }
`;

const Card = styled.div`
  background: #0F172A;
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  position: relative;
  z-index: 1;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);

  animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  transform: translateY(0);
  opacity: 1;

  @keyframes slideIn {
    from {
      transform: translateY(16px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
`;

const Logo = styled.div`
  text-align: center;
  margin-bottom: 32px;
  color: #6366F1;
  font-size: 24px;
  font-weight: 600;
`;

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle: string;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children, title, subtitle }) => {
  return (
    <Container>
      <Card>
        <Logo>SensCoder</Logo>
        <h1 style={{ fontSize: '24px', fontWeight: '600', color: '#F9FAFB', marginBottom: '8px', textAlign: 'center' }}>
          {title}
        </h1>
        <p style={{ fontSize: '14px', color: '#9CA3AF', marginBottom: '32px', textAlign: 'center' }}>
          {subtitle}
        </p>
        {children}
      </Card>
    </Container>
  );
};

export default AuthLayout;