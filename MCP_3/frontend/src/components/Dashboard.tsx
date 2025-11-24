import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { User } from '../types';
import { authApi, chatApi, integrationsApi } from '../api';
import { UserProfile, ChatMessage, IntegrationStatus } from '../types';

interface DashboardProps {
  user: User | null;
}

const Container = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 32px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const LeftColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: 32px;
`;

const RightColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: 32px;
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

const ProfileCard = styled(Card)`
  text-align: center;
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
  margin: 0 auto 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
`;

const Name = styled.h2`
  font-size: 20px;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: #EDEDED;
  margin-bottom: 4px;
`;

const Email = styled.p`
  font-size: 14px;
  color: #9CA3AF;
  line-height: 1.6;
`;

const StatsCard = styled(Card)``;

const StatTitle = styled.h3`
  font-size: 16px;
  font-weight: 500;
  color: #EDEDED;
  margin-bottom: 16px;
`;

const StatItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  &:last-child {
    margin-bottom: 0;
  }
`;

const StatLabel = styled.span`
  font-size: 14px;
  color: #9CA3AF;
`;

const StatValue = styled.span`
  font-size: 14px;
  font-weight: 500;
  color: #EDEDED;
`;

const ProgressBar = styled.div`
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 8px;
`;

const ProgressFill = styled.div<{ percentage: number }>`
  height: 100%;
  background: #4F46E5;
  width: ${props => props.percentage}%;
  border-radius: 2px;
  transition: width 0.3s ease;
`;

const ChatCard = styled(Card)``;

const ChatTitle = styled.h3`
  font-size: 16px;
  font-weight: 500;
  color: #EDEDED;
  margin-bottom: 16px;
`;

const ChatBubble = styled.div<{ isUser?: boolean }>`
  padding: 12px 16px;
  background: ${props => props.isUser ? '#4F46E5' : '#374151'};
  border-radius: 12px;
  margin-bottom: 12px;
  max-width: 80%;
  align-self: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  font-size: 14px;
  color: #EDEDED;
  line-height: 1.4;
`;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
  max-height: 300px;
  overflow-y: auto;
`;

const ChatInput = styled.div`
  display: flex;
  gap: 8px;
  margin-top: 16px;
`;

const Input = styled.input`
  flex: 1;
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

  &::placeholder {
    color: #9CA3AF;
  }
`;

const Button = styled.button`
  padding: 12px 16px;
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

const MCPButton = styled(Button)<{ status?: string }>`
  background: ${props => {
    switch (props.status) {
      case 'running': return '#10B981';
      case 'error': return '#EF4444';
      default: return '#6B7280';
    }
  }};
  margin-top: 16px;

  &:hover {
    background: ${props => {
      switch (props.status) {
        case 'running': return '#059669';
        case 'error': return '#DC2626';
        default: return '#4B5563';
      }
    }};
  }
`;

const StatusIndicator = styled.div<{ status: string }>`
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: ${props => {
    switch (props.status) {
      case 'running': return '#10B981';
      case 'error': return '#EF4444';
      default: return '#6B7280';
    }
  }};
  margin-right: 8px;
`;

const Dashboard: React.FC<DashboardProps> = ({ user }) => {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [integrationStatus, setIntegrationStatus] = useState<IntegrationStatus | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
const [isMcpLoading, setIsMcpLoading] = useState(false);
  const [mcpConfig, setMcpConfig] = useState<any>(null);
  const [mcpError, setMcpError] = useState<string | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadUserData();
    loadIntegrationStatus();
  }, []);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const loadUserData = async () => {
    try {
      const response = await authApi.me();
      setUserProfile(response.data);
    } catch (error) {
      console.error('Failed to load user data:', error);
    }
  };

  const loadIntegrationStatus = async () => {
    try {
      const response = await integrationsApi.getStatus();
      setIntegrationStatus(response.data);
    } catch (error) {
      console.error('Failed to load integration status:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const chatMessages = [...messages, userMessage].map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const response = await chatApi.sendMessage(chatMessages);

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Refresh user data to update usage stats
      loadUserData();
    } catch (error: any) {
      console.error('Failed to send message:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: error.response?.data?.error || 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMcpToggle = async () => {
    if (!integrationStatus) return;

    setIsMcpLoading(true);
    setMcpError(null);

    try {
      if (integrationStatus.mcp.status === 'running') {
        await integrationsApi.stopMcp();
        setMcpConfig(null);
      } else {
        const response = await integrationsApi.startMcp();
        setMcpConfig(response.data);
      }
      // Refresh status
      await loadIntegrationStatus();
    } catch (error: any) {
      console.error('Failed to toggle MCP server:', error);
      setMcpError(error.response?.data?.error || error.message || 'Failed to toggle MCP server');
    } finally {
      setIsMcpLoading(false);
    }
  };

  const getMcpButtonText = () => {
    if (isMcpLoading) return 'Starting MCP Server...';
    if (integrationStatus?.mcp.status === 'running') return `MCP Server Running on Port ${integrationStatus.mcp.port || 'Unknown'}`;
    return 'Start SensCoder MCP Server';
  };

  const getUsagePercentage = () => {
    if (!userProfile?.usage) return 0;
    return (userProfile.usage.messageCount / userProfile.usage.dailyLimit) * 100;
  };

  return (
    <Container>
      <LeftColumn>
        <ProfileCard>
          <Avatar>
            {userProfile?.user?.name?.charAt(0).toUpperCase() || user?.name?.charAt(0).toUpperCase() || 'U'}
          </Avatar>
          <Name>{userProfile?.user?.name || user?.name || 'User'}</Name>
          <Email>{userProfile?.user?.email || user?.email || 'user@example.com'}</Email>
        </ProfileCard>

        <StatsCard>
          <StatTitle>Usage Stats</StatTitle>
          <StatItem>
            <StatLabel>Messages today</StatLabel>
            <StatValue>{userProfile?.usage?.messagesToday || '0 / 20'}</StatValue>
          </StatItem>
          <ProgressBar>
            <ProgressFill percentage={getUsagePercentage()} />
          </ProgressBar>
          <StatItem>
            <StatLabel>Provider</StatLabel>
            <StatValue>{userProfile?.settings?.provider || 'gemini'}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>API Key</StatLabel>
            <StatValue>{userProfile?.settings?.hasApiKey ? 'Set' : 'Shared'}</StatValue>
          </StatItem>
        </StatsCard>
      </LeftColumn>

      <RightColumn>
        <ChatCard>
          <ChatTitle>Chat with SensCoder</ChatTitle>
          <ChatContainer ref={chatContainerRef}>
            {messages.length === 0 && (
              <ChatBubble>
                <ReactMarkdown
                  components={{
                    code({node, inline, className, children, ...props}) {
                      const match = /language-(\w+)/.exec(className || "");
                      return !inline && match ? (
                        <SyntaxHighlighter
                          language={match[1]}
                          PreTag="div"
                          style={{
                            margin: 0,
                            padding: '8px',
                            borderRadius: '4px',
                            fontSize: '12px',
                            background: '#1f2937'
                          }}
                          {...props}
                        >
                          {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                      ) : (
                        <code
                          className={className}
                          style={{
                            background: 'rgba(0,0,0,0.2)',
                            padding: '2px 4px',
                            borderRadius: '3px',
                            fontSize: '12px'
                          }}
                          {...props}
                        >
                          {children}
                        </code>
                      );
                    }
                  }}
                >
                  👋 Hi! I'm your SensCoder assistant. Ask me anything about coding, and I'll help you build amazing things!
                </ReactMarkdown>
              </ChatBubble>
            )}
            {messages.map((message, index) => (
              <ChatBubble key={index} isUser={message.role === 'user'}>
                <ReactMarkdown
                  components={{
                    code({node, inline, className, children, ...props}) {
                      const match = /language-(\w+)/.exec(className || "");
                      return !inline && match ? (
                        <SyntaxHighlighter
                          language={match[1]}
                          PreTag="div"
                          style={{
                            margin: 0,
                            padding: '8px',
                            borderRadius: '4px',
                            fontSize: '12px',
                            background: '#1f2937'
                          }}
                          {...props}
                        >
                          {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                      ) : (
                        <code
                          className={className}
                          style={{
                            background: 'rgba(0,0,0,0.2)',
                            padding: '2px 4px',
                            borderRadius: '3px',
                            fontSize: '12px'
                          }}
                          {...props}
                        >
                          {children}
                        </code>
                      );
                    }
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </ChatBubble>
            ))}
            {isLoading && (
              <ChatBubble>
                <StatusIndicator status="running" /> Thinking...
              </ChatBubble>
            )}
          </ChatContainer>
          <ChatInput>
            <Input
              placeholder="Ask me anything about coding..."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              disabled={isLoading}
            />
            <Button onClick={handleSendMessage} disabled={isLoading || !inputMessage.trim()}>
              Send
            </Button>
          </ChatInput>
          <MCPButton
            status={integrationStatus?.mcp.status}
            onClick={handleMcpToggle}
            disabled={isMcpLoading}
          >
            <StatusIndicator status={integrationStatus?.mcp.status || 'stopped'} />
            {getMcpButtonText()}
          </MCPButton>

          {mcpError && (
            <div style={{
              color: '#EF4444',
              fontSize: '14px',
              marginTop: '8px',
              padding: '8px',
              background: 'rgba(239, 68, 68, 0.1)',
              borderRadius: '4px',
              border: '1px solid rgba(239, 68, 68, 0.2)'
            }}>
              Error: {mcpError}
            </div>
          )}

          {integrationStatus?.mcp.status === 'running' && mcpConfig && (
            <div style={{
              marginTop: '16px',
              padding: '16px',
              background: 'rgba(16, 185, 129, 0.1)',
              border: '1px solid rgba(16, 185, 129, 0.2)',
              borderRadius: '8px'
            }}>
              <div style={{
                fontSize: '14px',
                fontWeight: '500',
                color: '#10B981',
                marginBottom: '8px'
              }}>
                MCP Server Configuration
              </div>
              <div style={{
                fontSize: '12px',
                color: '#6B7280',
                marginBottom: '12px'
              }}>
                Copy this JSON configuration and paste it into your Claude Desktop or Cursor MCP settings:
              </div>
              <div style={{
                position: 'relative'
              }}>
                <pre style={{
                  background: '#1F2937',
                  color: '#EDEDED',
                  padding: '12px',
                  borderRadius: '4px',
                  fontSize: '12px',
                  fontFamily: 'monospace',
                  overflow: 'auto',
                  maxHeight: '200px',
                  margin: '0'
                }}>
                  {JSON.stringify(mcpConfig.configJson, null, 2)}
                </pre>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(JSON.stringify(mcpConfig.configJson, null, 2));
                    // Could add a toast notification here
                  }}
                  style={{
                    position: 'absolute',
                    top: '8px',
                    right: '8px',
                    padding: '4px 8px',
                    background: '#4F46E5',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    fontSize: '11px',
                    cursor: 'pointer'
                  }}
                >
                  Copy
                </button>
              </div>
            </div>
          )}
        </ChatCard>
      </RightColumn>
    </Container>
  );
};

export default Dashboard;