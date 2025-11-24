import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { integrationsApi } from '../api';

const Container = styled.div`
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px;
  position: relative;
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: 48px;
`;

const Title = styled.h1`
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #EDEDED;
  margin-bottom: 8px;
`;

const Subtitle = styled.p`
  font-size: 16px;
  color: #9CA3AF;
  line-height: 1.5;
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
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
`;

const ProviderCard = styled(Card)`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ProviderInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 16px;
`;

const ProviderName = styled.h3`
  font-size: 16px;
  font-weight: 500;
  color: #EDEDED;
  margin: 0;
`;

const StatusBadge = styled.span<{ connected: boolean }>`
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  background: ${props => props.connected ? '#10B981' : '#6B7280'};
  color: white;
`;

const KeyBadge = styled.span`
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 10px;
  background: #4F46E5;
  color: white;
`;

const Button = styled.button`
  padding: 8px 16px;
  background: #4F46E5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: #6366F1;
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

const Modal = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background: #111827;
  border-radius: 16px;
  padding: 32px;
  width: 400px;
  max-width: 90vw;
`;

const ModalTitle = styled.h3`
  font-size: 20px;
  font-weight: 600;
  color: #EDEDED;
  margin-bottom: 24px;
`;

const Input = styled.input`
  width: 100%;
  padding: 12px 16px;
  background: #374151;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #EDEDED;
  font-size: 14px;
  margin-bottom: 16px;

  &:focus {
    outline: none;
    border-color: #4F46E5;
  }
`;

const TextArea = styled.textarea`
  width: 100%;
  padding: 12px 16px;
  background: #374151;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #EDEDED;
  font-size: 14px;
  margin-bottom: 16px;
  resize: vertical;
`;

const ModalButtons = styled.div`
  display: flex;
  gap: 12px;
  justify-content: flex-end;
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

const ToolItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);

  &:last-child {
    border-bottom: none;
  }
`;

const ToolLabel = styled.label`
  font-size: 14px;
  color: #EDEDED;
  cursor: pointer;
`;

const ToolWarning = styled.span`
  font-size: 12px;
  color: #F59E0B;
  margin-left: 8px;
`;

const ActivityList = styled.div`
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
`;

const ActivityItem = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);

  &:last-child {
    border-bottom: none;
  }
`;

const ActivityTime = styled.span`
  font-size: 12px;
  color: #6B7280;
  min-width: 80px;
`;

const ActivityText = styled.span`
  font-size: 14px;
  color: #EDEDED;
`;

interface Provider {
  name: string;
  connected: boolean;
  usingOwnKey: boolean;
  lastUsed?: string;
}

interface McpStatus {
  running: boolean;
  port?: number;
}

interface Tool {
  name: string;
  enabled: boolean;
  warning?: string;
}

const ApiIntegrationsPage: React.FC = () => {
  const [providers, setProviders] = useState<Provider[]>([
    { name: 'Google Gemini', connected: true, usingOwnKey: false, lastUsed: '2 min ago' },
    { name: 'OpenAI', connected: false, usingOwnKey: false },
    { name: 'Anthropic', connected: true, usingOwnKey: true, lastUsed: '1 hour ago' },
    { name: 'Groq', connected: false, usingOwnKey: false },
    { name: 'OpenRouter', connected: false, usingOwnKey: false },
    { name: 'Ollama (Local)', connected: true, usingOwnKey: false, lastUsed: '5 min ago' },
  ]);

  const [mcpStatus, setMcpStatus] = useState<McpStatus>({ running: true, port: 4001 });

  const [tools, setTools] = useState<Tool[]>([
    { name: 'Filesystem access (read/write)', enabled: true, warning: 'Allows reading and writing files' },
    { name: 'Git integration', enabled: true, warning: 'Allows git commands' },
    { name: 'Terminal/exec commands', enabled: false, warning: 'High security risk - allows running system commands' },
  ]);

  const [modalOpen, setModalOpen] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState<string>('');
  const [apiKey, setApiKey] = useState('');

  const [activities] = useState([
    { time: '2 min ago', text: 'Used Gemini for 3 messages' },
    { time: '1 hour ago', text: 'Connected OpenAI key' },
    { time: '2 hours ago', text: 'Started MCP server on port 4001' },
  ]);

  useEffect(() => {
    // Fetch initial status
    integrationsApi.getStatus().then(response => {
      // Update state with real data
      console.log('Status:', response.data);
    }).catch(error => {
      console.error('Failed to fetch status:', error);
    });
  }, []);

  const handleConfigureProvider = (providerName: string) => {
    setSelectedProvider(providerName);
    setModalOpen(true);
    // In real app, fetch existing key if any
    setApiKey('');
  };

  const handleSaveKey = () => {
    integrationsApi.setProviderKey(selectedProvider, apiKey).then(() => {
      // Update provider status
      setProviders(prev => prev.map(p =>
        p.name === selectedProvider ? { ...p, connected: true, usingOwnKey: true } : p
      ));
      setModalOpen(false);
      setApiKey('');
    }).catch(error => {
      console.error('Failed to save key:', error);
    });
  };

  const handleRemoveKey = () => {
    integrationsApi.removeProviderKey(selectedProvider).then(() => {
      setProviders(prev => prev.map(p =>
        p.name === selectedProvider ? { ...p, connected: false, usingOwnKey: false } : p
      ));
      setModalOpen(false);
    }).catch(error => {
      console.error('Failed to remove key:', error);
    });
  };

  const handleStartMcp = () => {
    integrationsApi.startMcp().then(response => {
      setMcpStatus({ running: true, port: response.data.port });
    }).catch(error => {
      console.error('Failed to start MCP:', error);
    });
  };

  const handleStopMcp = () => {
    integrationsApi.stopMcp().then(() => {
      setMcpStatus({ running: false });
    }).catch(error => {
      console.error('Failed to stop MCP:', error);
    });
  };

  const handleToggleTool = (toolName: string, enabled: boolean) => {
    setTools(prev => prev.map(t =>
      t.name === toolName ? { ...t, enabled } : t
    ));
    // In real app, save to backend
  };

  return (
    <Container>
      <Header>
        <Title>API & Integrations</Title>
        <Subtitle>Connect LLM providers, manage MCP server, and control your tools.</Subtitle>
      </Header>

      <Section>
        <SectionTitle>LLM Providers</SectionTitle>
        {providers.map(provider => (
          <ProviderCard key={provider.name}>
            <ProviderInfo>
              <ProviderName>{provider.name}</ProviderName>
              <StatusBadge connected={provider.connected}>
                {provider.connected ? 'Connected' : 'Not connected'}
              </StatusBadge>
              {provider.usingOwnKey && <KeyBadge>Using your key</KeyBadge>}
              {provider.lastUsed && (
                <span style={{ fontSize: '12px', color: '#6B7280' }}>
                  Last used: {provider.lastUsed}
                </span>
              )}
            </ProviderInfo>
            <Button onClick={() => handleConfigureProvider(provider.name)}>
              Configure
            </Button>
          </ProviderCard>
        ))}
      </Section>

      <Section>
        <SectionTitle>MCP & Local Tools</SectionTitle>
        <Card>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
            <div>
              <h3 style={{ fontSize: '16px', fontWeight: '500', color: '#EDEDED', margin: '0 0 4px 0' }}>
                SensCoder MCP Server
              </h3>
              <p style={{ fontSize: '14px', color: '#9CA3AF', margin: 0 }}>
                Status: {mcpStatus.running ? 'Running' : 'Stopped'}
                {mcpStatus.port && ` on port ${mcpStatus.port}`}
              </p>
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              {!mcpStatus.running ? (
                <Button onClick={handleStartMcp}>Start MCP Server</Button>
              ) : (
                <DangerButton onClick={handleStopMcp}>Stop MCP Server</DangerButton>
              )}
              <Button>Open MCP Wizard</Button>
            </div>
          </div>

          <div>
            <h4 style={{ fontSize: '14px', fontWeight: '500', color: '#EDEDED', marginBottom: '16px' }}>
              Enabled Tools
            </h4>
            {tools.map(tool => (
              <ToolItem key={tool.name}>
                <div>
                  <ToolLabel htmlFor={`tool-${tool.name}`}>
                    {tool.name}
                  </ToolLabel>
                  {tool.warning && <ToolWarning>{tool.warning}</ToolWarning>}
                </div>
                <Toggle>
                  <ToggleInput
                    type="checkbox"
                    id={`tool-${tool.name}`}
                    checked={tool.enabled}
                    onChange={(e) => handleToggleTool(tool.name, e.target.checked)}
                  />
                  <ToggleSlider />
                </Toggle>
              </ToolItem>
            ))}
          </div>
        </Card>
      </Section>

      <Section>
        <SectionTitle>Activity & Logs</SectionTitle>
        <ActivityList>
          {activities.map((activity, index) => (
            <ActivityItem key={index}>
              <ActivityTime>{activity.time}</ActivityTime>
              <ActivityText>{activity.text}</ActivityText>
            </ActivityItem>
          ))}
        </ActivityList>
      </Section>

      {modalOpen && (
        <Modal onClick={() => setModalOpen(false)}>
          <ModalContent onClick={e => e.stopPropagation()}>
            <ModalTitle>Configure {selectedProvider}</ModalTitle>
            <Input
              type="password"
              placeholder="Enter API key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <TextArea
              placeholder="Keys are stored encrypted and never shown in full. Only **** + last 4 characters are displayed."
              rows={3}
              readOnly
              value="Keys are stored encrypted and never shown in full. Only **** + last 4 characters are displayed."
            />
            <ModalButtons>
              <DangerButton onClick={handleRemoveKey}>Remove Key</DangerButton>
              <Button onClick={handleSaveKey}>Save Key</Button>
            </ModalButtons>
          </ModalContent>
        </Modal>
      )}
    </Container>
  );
};

export default ApiIntegrationsPage;