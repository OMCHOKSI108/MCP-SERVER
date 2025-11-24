import React, { useState, useEffect } from 'react';
import styled, { keyframes, css } from 'styled-components';
import {
  FaUsers,
  FaComments,
  FaRobot,
  FaKey,
  FaCog,
  FaFileAlt,
  FaEdit,
  FaTrash,
  FaBan,
  FaCheckCircle,
  FaTimesCircle,
  FaExclamationTriangle,
  FaPlus,
  FaEye,
  FaEyeSlash,
  FaRedo,
  FaSave,
  FaTimes,
  FaChevronLeft,
  FaChevronRight,
  FaSearch,
  FaUserShield,
  FaChartBar,
  FaDatabase,
  FaServer,
  FaClock
} from 'react-icons/fa';
import { User } from '../types';
import { adminApi } from '../api';

// Animations
const slideIn = keyframes`
  from { transform: translateX(-20px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const glow = keyframes`
  0% { box-shadow: 0 0 5px rgba(0, 212, 255, 0.3); }
  50% { box-shadow: 0 0 20px rgba(0, 212, 255, 0.6); }
  100% { box-shadow: 0 0 5px rgba(0, 212, 255, 0.3); }
`;

const confetti = keyframes`
  0% { transform: rotate(0deg) scale(0); opacity: 1; }
  50% { transform: rotate(180deg) scale(1); opacity: 0.8; }
  100% { transform: rotate(360deg) scale(0); opacity: 0; }
`;

// Layout Components
const AdminContainer = styled.div`
  display: flex;
  min-height: 100vh;
  background: #f8f9fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
`;

const Sidebar = styled.div`
  width: 250px;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  padding: 20px 15px;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  box-shadow: 2px 0 4px rgba(0,0,0,0.05);
  z-index: 10;
`;

const SidebarTitle = styled.h2`
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 24px;
  text-align: center;
`;

const SidebarNav = styled.nav`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

const SidebarLink = styled.button<{ $active: boolean }>`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: none;
  border-radius: 6px;
  background: ${props => props.$active ? '#e5e7eb' : 'transparent'};
  color: ${props => props.$active ? '#1f2937' : '#6b7280'};
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
  width: 100%;

  &:hover {
    background: #f3f4f6;
    color: #1f2937;
  }

  svg {
    width: 16px;
    height: 16px;
  }
`;

const MainContent = styled.div`
  flex: 1;
  margin-left: 280px;
  padding: 24px;
`;

const ContentHeader = styled.div`
  margin-bottom: 24px;
`;

const PageTitle = styled.h1`
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
`;

const PageSubtitle = styled.p`
  font-size: 14px;
  color: #6b7280;
`;

// Stats Components
const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
`;

const StatCard = styled.div`
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);

  &:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }
`;

const StatIcon = styled.div`
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  color: white;
`;

const StatNumber = styled.div`
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
`;

const StatLabel = styled.div`
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
`;

// Table Components
const TableContainer = styled.div`
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const TableHeader = styled.thead`
  background: #f9fafb;
`;

const Th = styled.th`
  text-align: left;
  padding: 12px 16px;
  color: #374151;
  font-weight: 600;
  font-size: 12px;
  border-bottom: 1px solid #e5e7eb;
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const Td = styled.td`
  padding: 12px 16px;
  color: #374151;
  border-bottom: 1px solid #f3f4f6;
  font-size: 14px;
`;

const TableRow = styled.tr`
  transition: all 0.2s ease;

  &:hover {
    background: #f9fafb;
  }
`;

// Form Components
const FormCard = styled.div`
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
`;

const FormTitle = styled.h3`
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 16px;
`;

const FormGroup = styled.div`
  margin-bottom: 16px;
`;

const Label = styled.label`
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
  margin-bottom: 6px;
`;

const Input = styled.input`
  width: 100%;
  padding: 8px 12px;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 14px;
  transition: all 0.2s;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 8px 12px;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 14px;
  transition: all 0.2s;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 8px 12px;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 14px;
  min-height: 80px;
  resize: vertical;
  transition: all 0.2s;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  }
`;

// Button Components
const ButtonGroup = styled.div`
  display: flex;
  gap: 8px;
  margin-top: 16px;
`;

const Button = styled.button<{ variant?: 'primary' | 'danger' | 'success' | 'warning' }>`
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;

  ${props => {
    switch (props.variant) {
      case 'danger':
        return css`
          background: #dc2626;
          color: white;
          &:hover { background: #b91c1c; }
        `;
      case 'success':
        return css`
          background: #16a34a;
          color: white;
          &:hover { background: #15803d; }
        `;
      case 'warning':
        return css`
          background: #d97706;
          color: white;
          &:hover { background: #b45309; }
        `;
      default:
        return css`
          background: #3b82f6;
          color: white;
          &:hover { background: #2563eb; }
        `;
    }
  }}

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Action Buttons Container
const ActionButtons = styled.div`
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  align-items: center;
`;

// Modal Components
const Modal = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: ${fadeIn} 0.3s ease-out;
`;

const ModalContent = styled.div`
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 24px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
`;

const ModalHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
`;

const ModalTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: #6b7280;
  font-size: 24px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;

  &:hover {
    background: #f3f4f6;
    color: #374151;
  }
`;

// Toast Components
const ToastContainer = styled.div`
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 2000;
`;

const Toast = styled.div<{ type: 'success' | 'error' | 'warning' }>`
  background: ${props => {
    switch (props.type) {
      case 'success': return '#dcfce7';
      case 'error': return '#fef2f2';
      case 'warning': return '#fef3c7';
      default: return '#eff6ff';
    }
  }};
  color: ${props => {
    switch (props.type) {
      case 'success': return '#166534';
      case 'error': return '#991b1b';
      case 'warning': return '#92400e';
      default: return '#1e40af';
    }
  }};
  padding: 12px 16px;
  border-radius: 6px;
  margin-bottom: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  border: 1px solid ${props => {
    switch (props.type) {
      case 'success': return '#bbf7d0';
      case 'error': return '#fecaca';
      case 'warning': return '#fde68a';
      default: return '#bfdbfe';
    }
  }};
`;

const ConfettiContainer = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  overflow: hidden;
`;

const Confetti = styled.div`
  position: absolute;
  width: 10px;
  height: 10px;
  background: ${props => ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'][Math.floor(Math.random() * 5)]};
  animation: ${confetti} 1s ease-out forwards;
`;

// Status Components
const StatusBadge = styled.span<{ status: 'active' | 'blocked' | 'admin' | 'banned' }>`
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;

  ${props => {
    switch (props.status) {
      case 'admin':
        return 'background: #dbeafe; color: #1e40af;';
      case 'blocked':
      case 'banned':
        return 'background: #fef2f2; color: #991b1b;';
      default:
        return 'background: #dcfce7; color: #166534;';
    }
  }}
`;

// Pagination
const Pagination = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 24px;
  gap: 8px;
`;

const PageButton = styled.button<{ active?: boolean }>`
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: ${props => props.active ? '#3b82f6' : '#ffffff'};
  color: ${props => props.active ? '#ffffff' : '#374151'};
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: ${props => props.active ? '#2563eb' : '#f9fafb'};
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Types
interface UserWithAdmin extends Omit<User, 'role'> {
  role?: string;
  isBlocked?: boolean;
  isBanned?: boolean;
  dailyMessages?: number;
  lastActivity?: string;
  createdAt?: string;
}

interface Stats {
  users: number;
  messagesToday: number;
  geminiCalls: number;
  healthyKeys: number;
}

interface GeminiKey {
  _id: string;
  name: string;
  key: string;
  dailyCalls: number;
  isActive: boolean;
  lastUsedAt?: string;
  createdAt: string;
}

interface LogStats {
  totalLogs: number;
  todayLogs: number;
  errorLogs: number;
  userActions: number;
  adminActions: number;
}

interface ActivityLog {
  _id: string;
  userId?: {
    _id: string;
    name: string;
    email: string;
  };
  action: string;
  message: string;
  level: 'info' | 'warning' | 'error' | 'critical';
  details: any;
  ipAddress?: string;
  createdAt: string;
}

type AdminTab = 'overview' | 'users' | 'keys' | 'settings' | 'logs' | 'master';

const Admin: React.FC = () => {
  const [activeTab, setActiveTab] = useState<AdminTab>('overview');
  const [users, setUsers] = useState<UserWithAdmin[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [geminiKeys, setGeminiKeys] = useState<GeminiKey[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<UserWithAdmin | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showKeyModal, setShowKeyModal] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  // Form states
  const [newKeyName, setNewKeyName] = useState('');
  const [newKeyValue, setNewKeyValue] = useState('');
  const [dailyLimit, setDailyLimit] = useState('');
  const [maintenanceMode, setMaintenanceMode] = useState(false);
  const [bannerMessage, setBannerMessage] = useState('');
  const [logs, setLogs] = useState<ActivityLog[]>([]);
  const [logStats, setLogStats] = useState<LogStats | null>(null);
  const [currentLogPage, setCurrentLogPage] = useState(1);
  const [totalLogPages, setTotalLogPages] = useState(1);
  const [logFilters, setLogFilters] = useState({
    action: '',
    level: '',
    startDate: '',
    endDate: ''
  });

  useEffect(() => {
    loadData();
  }, [activeTab, currentPage, searchTerm, currentLogPage, logFilters]);

  const loadData = async () => {
    try {
      setLoading(true);

      if (activeTab === 'overview' || activeTab === 'users' || activeTab === 'master') {
        const [usersResponse, statsResponse] = await Promise.all([
          adminApi.getUsers(currentPage, 10, searchTerm),
          adminApi.getStats()
        ]);

        setUsers(usersResponse.data.users);
        setTotalPages(usersResponse.data.pagination.pages);
        setStats(statsResponse.data);
      }

      if (activeTab === 'keys' || activeTab === 'master') {
        const keysResponse = await adminApi.getGeminiKeys();
        setGeminiKeys(keysResponse.data);
      }

      if (activeTab === 'settings' || activeTab === 'master') {
        const settingsResponse = await adminApi.getSettings();
        const settings = settingsResponse.data;
        setDailyLimit(settings.dailyLimit?.toString() || '');
        setMaintenanceMode(settings.maintenanceMode || false);
        setBannerMessage(settings.banner || '');
      }

      if (activeTab === 'logs') {
        const [logsResponse, logStatsResponse] = await Promise.all([
          adminApi.getLogs(currentLogPage, 50, logFilters),
          adminApi.getLogStats()
        ]);

        setLogs(logsResponse.data.logs);
        setTotalLogPages(logsResponse.data.pagination.pages);
        setLogStats(logStatsResponse.data);
      }
    } catch (error) {
      console.error('Failed to load admin data', error);
      showToast('error', 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const showToast = (type: 'success' | 'error' | 'warning', message: string, showConfetti = false) => {
    const id = Date.now().toString();
    setToasts(prev => [...prev, { id, type, message, showConfetti }]);

    setTimeout(() => {
      setToasts(prev => prev.filter(toast => toast.id !== id));
    }, 5000);
  };

  const handleUserAction = async (userId: string, action: string, data?: any) => {
    if (!userId || userId === 'undefined') {
      showToast('error', 'Invalid user ID');
      return;
    }

    try {
      let response;
      switch (action) {
        case 'update':
          response = await adminApi.updateUser(userId, data);
          break;
        case 'delete':
          response = await adminApi.deleteUser(userId);
          break;
        default:
          return;
      }

      showToast('success', `User ${action}d successfully`, action === 'delete');
      await loadData();
    } catch (error) {
      console.error(`Failed to ${action} user`, error);
      showToast('error', `Failed to ${action} user`);
    }
  };

  const handleKeyAction = async (action: string, keyId?: string, data?: any) => {
    try {
      let response;
      switch (action) {
        case 'add':
          response = await adminApi.addGeminiKey(data);
          break;
        case 'update':
          response = await adminApi.updateGeminiKey(keyId!, data);
          break;
        case 'delete':
          response = await adminApi.deleteGeminiKey(keyId!);
          break;
        default:
          return;
      }

      showToast('success', `Key ${action}d successfully`);
      setShowKeyModal(false);
      setNewKeyName('');
      setNewKeyValue('');
      await loadData();
    } catch (error) {
      console.error(`Failed to ${action} key`, error);
      showToast('error', `Failed to ${action} key`);
    }
  };

  const handleSettingsUpdate = async () => {
    try {
      await adminApi.updateSettings({
        dailyLimit: parseInt(dailyLimit),
        maintenanceMode,
        banner: bannerMessage
      });
      showToast('success', 'Settings updated successfully');
    } catch (error) {
      console.error('Failed to update settings', error);
      showToast('error', 'Failed to update settings');
    }
  };

  const handleClearOldLogs = async () => {
    try {
      const response = await adminApi.clearOldLogs(30);
      showToast('success', response.data.message);
      await loadData(); // Refresh logs
    } catch (error) {
      console.error('Failed to clear old logs', error);
      showToast('error', 'Failed to clear old logs');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const renderOverview = () => (
    <>
      <StatsGrid>
        <StatCard>
          <StatIcon><FaUsers size={24} /></StatIcon>
          <StatNumber>{stats?.users || 0}</StatNumber>
          <StatLabel>Total Users</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon><FaComments size={24} /></StatIcon>
          <StatNumber>{stats?.messagesToday || 0}</StatNumber>
          <StatLabel>Messages Today</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon><FaRobot size={24} /></StatIcon>
          <StatNumber>{stats?.geminiCalls || 0}</StatNumber>
          <StatLabel>Gemini Calls Today</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon><FaKey size={24} /></StatIcon>
          <StatNumber>{stats?.healthyKeys || 0}</StatNumber>
          <StatLabel>Healthy Keys</StatLabel>
        </StatCard>
      </StatsGrid>

      <FormCard>
        <FormTitle>Recent Activity</FormTitle>
        <p style={{ color: '#9CA3AF' }}>Activity logs will be displayed here...</p>
      </FormCard>
    </>
  );

  const renderUsers = () => (
    <>
      <div style={{ marginBottom: '24px' }}>
        <Input
          type="text"
          placeholder="Search users..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ maxWidth: '300px' }}
        />
      </div>

      <TableContainer>
        <Table>
          <TableHeader>
            <tr>
              <Th>Name</Th>
              <Th>Email</Th>
              <Th>Role</Th>
              <Th>Status</Th>
              <Th>Daily Messages</Th>
              <Th>Last Activity</Th>
              <Th>Actions</Th>
            </tr>
          </TableHeader>
          <tbody>
            {users.map(user => (
              <TableRow key={user._id}>
                <Td>{user.name}</Td>
                <Td>{user.email}</Td>
                <Td>
                  <StatusBadge status={user.role === 'admin' ? 'admin' : 'active'}>
                    {user.role || 'user'}
                  </StatusBadge>
                </Td>
                <Td>
                  <StatusBadge status={user.isBanned ? 'banned' : user.isBlocked ? 'blocked' : 'active'}>
                    {user.isBanned ? 'Banned' : user.isBlocked ? 'Blocked' : 'Active'}
                  </StatusBadge>
                </Td>
                <Td>{user.dailyMessages || 0}</Td>
                <Td>{user.lastActivity ? formatDate(user.lastActivity) : 'Never'}</Td>
                <Td>
                  <ActionButtons>
                    <Button
                      variant="primary"
                      onClick={() => {
                        setSelectedUser(user);
                        setShowEditModal(true);
                      }}
                      title="Edit User"
                    >
                      <FaEdit size={14} />
                    </Button>
                    <Button
                      variant={user.isBanned ? "success" : "danger"}
                      onClick={() => handleUserAction(user._id, 'update', { isBanned: !user.isBanned })}
                      title={user.isBanned ? 'Unban User' : 'Ban User'}
                    >
                      {user.isBanned ? <FaCheckCircle size={14} /> : <FaBan size={14} />}
                    </Button>
                    <Button
                      variant="warning"
                      onClick={() => handleUserAction(user._id, 'update', { resetCounter: true })}
                      title="Reset Message Counter"
                    >
                      <FaRedo size={14} />
                    </Button>
                    {user.role !== 'admin' && (
                      <Button
                        variant="danger"
                        onClick={() => {
                          if (confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
                            handleUserAction(user._id, 'delete');
                          }
                        }}
                        title="Delete User"
                      >
                        <FaTrash size={14} />
                      </Button>
                    )}
                  </ActionButtons>
                </Td>
              </TableRow>
            ))}
          </tbody>
        </Table>
      </TableContainer>

      {totalPages > 1 && (
        <Pagination>
          <PageButton
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(currentPage - 1)}
          >
            Previous
          </PageButton>
          {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
            <PageButton
              key={page}
              active={page === currentPage}
              onClick={() => setCurrentPage(page)}
            >
              {page}
            </PageButton>
          ))}
          <PageButton
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Next
          </PageButton>
        </Pagination>
      )}
    </>
  );

  const renderKeys = () => (
    <>
      <Button
        variant="primary"
        onClick={() => setShowKeyModal(true)}
        style={{ marginBottom: '24px' }}
      >
        Add New Key
      </Button>

      <TableContainer>
        <Table>
          <TableHeader>
            <tr>
              <Th>Name</Th>
              <Th>Key (masked)</Th>
              <Th>Daily Calls</Th>
              <Th>Status</Th>
              <Th>Last Used</Th>
              <Th>Actions</Th>
            </tr>
          </TableHeader>
          <tbody>
            {geminiKeys.map(key => (
              <TableRow key={key._id}>
                <Td>{key.name}</Td>
                <Td>{key.key.substring(0, 10)}...</Td>
                <Td>{key.dailyCalls}</Td>
                <Td>
                  <StatusBadge status={key.isActive ? 'active' : 'blocked'}>
                    {key.isActive ? 'Active' : 'Disabled'}
                  </StatusBadge>
                </Td>
                <Td>{key.lastUsedAt ? formatDate(key.lastUsedAt) : 'Never'}</Td>
                <Td>
                  <ActionButtons>
                    <Button
                      variant={key.isActive ? "warning" : "success"}
                      onClick={() => handleKeyAction('update', key._id, { isActive: !key.isActive })}
                      title={key.isActive ? 'Disable Key' : 'Enable Key'}
                    >
                      {key.isActive ? <FaEyeSlash size={14} /> : <FaEye size={14} />}
                    </Button>
                    <Button
                      variant="danger"
                      onClick={() => {
                        if (confirm('Are you sure you want to delete this key?')) {
                          handleKeyAction('delete', key._id);
                        }
                      }}
                      title="Delete Key"
                    >
                      <FaTrash size={14} />
                    </Button>
                  </ActionButtons>
                </Td>
              </TableRow>
            ))}
          </tbody>
        </Table>
      </TableContainer>
    </>
  );

  const renderSettings = () => (
    <FormCard>
      <FormTitle>System Settings</FormTitle>

      <FormGroup>
        <Label htmlFor="dailyLimit">Daily Message Limit</Label>
        <Input
          id="dailyLimit"
          type="number"
          value={dailyLimit}
          onChange={(e) => setDailyLimit(e.target.value)}
          placeholder="Enter daily limit"
        />
      </FormGroup>

      <FormGroup>
        <Label>
          <input
            type="checkbox"
            checked={maintenanceMode}
            onChange={(e) => setMaintenanceMode(e.target.checked)}
            style={{ marginRight: '8px' }}
          />
          Maintenance Mode
        </Label>
      </FormGroup>

      <FormGroup>
        <Label htmlFor="banner">Banner Message</Label>
        <TextArea
          id="banner"
          value={bannerMessage}
          onChange={(e) => setBannerMessage(e.target.value)}
          placeholder="Enter banner message (leave empty to hide)"
        />
      </FormGroup>

      <Button variant="primary" onClick={handleSettingsUpdate}>
        Save Settings
      </Button>
    </FormCard>
  );

  const renderLogs = () => (
    <>
      {/* Log Statistics */}
      {logStats && (
        <StatsGrid>
          <StatCard>
            <StatIcon><FaFileAlt size={24} /></StatIcon>
            <StatNumber>{logStats.totalLogs}</StatNumber>
            <StatLabel>Total Logs</StatLabel>
          </StatCard>
          <StatCard>
            <StatIcon><FaClock size={24} /></StatIcon>
            <StatNumber>{logStats.todayLogs}</StatNumber>
            <StatLabel>Today's Logs</StatLabel>
          </StatCard>
          <StatCard>
            <StatIcon><FaExclamationTriangle size={24} /></StatIcon>
            <StatNumber>{logStats.errorLogs}</StatNumber>
            <StatLabel>Error Logs</StatLabel>
          </StatCard>
          <StatCard>
            <StatIcon><FaUserShield size={24} /></StatIcon>
            <StatNumber>{logStats.adminActions}</StatNumber>
            <StatLabel>Admin Actions</StatLabel>
          </StatCard>
        </StatsGrid>
      )}

      {/* Filters */}
      <FormCard>
        <FormTitle>Filter Logs</FormTitle>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          <FormGroup>
            <Label htmlFor="actionFilter">Action</Label>
            <Select
              id="actionFilter"
              value={logFilters.action}
              onChange={(e) => setLogFilters({...logFilters, action: e.target.value})}
            >
              <option value="">All Actions</option>
              <option value="user_login">User Login</option>
              <option value="user_signup">User Signup</option>
              <option value="message_sent">Message Sent</option>
              <option value="user_update">User Update</option>
              <option value="user_delete">User Delete</option>
              <option value="user_ban">User Ban</option>
              <option value="user_unban">User Unban</option>
              <option value="api_key_added">API Key Added</option>
              <option value="api_key_deleted">API Key Deleted</option>
              <option value="settings_updated">Settings Updated</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <Label htmlFor="levelFilter">Level</Label>
            <Select
              id="levelFilter"
              value={logFilters.level}
              onChange={(e) => setLogFilters({...logFilters, level: e.target.value})}
            >
              <option value="">All Levels</option>
              <option value="info">Info</option>
              <option value="warning">Warning</option>
              <option value="error">Error</option>
              <option value="critical">Critical</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <Label htmlFor="startDate">Start Date</Label>
            <Input
              id="startDate"
              type="date"
              value={logFilters.startDate}
              onChange={(e) => setLogFilters({...logFilters, startDate: e.target.value})}
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="endDate">End Date</Label>
            <Input
              id="endDate"
              type="date"
              value={logFilters.endDate}
              onChange={(e) => setLogFilters({...logFilters, endDate: e.target.value})}
            />
          </FormGroup>
        </div>

        <ButtonGroup>
          <Button
            onClick={() => {
              setLogFilters({ action: '', level: '', startDate: '', endDate: '' });
              setCurrentLogPage(1);
            }}
          >
            Clear Filters
          </Button>
          <Button
            variant="danger"
            onClick={() => {
              if (confirm('Are you sure you want to clear logs older than 30 days?')) {
                handleClearOldLogs();
              }
            }}
          >
            Clear Old Logs (30+ days)
          </Button>
        </ButtonGroup>
      </FormCard>

      {/* Logs Table */}
      <TableContainer>
        <Table>
          <TableHeader>
            <tr>
              <Th>Timestamp</Th>
              <Th>User</Th>
              <Th>Action</Th>
              <Th>Level</Th>
              <Th>Message</Th>
              <Th>IP Address</Th>
            </tr>
          </TableHeader>
          <tbody>
            {logs.map(log => (
              <TableRow key={log._id}>
                <Td>{formatDate(log.createdAt)}</Td>
                <Td>
                  {log.userId ? (
                    <div>
                      <div style={{ fontWeight: '500' }}>{log.userId.name}</div>
                      <div style={{ fontSize: '12px', color: '#9CA3AF' }}>{log.userId.email}</div>
                    </div>
                  ) : (
                    <span style={{ color: '#9CA3AF' }}>System</span>
                  )}
                </Td>
                <Td>
                  <StatusBadge status={log.level === 'error' || log.level === 'critical' ? 'banned' : 'active'}>
                    {log.action.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </StatusBadge>
                </Td>
                <Td>
                  <StatusBadge status={
                    log.level === 'critical' ? 'banned' :
                    log.level === 'error' ? 'blocked' :
                    log.level === 'warning' ? 'admin' : 'active'
                  }>
                    {log.level.toUpperCase()}
                  </StatusBadge>
                </Td>
                <Td style={{ maxWidth: '300px', wordWrap: 'break-word' }}>
                  {log.message}
                  {log.details && Object.keys(log.details).length > 0 && (
                    <details style={{ marginTop: '8px' }}>
                      <summary style={{ cursor: 'pointer', color: '#4F46E5', fontSize: '12px' }}>
                        Show Details
                      </summary>
                      <pre style={{
                        background: '#f9fafb',
                        border: '1px solid #e5e7eb',
                        padding: '8px',
                        borderRadius: '4px',
                        fontSize: '11px',
                        marginTop: '4px',
                        overflow: 'auto',
                        maxHeight: '150px',
                        color: '#374151'
                      }}>
                        {JSON.stringify(log.details, null, 2)}
                      </pre>
                    </details>
                  )}
                </Td>
                <Td>{log.ipAddress || 'N/A'}</Td>
              </TableRow>
            ))}
          </tbody>
        </Table>
      </TableContainer>

      {/* Pagination */}
      {totalLogPages > 1 && (
        <Pagination>
          <PageButton
            disabled={currentLogPage === 1}
            onClick={() => setCurrentLogPage(currentLogPage - 1)}
          >
            Previous
          </PageButton>
          {Array.from({ length: totalLogPages }, (_, i) => i + 1).map(page => (
            <PageButton
              key={page}
              active={page === currentLogPage}
              onClick={() => setCurrentLogPage(page)}
            >
              {page}
            </PageButton>
          ))}
          <PageButton
            disabled={currentLogPage === totalLogPages}
            onClick={() => setCurrentLogPage(currentLogPage + 1)}
          >
            Next
          </PageButton>
        </Pagination>
      )}
    </>
  );

  const renderMaster = () => (
    <>
      <StatsGrid>
        <StatCard>
          <StatIcon><FaUsers size={24} /></StatIcon>
          <StatNumber>{stats?.users || 0}</StatNumber>
          <StatLabel>Total Users</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon><FaComments size={24} /></StatIcon>
          <StatNumber>{stats?.messagesToday || 0}</StatNumber>
          <StatLabel>Messages Today</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon><FaRobot size={24} /></StatIcon>
          <StatNumber>{stats?.geminiCalls || 0}</StatNumber>
          <StatLabel>Gemini Calls Today</StatLabel>
        </StatCard>
        <StatCard>
          <StatIcon><FaKey size={24} /></StatIcon>
          <StatNumber>{stats?.healthyKeys || 0}</StatNumber>
          <StatLabel>Healthy Keys</StatLabel>
        </StatCard>
      </StatsGrid>

      {/* Quick Actions */}
      <FormCard>
        <FormTitle>Quick Actions</FormTitle>
        <ButtonGroup>
          <Button variant="primary" onClick={() => setShowKeyModal(true)}>
            Add API Key
          </Button>
          <Button variant="success" onClick={() => setActiveTab('users')}>
            Manage Users
          </Button>
          <Button variant="warning" onClick={() => setActiveTab('settings')}>
            System Settings
          </Button>
        </ButtonGroup>
      </FormCard>

      {/* Users Table */}
      <FormCard>
        <FormTitle>Users Overview</FormTitle>
        <TableContainer>
          <Table>
            <TableHeader>
              <tr>
                <Th>Name</Th>
                <Th>Email</Th>
                <Th>Role</Th>
                <Th>Status</Th>
                <Th>Messages</Th>
                <Th>Actions</Th>
              </tr>
            </TableHeader>
            <tbody>
              {users.slice(0, 5).map(user => (
                <TableRow key={user._id}>
                  <Td>{user.name}</Td>
                  <Td>{user.email}</Td>
                  <Td>
                    <StatusBadge status={user.role === 'admin' ? 'admin' : 'active'}>
                      {user.role || 'user'}
                    </StatusBadge>
                  </Td>
                  <Td>
                    <StatusBadge status={user.isBanned ? 'banned' : user.isBlocked ? 'blocked' : 'active'}>
                      {user.isBanned ? 'Banned' : user.isBlocked ? 'Blocked' : 'Active'}
                    </StatusBadge>
                  </Td>
                  <Td>{user.dailyMessages || 0}</Td>
                  <Td>
                    <ActionButtons>
                      <Button
                        onClick={() => {
                          setSelectedUser(user);
                          setShowEditModal(true);
                        }}
                        title="Edit User"
                      >
                        <FaEdit size={14} />
                      </Button>
                      <Button
                        variant={user.isBanned ? "success" : "danger"}
                        onClick={() => handleUserAction(user._id, 'update', { isBanned: !user.isBanned })}
                        title={user.isBanned ? 'Unban User' : 'Ban User'}
                      >
                        {user.isBanned ? <FaCheckCircle size={14} /> : <FaBan size={14} />}
                      </Button>
                    </ActionButtons>
                  </Td>
                </TableRow>
              ))}
            </tbody>
          </Table>
        </TableContainer>
        <Button variant="primary" onClick={() => setActiveTab('users')} style={{ marginTop: '16px' }}>
          View All Users
        </Button>
      </FormCard>

      {/* API Keys Table */}
      <FormCard>
        <FormTitle>API Keys Overview</FormTitle>
        <TableContainer>
          <Table>
            <TableHeader>
              <tr>
                <Th>Name</Th>
                <Th>Status</Th>
                <Th>Daily Calls</Th>
                <Th>Last Used</Th>
                <Th>Actions</Th>
              </tr>
            </TableHeader>
            <tbody>
              {geminiKeys.slice(0, 5).map(key => (
                <TableRow key={key._id}>
                  <Td>{key.name}</Td>
                  <Td>
                    <StatusBadge status={key.isActive ? 'active' : 'blocked'}>
                      {key.isActive ? 'Active' : 'Disabled'}
                    </StatusBadge>
                  </Td>
                  <Td>{key.dailyCalls}</Td>
                  <Td>{key.lastUsedAt ? formatDate(key.lastUsedAt) : 'Never'}</Td>
                  <Td>
                    <ActionButtons>
                      <Button
                        variant={key.isActive ? "warning" : "success"}
                        onClick={() => handleKeyAction('update', key._id, { isActive: !key.isActive })}
                        title={key.isActive ? 'Disable Key' : 'Enable Key'}
                      >
                        {key.isActive ? <FaEyeSlash size={14} /> : <FaEye size={14} />}
                      </Button>
                    </ActionButtons>
                  </Td>
                </TableRow>
              ))}
            </tbody>
          </Table>
        </TableContainer>
        <Button variant="primary" onClick={() => setActiveTab('keys')} style={{ marginTop: '16px' }}>
          Manage All Keys
        </Button>
      </FormCard>

      {/* System Status */}
      <FormCard>
        <FormTitle>System Status</FormTitle>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          <div>
            <Label>Database Status</Label>
            <StatusBadge status="active">Connected</StatusBadge>
          </div>
          <div>
            <Label>API Status</Label>
            <StatusBadge status="active">Online</StatusBadge>
          </div>
          <div>
            <Label>Maintenance Mode</Label>
            <StatusBadge status={maintenanceMode ? 'blocked' : 'active'}>
              {maintenanceMode ? 'Enabled' : 'Disabled'}
            </StatusBadge>
          </div>
          <div>
            <Label>System Load</Label>
            <StatusBadge status="active">Normal</StatusBadge>
          </div>
        </div>
      </FormCard>
    </>
  );

  if (loading && !stats) {
    return (
      <AdminContainer>
        <Sidebar>
         
          <br />
          <br />

          <SidebarNav>
            {[
              { id: 'overview', label: 'Overview', icon: FaChartBar },
              { id: 'master', label: 'Master View', icon: FaDatabase },
              { id: 'users', label: 'Users', icon: FaUsers },
              { id: 'keys', label: 'API Keys', icon: FaKey },
              { id: 'settings', label: 'Settings', icon: FaCog },
              { id: 'logs', label: 'Logs', icon: FaFileAlt }
            ].map(tab => (
              <SidebarLink key={tab.id} $active={activeTab === tab.id} onClick={() => setActiveTab(tab.id as AdminTab)}>
                <tab.icon size={20} />
                {tab.label}
              </SidebarLink>
            ))}
          </SidebarNav>
        </Sidebar>
        <MainContent>
          <ContentHeader>
            <PageTitle>Loading admin panel...</PageTitle>
          </ContentHeader>
        </MainContent>
      </AdminContainer>
    );
  }

  return (
    <AdminContainer>
      <Sidebar>
      
        <SidebarNav>
          {[
            { id: 'overview', label: 'Overview', icon: FaChartBar },
            { id: 'master', label: 'Master View', icon: FaDatabase },
            { id: 'users', label: 'Users', icon: FaUsers },
            { id: 'keys', label: 'API Keys', icon: FaKey },
            { id: 'settings', label: 'Settings', icon: FaCog },
            { id: 'logs', label: 'Logs', icon: FaFileAlt }
          ].map(tab => (
            <SidebarLink key={tab.id} $active={activeTab === tab.id} onClick={() => setActiveTab(tab.id as AdminTab)}>
              <tab.icon size={20} />
              {tab.label}
            </SidebarLink>
          ))}
        </SidebarNav>
      </Sidebar>

      <MainContent>
        <ContentHeader>
          <PageTitle>
            {activeTab === 'overview' && 'Dashboard Overview'}
            {activeTab === 'master' && 'Master Data View'}
            {activeTab === 'users' && 'User Management'}
            {activeTab === 'keys' && 'API Key Management'}
            {activeTab === 'settings' && 'System Settings'}
            {activeTab === 'logs' && 'Activity Logs'}
          </PageTitle>
          <PageSubtitle>
            {activeTab === 'overview' && 'Monitor system statistics and recent activity'}
            {activeTab === 'master' && 'Complete overview of all system data and controls'}
            {activeTab === 'users' && 'Manage user accounts, roles, and permissions'}
            {activeTab === 'keys' && 'Configure and monitor Gemini API keys'}
            {activeTab === 'settings' && 'Configure system-wide settings and limits'}
            {activeTab === 'logs' && 'View system activity and audit logs'}
          </PageSubtitle>
        </ContentHeader>

        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'master' && renderMaster()}
        {activeTab === 'users' && renderUsers()}
        {activeTab === 'keys' && renderKeys()}
        {activeTab === 'settings' && renderSettings()}
        {activeTab === 'logs' && renderLogs()}
      </MainContent>

      {/* Edit User Modal */}
      {showEditModal && selectedUser && (
        <Modal onClick={() => setShowEditModal(false)}>
          <ModalContent onClick={e => e.stopPropagation()}>
            <ModalHeader>
              <ModalTitle>Edit User</ModalTitle>
              <CloseButton onClick={() => setShowEditModal(false)}>×</CloseButton>
            </ModalHeader>

            <FormGroup>
              <Label htmlFor="editName">Name</Label>
              <Input
                id="editName"
                type="text"
                value={selectedUser.name}
                onChange={(e) => setSelectedUser({...selectedUser, name: e.target.value})}
              />
            </FormGroup>

            <FormGroup>
              <Label htmlFor="editEmail">Email</Label>
              <Input
                id="editEmail"
                type="email"
                value={selectedUser.email}
                onChange={(e) => setSelectedUser({...selectedUser, email: e.target.value})}
              />
            </FormGroup>

            <FormGroup>
              <Label htmlFor="editRole">Role</Label>
              <Select
                id="editRole"
                value={selectedUser.role || 'user'}
                onChange={(e) => setSelectedUser({...selectedUser, role: e.target.value})}
              >
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </Select>
            </FormGroup>

            <FormGroup>
              <Label>
                <input
                  type="checkbox"
                  checked={selectedUser.isBanned || false}
                  onChange={(e) => setSelectedUser({...selectedUser, isBanned: e.target.checked})}
                  style={{ marginRight: '8px' }}
                />
                Banned
              </Label>
            </FormGroup>

            <FormGroup>
              <Label>
                <input
                  type="checkbox"
                  checked={selectedUser.isBlocked || false}
                  onChange={(e) => setSelectedUser({...selectedUser, isBlocked: e.target.checked})}
                  style={{ marginRight: '8px' }}
                />
                Blocked
              </Label>
            </FormGroup>

            <FormGroup>
              <Label htmlFor="editDailyMessages">Daily Messages</Label>
              <Input
                id="editDailyMessages"
                type="number"
                value={selectedUser.dailyMessages || 0}
                onChange={(e) => setSelectedUser({...selectedUser, dailyMessages: parseInt(e.target.value) || 0})}
                min="0"
              />
            </FormGroup>

            <ButtonGroup>
              <Button variant="primary" onClick={() => setShowEditModal(false)}>
                Cancel
              </Button>
              <Button
                variant="warning"
                onClick={() => {
                  handleUserAction(selectedUser._id, 'update', { resetCounter: true });
                  setSelectedUser({...selectedUser, dailyMessages: 0});
                }}
                style={{ marginRight: 'auto' }}
              >
                Reset Counter
              </Button>
              <Button
                variant="primary"
                onClick={() => {
                  handleUserAction(selectedUser._id, 'update', {
                    name: selectedUser.name,
                    email: selectedUser.email,
                    role: selectedUser.role,
                    isBanned: selectedUser.isBanned,
                    isBlocked: selectedUser.isBlocked,
                    dailyMessages: selectedUser.dailyMessages
                  });
                  setShowEditModal(false);
                }}
              >
                Save Changes
              </Button>
            </ButtonGroup>
          </ModalContent>
        </Modal>
      )}

      {/* Add Key Modal */}
      {showKeyModal && (
        <Modal onClick={() => setShowKeyModal(false)}>
          <ModalContent onClick={e => e.stopPropagation()}>
            <ModalHeader>
              <ModalTitle>Add New Gemini Key</ModalTitle>
              <CloseButton onClick={() => setShowKeyModal(false)}>×</CloseButton>
            </ModalHeader>

            <FormGroup>
              <Label htmlFor="keyName">Key Name</Label>
              <Input
                id="keyName"
                type="text"
                value={newKeyName}
                onChange={(e) => setNewKeyName(e.target.value)}
                placeholder="e.g., Primary Key, Backup Key"
              />
            </FormGroup>

            <FormGroup>
              <Label htmlFor="keyValue">API Key</Label>
              <Input
                id="keyValue"
                type="password"
                value={newKeyValue}
                onChange={(e) => setNewKeyValue(e.target.value)}
                placeholder="Enter your Gemini API key"
              />
            </FormGroup>

            <ButtonGroup>
              <Button variant="primary" onClick={() => setShowKeyModal(false)}>
                Cancel
              </Button>
              <Button
                variant="primary"
                onClick={() => handleKeyAction('add', undefined, { name: newKeyName, key: newKeyValue })}
                disabled={!newKeyName || !newKeyValue}
              >
                Add Key
              </Button>
            </ButtonGroup>
          </ModalContent>
        </Modal>
      )}

      {/* Toast Notifications */}
      <ToastContainer>
        {toasts.map(toast => (
          <Toast key={toast.id} type={toast.type}>
            {toast.message}
            {toast.showConfetti && (
              <ConfettiContainer>
                {Array.from({ length: 20 }).map((_, i) => (
                  <Confetti
                    key={i}
                    style={{
                      left: `${Math.random() * 100}%`,
                      animationDelay: `${Math.random() * 0.5}s`,
                      animationDuration: `${0.5 + Math.random() * 0.5}s`
                    }}
                  />
                ))}
              </ConfettiContainer>
            )}
          </Toast>
        ))}
      </ToastContainer>
    </AdminContainer>
  );
};

export default Admin;