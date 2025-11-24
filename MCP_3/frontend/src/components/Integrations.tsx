import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { integrationsApi } from '../api';
import { IntegrationStatus } from '../types';

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
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
  transition: all 0.3s;

  &:hover {
    border-color: rgba(79, 70, 229, 0.3);
    transform: translateY(-2px);
  }
`;

const StatusCard = styled(Card)`
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
`;

const StatusHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
`;

const StatusTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  color: #EDEDED;
  margin: 0;
`;

const StatusIndicator = styled.div<{ status: string }>`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;

  ${props => {
    switch (props.status) {
      case 'running':
        return `
          background: rgba(16, 185, 129, 0.2);
          color: #10B981;
          border: 1px solid rgba(16, 185, 129, 0.3);
        `;
      case 'stopped':
        return `
          background: rgba(107, 114, 128, 0.2);
          color: #6B7280;
          border: 1px solid rgba(107, 114, 128, 0.3);
        `;
      case 'error':
        return `
          background: rgba(239, 68, 68, 0.2);
          color: #EF4444;
          border: 1px solid rgba(239, 68, 68, 0.3);
        `;
      default:
        return `
          background: rgba(251, 191, 36, 0.2);
          color: #F59E0B;
          border: 1px solid rgba(251, 191, 36, 0.3);
        `;
    }
  }}
`;

const StatusDot = styled.div<{ status: string }>`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => {
    switch (props.status) {
      case 'running': return '#10B981';
      case 'stopped': return '#6B7280';
      case 'error': return '#EF4444';
      default: return '#F59E0B';
    }
  }};
`;

const StatusText = styled.p`
  font-size: 14px;
  color: #9CA3AF;
  margin-bottom: 16px;
  line-height: 1.5;
`;

const Button = styled.button`
  padding: 12px 24px;
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
    box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
  }

  &:active {
    transform: scale(0.98);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const DangerButton = styled(Button)`
  background: #DC2626;

  &:hover {
    background: #B91C1C;
  }
`;

const InstallCard = styled(Card)`
  text-align: center;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
`;

const InstallTitle = styled.h3`
  font-size: 24px;
  font-weight: 700;
  color: #EDEDED;
  margin-bottom: 8px;
`;

const InstallSubtitle = styled.p`
  font-size: 16px;
  color: #9CA3AF;
  margin-bottom: 24px;
  line-height: 1.5;
`;

const InstallButton = styled(Button)`
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  padding: 16px 32px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;

  &:hover {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
    transform: scale(1.05);
  }
`;

const InstallSteps = styled.div`
  text-align: left;
  margin-top: 24px;
`;

const Step = styled.div<{ completed?: boolean }>`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 8px;
  background: ${props => props.completed ? 'rgba(16, 185, 129, 0.1)' : 'rgba(255, 255, 255, 0.05)'};
`;

const StepNumber = styled.div<{ completed?: boolean }>`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  background: ${props => props.completed ? '#10B981' : '#6B7280'};
  color: white;
`;

const StepText = styled.span`
  font-size: 14px;
  color: #EDEDED;
`;

const ConfigCard = styled(Card)``;

const ConfigTitle = styled.h3`
  font-size: 18px;
  font-weight: 600;
  color: #EDEDED;
  margin-bottom: 16px;
`;

const ConfigItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  &:last-child {
    border-bottom: none;
  }
`;

const ConfigLabel = styled.span`
  font-size: 14px;
  color: #9CA3AF;
`;

const ConfigValue = styled.span`
  font-size: 14px;
  color: #EDEDED;
  font-weight: 500;
`;

const Integrations: React.FC = () => {
  const [integrationStatus, setIntegrationStatus] = useState<IntegrationStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [installing, setInstalling] = useState(false);
  const [installStep, setInstallStep] = useState(0);

  useEffect(() => {
    loadIntegrationStatus();
  }, []);

  const loadIntegrationStatus = async () => {
    try {
      const response = await integrationsApi.getStatus();
      setIntegrationStatus(response.data);
    } catch (error) {
      console.error('Failed to load integration status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInstallMCP = async () => {
    setInstalling(true);
    setInstallStep(1);

    try {
      // Step 1: Download MCP server
      setInstallStep(2);

      // Step 2: Configure project root
      setInstallStep(3);

      // Step 3: Install dependencies
      setInstallStep(4);

      // Step 4: Start MCP server
      await integrationsApi.startMcp();
      setInstallStep(5);

      // Refresh status
      await loadIntegrationStatus();

      alert('SensCoder MCP Server installed and started successfully!');
    } catch (error: any) {
      console.error('Failed to install MCP server:', error);
      alert('Failed to install MCP server: ' + (error.response?.data?.error || error.message));
    } finally {
      setInstalling(false);
      setInstallStep(0);
    }
  };

  const handleToggleMCP = async () => {
    if (!integrationStatus) return;

    try {
      if (integrationStatus.mcp.status === 'running') {
        await integrationsApi.stopMcp();
      } else {
        await integrationsApi.startMcp();
      }
      await loadIntegrationStatus();
    } catch (error: any) {
      console.error('Failed to toggle MCP server:', error);
      alert('Failed to toggle MCP server: ' + (error.response?.data?.error || error.message));
    }
  };

  const getMcpButtonText = () => {
    if (installing) return 'Installing...';
    if (integrationStatus?.mcp.status === 'running') return 'Stop SensCoder MCP Server';
    return 'Start SensCoder MCP Server';
  };

  const getMcpButtonColor = () => {
    if (integrationStatus?.mcp.status === 'running') return '#DC2626';
    return '#4F46E5';
  };

  if (loading) {
    return <Container><Title>Loading integrations...</Title></Container>;
  }

  const isMcpInstalled = integrationStatus?.mcp.status !== 'not_installed';

  return (
    <Container>
      <Title>Integrations</Title>
      <Subtitle>Connect SensCoder with your development environment.</Subtitle>

      <Section>
        <SectionTitle>SensCoder MCP Server</SectionTitle>

        {!isMcpInstalled ? (
          <InstallCard>
            <InstallTitle>🚀 Install SensCoder MCP Server</InstallTitle>
            <InstallSubtitle>
              Install the SensCoder MCP server locally to get AI-powered coding assistance directly in your IDE.
              The server provides tools for file operations, git management, terminal commands, and more.
            </InstallSubtitle>

            <InstallButton onClick={handleInstallMCP} disabled={installing}>
              {installing ? 'Installing...' : 'Install MCP Server'}
            </InstallButton>

            {installing && (
              <InstallSteps>
                <Step completed={installStep >= 1}>
                  <StepNumber completed={installStep >= 1}>1</StepNumber>
                  <StepText>Downloading MCP server files...</StepText>
                </Step>
                <Step completed={installStep >= 2}>
                  <StepNumber completed={installStep >= 2}>2</StepNumber>
                  <StepText>Configuring project root directory...</StepText>
                </Step>
                <Step completed={installStep >= 3}>
                  <StepNumber completed={installStep >= 3}>3</StepNumber>
                  <StepText>Installing Python dependencies...</StepText>
                </Step>
                <Step completed={installStep >= 4}>
                  <StepNumber completed={installStep >= 4}>4</StepNumber>
                  <StepText>Starting MCP server...</StepText>
                </Step>
                <Step completed={installStep >= 5}>
                  <StepNumber completed={installStep >= 5}>5</StepNumber>
                  <StepText>Installation complete!</StepText>
                </Step>
              </InstallSteps>
            )}
          </InstallCard>
        ) : (
          <StatusCard>
            <StatusHeader>
              <StatusTitle>SensCoder MCP Server</StatusTitle>
              <StatusIndicator status={integrationStatus.mcp.status}>
                <StatusDot status={integrationStatus.mcp.status} />
                {integrationStatus.mcp.status}
              </StatusIndicator>
            </StatusHeader>

            <StatusText>
              {integrationStatus.mcp.status === 'running'
                ? 'Your MCP server is running and ready to assist with coding tasks in your IDE.'
                : integrationStatus.mcp.status === 'stopped'
                ? 'Your MCP server is installed but not running. Start it to enable AI assistance.'
                : 'There was an error with your MCP server. Try restarting it.'}
            </StatusText>

            <Button
              onClick={handleToggleMCP}
              style={{ background: getMcpButtonColor() }}
              disabled={installing}
            >
              {getMcpButtonText()}
            </Button>
          </StatusCard>
        )}
      </Section>

      {isMcpInstalled && (
        <Section>
          <SectionTitle>Server Configuration</SectionTitle>
          <ConfigCard>
            <ConfigTitle>Current Settings</ConfigTitle>
            <ConfigItem>
              <ConfigLabel>Server Status</ConfigLabel>
              <ConfigValue>{integrationStatus?.mcp.status || 'Unknown'}</ConfigValue>
            </ConfigItem>
            <ConfigItem>
              <ConfigLabel>Port</ConfigLabel>
              <ConfigValue>{integrationStatus?.mcp.port || '3001'}</ConfigValue>
            </ConfigItem>
            <ConfigItem>
              <ConfigLabel>Project Root</ConfigLabel>
              <ConfigValue>{integrationStatus?.mcp.projectRoot || 'Not configured'}</ConfigValue>
            </ConfigItem>
            <ConfigItem>
              <ConfigLabel>Available Tools</ConfigLabel>
              <ConfigValue>File ops, Git, Terminal, Search</ConfigValue>
            </ConfigItem>
          </ConfigCard>
        </Section>
      )}

      <Section>
        <SectionTitle>IDE Integration</SectionTitle>
        <Card>
          <ConfigTitle>Connect to Your IDE</ConfigTitle>
          <StatusText>
            To use SensCoder in your IDE, configure the MCP server endpoint in your IDE's MCP settings.
            The server runs on <code style={{ background: '#374151', padding: '2px 4px', borderRadius: '4px' }}>
              http://localhost:{integrationStatus?.mcp.port || '3001'}
            </code>
          </StatusText>

          <div style={{ marginTop: '16px' }}>
            <h4 style={{ color: '#EDEDED', marginBottom: '8px' }}>Supported IDEs:</h4>
            <ul style={{ color: '#9CA3AF', paddingLeft: '20px' }}>
              <li>VS Code (with MCP extension)</li>
              <li>Cursor</li>
              <li>Other MCP-compatible editors</li>
            </ul>
          </div>
        </Card>
      </Section>
    </Container>
  );
};

export default Integrations;