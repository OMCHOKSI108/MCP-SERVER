import React from 'react';

export const UserIcon: React.FC<{ size?: number; color?: string }> = ({ size = 24, color = '#EDEDED' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export const AppIcon: React.FC<{ size?: number; color?: string }> = ({ size = 24, color = '#EDEDED' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke={color} strokeWidth="2"/>
    <line x1="8" y1="21" x2="16" y2="21" stroke={color} strokeWidth="2"/>
    <line x1="12" y1="17" x2="12" y2="21" stroke={color} strokeWidth="2"/>
  </svg>
);

export const BrainIcon: React.FC<{ size?: number; color?: string }> = ({ size = 24, color = '#EDEDED' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9.5 2C10.0523 2 10.5 2.44772 10.5 3V4.5C10.5 5.05228 10.0523 5.5 9.5 5.5C8.94772 5.5 8.5 5.05228 8.5 4.5V3C8.5 2.44772 8.94772 2 9.5 2Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M14.5 2C15.0523 2 15.5 2.44772 15.5 3V4.5C15.5 5.05228 15.0523 5.5 14.5 5.5C13.9477 5.5 13.5 5.05228 13.5 4.5V3C13.5 2.44772 13.9477 2 14.5 2Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M21 9.5C21 10.0523 20.5523 10.5 20 10.5H18.5C17.9477 10.5 17.5 10.0523 17.5 9.5C17.5 8.94772 17.9477 8.5 18.5 8.5H20C20.5523 8.5 21 8.94772 21 9.5Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M5.5 9.5C5.5 10.0523 5.05228 10.5 4.5 10.5H3C2.44772 10.5 2 10.0523 2 9.5C2 8.94772 2.44772 8.5 3 8.5H4.5C5.05228 8.5 5.5 8.94772 5.5 9.5Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 12C14.7614 12 17 9.76142 17 7C17 4.23858 14.7614 2 12 2C9.23858 2 7 4.23858 7 7C7 9.76142 9.23858 12 12 12Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 16V22" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M8 18H16" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export const ServerIcon: React.FC<{ size?: number; color?: string }> = ({ size = 24, color = '#EDEDED' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="2" y="2" width="20" height="8" rx="2" ry="2" stroke={color} strokeWidth="2"/>
    <rect x="2" y="14" width="20" height="8" rx="2" ry="2" stroke={color} strokeWidth="2"/>
    <line x1="6" y1="6" x2="6.01" y2="6" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <line x1="6" y1="18" x2="6.01" y2="18" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <line x1="10" y1="6" x2="10.01" y2="6" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <line x1="10" y1="18" x2="10.01" y2="18" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <line x1="14" y1="6" x2="14.01" y2="6" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <line x1="14" y1="18" x2="14.01" y2="18" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export const FolderIcon: React.FC<{ size?: number; color?: string }> = ({ size = 24, color = '#EDEDED' }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22 19C22 19.5304 21.7893 20.0391 21.4142 20.4142C21.0391 20.7893 20.5304 21 20 21H4C3.46957 21 2.96086 20.7893 2.58579 20.4142C2.21071 20.0391 2 19.5304 2 19V5C2 4.46957 2.21071 3.96086 2.58579 3.58579C2.96086 3.21071 3.46957 3 4 3H9L11 6H20C20.5304 6 21.0391 6.21071 21.4142 6.58579C21.7893 6.96086 22 7.46957 22 8V19Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export const LogoIcon: React.FC<{ size?: number }> = ({ size = 32 }) => (
  <svg width={size} height={size} viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="4" y="4" width="24" height="24" rx="4" fill="#4F46E5"/>
    <circle cx="16" cy="16" r="8" fill="white"/>
    <circle cx="16" cy="16" r="4" fill="#4F46E5"/>
  </svg>
);