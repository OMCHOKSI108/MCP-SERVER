import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { UserSettings as UserSettingsType, UserProfile } from '../types';
import { authApi, settingsApi } from '../api';

const Container = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 32px;
`;

const Title = styled.h1`
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
  color: #EDEDED;
`;

const Subtitle = styled.p`
  font-size: 16px;
  color: #9CA3AF;
  margin-bottom: 48px;
`;

const Section = styled.section`
  margin-bottom: 48px;
`;

const SectionTitle = styled.h2`
  font-size: 20px;
  font-weight: 600;
  color: #EDEDED;
  margin-bottom: 24px;
`;

const Card = styled.div`
  background: var(--gradient-surface);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
`;

const FormGroup = styled.div`
  margin-bottom: 24px;

  &:last-child {
    margin-bottom: 0;
  }
`;

const Label = styled.label`
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #EDEDED;
  margin-bottom: 8px;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px 16px;
  background: #374151;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #EDEDED;
  font-size: 14px;
  transition: all 0.2s;

  &:focus {
    outline: none;
    border-color: #4F46E5;
    box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
  }

  &:read-only {
    background: #1F2937;
    cursor: not-allowed;
  }
`;

const Select = styled.select`
  width: 100%;
  padding: 12px 16px;
  background: #374151;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #EDEDED;
  font-size: 14px;
  transition: all 0.2s;

  &:focus {
    outline: none;
    border-color: #4F46E5;
    box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
  }
`;

const Avatar = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #4F46E5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 600;
  color: white;
  margin-bottom: 16px;
`;

const Button = styled.button`
  padding: 12px 24px;
  background: var(--gradient-button);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: var(--gradient-button-hover);
    transform: scale(1.02);
  }

  &:active {
    transform: scale(0.98);
  }
`;

const DangerButton = styled(Button)`
  background: #DC2626;

  &:hover {
    background: #B91C1C;
  }
`;

const Toggle = styled.label`
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
`;

const ToggleInput = styled.input`
  opacity: 0;
  width: 0;
  height: 0;

  &:checked + span {
    background-color: #4F46E5;
  }

  &:checked + span:before {
    transform: translateX(20px);
  }
`;

const ToggleSlider = styled.span`
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #374151;
  transition: 0.2s;
  border-radius: 24px;

  &:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: 0.2s;
    border-radius: 50%;
  }
`;

const ToggleLabel = styled.span`
  font-size: 14px;
  color: #9CA3AF;
  margin-left: 12px;
`;

const HelperText = styled.p`
  font-size: 12px;
  color: #6B7280;
  margin-top: 4px;
  line-height: 1.4;
`;

const PreviewCard = styled.div<{ theme: string; accent: string }>`
  background: ${props => props.theme === 'dark' ? '#111827' : '#FFFFFF'};
  border: 1px solid ${props => props.theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)'};
  border-radius: 8px;
  padding: 16px;
  margin-top: 16px;
`;

const PreviewButton = styled.button<{ accent: string }>`
  padding: 8px 16px;
  background: ${props => props.accent};
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
`;

const AccentOptions = styled.div`
  display: flex;
  gap: 8px;
  margin-top: 8px;
`;

const AccentDot = styled.button<{ color: string; selected: boolean }>`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: ${props => props.color};
  border: 2px solid ${props => props.selected ? '#EDEDED' : 'transparent'};
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    transform: scale(1.1);
  }
`;

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<UserSettingsType>({
    provider: 'gemini',
    useOwnKey: false,
    hasApiKey: false,
    theme: 'dark'
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [defaultProvider, setDefaultProvider] = useState('gemini');
  const [useOwnKey, setUseOwnKey] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [accentColor, setAccentColor] = useState('#4F46E5');

  // Password change state
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [changingPassword, setChangingPassword] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const userResponse = await authApi.me();
      setUserProfile(userResponse.data);
      setName(userResponse.data.user.name);
      setEmail(userResponse.data.user.email);
      setDefaultProvider(userResponse.data.settings.provider);
      setUseOwnKey(userResponse.data.settings.hasApiKey);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async () => {
    setSaving(true);
    try {
      await settingsApi.updateSettings({ name });
      alert('Profile updated successfully!');
      await loadData(); // Refresh data
    } catch (error) {
      console.error('Failed to update profile:', error);
      alert('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleSaveProvider = async () => {
    setSaving(true);
    try {
      await settingsApi.updateSettings({
        provider: defaultProvider,
        hasApiKey: useOwnKey,
        apiKey: useOwnKey ? apiKey : undefined
      });
      alert('Provider settings updated successfully!');
      await loadData(); // Refresh data
    } catch (error) {
      console.error('Failed to update provider settings:', error);
      alert('Failed to update provider settings');
    } finally {
      setSaving(false);
    }
  };

  const handleChangePassword = async () => {
    if (!currentPassword || !newPassword || !confirmPassword) {
      alert('Please fill in all password fields');
      return;
    }

    if (newPassword !== confirmPassword) {
      alert('New passwords do not match');
      return;
    }

    if (newPassword.length < 6) {
      alert('New password must be at least 6 characters long');
      return;
    }

    setChangingPassword(true);
    try {
      const response = await authApi.changePassword(currentPassword, newPassword);
      const { token, user } = response.data;

      // Update localStorage with new token and user data
      localStorage.setItem('token', token);
      // Note: User state will be updated when the page refreshes or when auth check runs

      alert('Password changed successfully! You have been logged in with the new password.');
      // Clear password fields
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (error: any) {
      console.error('Failed to change password:', error);
      alert(error.message || 'Failed to change password');
    } finally {
      setChangingPassword(false);
    }
  };

  const accentColors = [
    { name: 'Purple', value: '#4F46E5' },
    { name: 'Blue', value: '#3B82F6' },
    { name: 'Green', value: '#10B981' },
  ];

  if (loading) {
    return <Container><Title>Loading settings...</Title></Container>;
  }

  return (
    <Container>
      <Title>Settings</Title>
      <Subtitle>Manage your account, preferences, and integrations.</Subtitle>

      <Section>
        <SectionTitle>Profile</SectionTitle>
        <Card>
          <Avatar>
            {name.charAt(0).toUpperCase()}
          </Avatar>
          <FormGroup>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </FormGroup>
          <FormGroup>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              readOnly
            />
          </FormGroup>
          <Button onClick={handleSaveProfile} disabled={saving}>
            {saving ? 'Saving...' : 'Save Changes'}
          </Button>
        </Card>
      </Section>

      <Section>
        <SectionTitle>LLM Provider & API Key</SectionTitle>
        <Card>
          <FormGroup>
            <Label htmlFor="provider">Default LLM Provider</Label>
            <Select
              id="provider"
              value={defaultProvider}
              onChange={(e) => setDefaultProvider(e.target.value)}
            >
              <option value="gemini">Google Gemini</option>
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
              <option value="groq">Groq</option>
              <option value="openrouter">OpenRouter</option>
              <option value="ollama">Ollama (Local)</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <Toggle>
                <ToggleInput
                  type="checkbox"
                  checked={useOwnKey}
                  onChange={(e) => setUseOwnKey(e.target.checked)}
                />
                <ToggleSlider />
              </Toggle>
              <ToggleLabel>Use my own API key</ToggleLabel>
            </div>
            <HelperText>
              {useOwnKey
                ? 'Using your own key; shared limit does not apply.'
                : 'Using SensCoder shared Gemini keys (20 messages/day limit)'
              }
            </HelperText>
          </FormGroup>

          {useOwnKey && (
            <FormGroup>
              <Label htmlFor="apiKey">API Key</Label>
              <Input
                id="apiKey"
                type="password"
                placeholder="Enter your API key"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
              />
              <HelperText>
                Your API key is encrypted and stored securely. We never share or use it for other purposes.
              </HelperText>
            </FormGroup>
          )}

          <Button onClick={handleSaveProvider} disabled={saving}>
            {saving ? 'Saving...' : 'Save Provider Settings'}
          </Button>
        </Card>
      </Section>

      <Section>
        <SectionTitle>Appearance</SectionTitle>
        <Card>
          <FormGroup>
            <Label>Theme</Label>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: '8px' }}>
              <Toggle>
                <ToggleInput
                  type="checkbox"
                  checked={settings.theme === 'dark'}
                  onChange={(e) => setSettings(prev => ({ ...prev, theme: e.target.checked ? 'dark' : 'light' }))}
                />
                <ToggleSlider />
              </Toggle>
              <ToggleLabel>Dark mode</ToggleLabel>
            </div>
          </FormGroup>

          <FormGroup>
            <Label>Accent Color</Label>
            <AccentOptions>
              {accentColors.map(color => (
                <AccentDot
                  key={color.value}
                  color={color.value}
                  selected={accentColor === color.value}
                  onClick={() => setAccentColor(color.value)}
                />
              ))}
            </AccentOptions>
          </FormGroup>

          <PreviewCard theme={settings.theme} accent={accentColor}>
            <h4 style={{ fontSize: '14px', color: settings.theme === 'dark' ? '#EDEDED' : '#111827', margin: '0 0 8px 0' }}>
              Preview
            </h4>
            <PreviewButton accent={accentColor}>Button</PreviewButton>
          </PreviewCard>
        </Card>
      </Section>

      <Section>
        <SectionTitle>Security</SectionTitle>
        <Card>
          <FormGroup>
            <Label htmlFor="currentPassword">Current Password</Label>
            <Input
              id="currentPassword"
              type="password"
              placeholder="Enter current password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
            />
          </FormGroup>
          <FormGroup>
            <Label htmlFor="newPassword">New Password</Label>
            <Input
              id="newPassword"
              type="password"
              placeholder="Enter new password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
          </FormGroup>
          <FormGroup>
            <Label htmlFor="confirmPassword">Confirm New Password</Label>
            <Input
              id="confirmPassword"
              type="password"
              placeholder="Confirm new password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </FormGroup>
          <div style={{ display: 'flex', gap: '12px' }}>
            <Button onClick={handleChangePassword} disabled={changingPassword}>
              {changingPassword ? 'Changing...' : 'Change Password'}
            </Button>
            <DangerButton>Logout from all devices</DangerButton>
          </div>
        </Card>
      </Section>
    </Container>
  );
};

export default Settings;