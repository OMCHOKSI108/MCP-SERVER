export interface User {
  _id: string;
  name: string;
  email: string;
  avatar?: string;
  role?: 'user' | 'admin';
  isActive?: boolean;
  isBanned?: boolean;
  isBlocked?: boolean;
  dailyMessages?: number;
  lastActivity?: string;
  createdAt?: string;
}

export interface UserProfile {
  user: User;
  usage: {
    messageCount: number;
    dailyLimit: number;
    messagesToday: string;
  };
  settings: UserSettings;
}

export interface UserSettings {
  provider: 'gemini' | 'openai';
  useOwnKey: boolean;
  hasApiKey: boolean;
  theme: 'light' | 'dark';
  projectRoot?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
  message?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ChatResponse {
  response: string;
  usage: {
    messageCount: number;
    dailyLimit: number;
  };
}

export interface IntegrationStatus {
  providers: {
    gemini: {
      hasKey: boolean;
      isConfigured: boolean;
    };
    openai: {
      hasKey: boolean;
      isConfigured: boolean;
    };
  };
  mcp: {
    status: 'running' | 'stopped' | 'error';
    port: number | null;
    lastStarted: Date | null;
  };
  settings: UserSettings;
}

export interface MCPStartResponse {
  success: boolean;
  message: string;
  status: 'running' | 'stopped';
  port: number;
  configJson: any;
}

export interface ApiError {
  error: string;
}