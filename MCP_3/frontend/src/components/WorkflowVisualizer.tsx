import React, { useState } from 'react';
import styled from 'styled-components';
import { UserIcon, AppIcon, BrainIcon, ServerIcon, FolderIcon } from './Icons.tsx';

const Container = styled.div`
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
`;

const Title = styled.h2`
  font-size: 20px;
  font-weight: 500;
  color: #EDEDED;
  letter-spacing: -0.02em;
`;

const Controls = styled.div`
  display: flex;
  gap: 8px;
`;

const ControlButton = styled.button<{ active?: boolean }>`
  padding: 8px 16px;
  background: ${props => props.active ? '#4F46E5' : '#374151'};
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: ${props => props.active ? '#6366F1' : '#4B5563'};
    transform: scale(1.02);
  }

  &:active {
    transform: scale(0.98);
  }
`;

const WorkflowContainer = styled.div`
  position: relative;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const Node = styled.div<{ active?: boolean; error?: boolean }>`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: ${props => props.error ? '#DC2626' : props.active ? '#4F46E5' : '#374151'};
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  min-width: 100px;
  text-align: center;
  transition: all 0.3s;
  transform: ${props => props.active ? 'scale(1.03)' : 'scale(1)'};
  box-shadow: ${props => props.active ? '0 0 20px rgba(79, 70, 229, 0.3)' : '0 2px 4px rgba(0,0,0,0.1)'};

  ${props => props.active && `
    animation: glow 2s ease-in-out infinite alternate;
  `}
`;

const NodeIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
`;

const NodeLabel = styled.div`
  font-size: 12px;
  font-weight: 500;
  color: #EDEDED;
`;

const NodeStatus = styled.div`
  font-size: 10px;
  color: #9CA3AF;
`;

const Connector = styled.div<{ active?: boolean }>`
  flex: 1;
  height: 2px;
  background: ${props => props.active ? '#4F46E5' : 'rgba(255, 255, 255, 0.1)'};
  position: relative;
  margin: 0 8px;
  border-radius: 1px;
  overflow: hidden;

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: -20px;
    width: 20px;
    height: 100%;
    background: linear-gradient(90deg, transparent, #4F46E5, transparent);
    animation: ${props => props.active ? 'flow 3s linear infinite' : 'none'};
  }
`;

const RunningDot = styled.div<{ position: number }>`
  position: absolute;
  top: 50%;
  left: ${props => props.position}%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: #4F46E5;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(79, 70, 229, 0.5);
  animation: moveDot 5s linear infinite;
`;

type WorkflowState = 'idle' | 'running' | 'error';

interface WorkflowVisualizerProps {
  initialState?: WorkflowState;
}

const WorkflowVisualizer: React.FC<WorkflowVisualizerProps> = ({ initialState = 'running' }) => {
  const [state, setState] = useState<WorkflowState>(initialState);

  const nodes = [
    { id: 'user', label: 'User Prompt', icon: <UserIcon size={20} />, status: 'Ready' },
    { id: 'app', label: 'SensCoder App', icon: <AppIcon size={20} />, status: state === 'running' ? 'Processing' : 'Idle' },
    { id: 'llm', label: 'LLM Provider', icon: <BrainIcon size={20} />, status: state === 'running' ? 'Generating' : 'Idle' },
    { id: 'mcp', label: 'MCP Server', icon: <ServerIcon size={20} />, status: state === 'error' ? 'Error' : state === 'running' ? 'Running' : 'Idle' },
    { id: 'fs', label: 'Filesystem', icon: <FolderIcon size={20} />, status: 'Ready' },
  ];

  return (
    <Container>
      <Header>
        <Title>Workflow Status</Title>
        <Controls>
          <ControlButton active={state === 'idle'} onClick={() => setState('idle')}>
            Idle
          </ControlButton>
          <ControlButton active={state === 'running'} onClick={() => setState('running')}>
            Running
          </ControlButton>
          <ControlButton active={state === 'error'} onClick={() => setState('error')}>
            Error
          </ControlButton>
        </Controls>
      </Header>

      <WorkflowContainer>
        {nodes.map((node, index) => (
          <React.Fragment key={node.id}>
            <Node
              active={state === 'running' && index === 1}
              error={state === 'error' && index === 3}
            >
              <NodeIcon>{node.icon}</NodeIcon>
              <NodeLabel>{node.label}</NodeLabel>
              <NodeStatus>{node.status}</NodeStatus>
            </Node>
            {index < nodes.length - 1 && (
              <Connector active={state === 'running'}>
                {state === 'running' && <RunningDot position={50} />}
              </Connector>
            )}
          </React.Fragment>
        ))}
      </WorkflowContainer>
    </Container>
  );
};

export default WorkflowVisualizer;

// CSS animations
const styles = `
@keyframes glow {
  from {
    box-shadow: 0 0 20px rgba(79, 70, 229, 0.3);
  }
  to {
    box-shadow: 0 0 30px rgba(79, 70, 229, 0.6);
  }
}

@keyframes flow {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

@keyframes moveDot {
  0% {
    left: 0%;
  }
  20% {
    left: 25%;
  }
  40% {
    left: 50%;
  }
  60% {
    left: 75%;
  }
  80% {
    left: 100%;
  }
  100% {
    left: 0%;
  }
}
`;

// Inject styles
const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = styles;
document.head.appendChild(styleSheet);