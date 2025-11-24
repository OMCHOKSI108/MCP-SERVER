import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { User } from '../types';

const Container = styled.div`
  min-height: 100vh;
  background: #050816;
  color: #F9FAFB;
`;

const Navbar = styled.nav`
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.3);
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
`;

const Logo = styled(Link)`
  color: #6366F1;
  font-size: 18px;
  font-weight: 600;
  text-decoration: none;
`;

const UserMenu = styled.div`
  position: relative;
`;

const UserAvatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #6366F1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.15s;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  }
`;

const Dropdown = styled.div<{ show: boolean }>`
  position: absolute;
  top: 50px;
  right: 0;
  background: #0F172A;
  border: 1px solid rgba(148, 163, 184, 0.3);
  border-radius: 8px;
  padding: 8px 0;
  min-width: 150px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  opacity: ${props => props.show ? 1 : 0};
  visibility: ${props => props.show ? 'visible' : 'hidden'};
  transform: translateY(${props => props.show ? 0 : -10}px);
  transition: all 0.15s;
`;

const DropdownItem = styled(Link)`
  display: block;
  padding: 8px 16px;
  color: #F9FAFB;
  text-decoration: none;
  font-size: 14px;
  transition: background 0.15s;

  &:hover {
    background: rgba(99, 102, 241, 0.1);
  }
`;

const LogoutButton = styled.button`
  display: block;
  width: 100%;
  padding: 8px 16px;
  background: none;
  border: none;
  color: #F9FAFB;
  font-size: 14px;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;

  &:hover {
    background: rgba(99, 102, 241, 0.1);
  }
`;

const Main = styled.main`
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
`;

interface AppShellProps {
  user: User | null;
  onLogout: () => void;
  children: React.ReactNode;
}

const AppShell: React.FC<AppShellProps> = ({ user, onLogout, children }) => {
  const [showDropdown, setShowDropdown] = useState(false);

  const handleLogout = () => {
    onLogout();
    setShowDropdown(false);
  };

  return (
    <Container>
      <Navbar>
        <Logo to="/dashboard">SensCoder</Logo>
        {user && (
          <UserMenu>
            <UserAvatar onClick={() => setShowDropdown(!showDropdown)}>
              {user.name.charAt(0).toUpperCase()}
            </UserAvatar>
            <Dropdown show={showDropdown}>
              <DropdownItem to="/profile" onClick={() => setShowDropdown(false)}>
                Profile
              </DropdownItem>
              <DropdownItem to="/settings" onClick={() => setShowDropdown(false)}>
                Settings
              </DropdownItem>
              <DropdownItem to="/integrations" onClick={() => setShowDropdown(false)}>
                Integrations
              </DropdownItem>
              {user?.role === 'admin' && (
                <DropdownItem to="/admin" onClick={() => setShowDropdown(false)}>
                  Admin Panel
                </DropdownItem>
              )}
              <LogoutButton onClick={handleLogout}>Logout</LogoutButton>
            </Dropdown>
          </UserMenu>
        )}
      </Navbar>
      <Main>
        {children}
      </Main>
    </Container>
  );
};

export default AppShell;