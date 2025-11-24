import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import { User } from '../types';
import { authApi } from '../api';

interface ProfileProps {
  user: User | null;
}

const Container = styled.div`
  max-width: 600px;
  margin: 0 auto;
  padding: 24px;
`;

const Header = styled.div`
  text-align: center;
  margin-bottom: 48px;
`;

const AvatarContainer = styled.div`
  position: relative;
  display: inline-block;
  margin-bottom: 24px;
`;

const Avatar = styled.img`
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
`;

const AvatarPlaceholder = styled.div`
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #4F46E5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: 600;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
`;

const FileInput = styled.input`
  position: absolute;
  bottom: 0;
  right: 0;
  opacity: 0;
  width: 40px;
  height: 40px;
  cursor: pointer;
`;

const EditButton = styled.label`
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  background: #4F46E5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 12px 24px rgba(0,0,0,0.1);
  }
`;

const Title = styled.h1`
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
  color: #EDEDED;
`;

const Subtitle = styled.p`
  font-size: 14px;
  color: #9CA3AF;
  line-height: 1.6;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 24px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Label = styled.label`
  font-size: 14px;
  font-weight: 500;
  color: #EDEDED;
`;

const Input = styled.input`
  padding: 12px 16px;
  background: #111827;
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

const Textarea = styled.textarea`
  padding: 12px 16px;
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #EDEDED;
  font-size: 14px;
  min-height: 100px;
  resize: vertical;
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

const ButtonGroup = styled.div`
  display: flex;
  gap: 12px;
  margin-top: 24px;
`;

const Button = styled.button<{ variant?: 'primary' | 'danger' }>`
  padding: 12px 24px;
  background: ${props => props.variant === 'danger' ? '#EF4444' : '#4F46E5'};
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  height: 44px;

  &:hover {
    background: ${props => props.variant === 'danger' ? '#DC2626' : '#6366F1'};
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

const Profile: React.FC<ProfileProps> = ({ user }) => {
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [bio, setBio] = useState(user?.bio || '');
  const [profilePhoto, setProfilePhoto] = useState(user?.profilePhoto || '');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setProfilePhoto(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      await authApi.update({ name, bio, profilePhoto });
      alert('Profile updated');
      setEditing(false);
    } catch (error) {
      alert('Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      setLoading(true);
      try {
        await authApi.delete();
        localStorage.removeItem('token');
        navigate('/login');
      } catch (error) {
        alert('Failed to delete account');
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Container>
      <Header>
        <AvatarContainer>
          {profilePhoto ? (
            <Avatar src={profilePhoto} alt="Profile" />
          ) : (
            <AvatarPlaceholder>
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </AvatarPlaceholder>
          )}
          {editing && (
            <>
              <FileInput
                type="file"
                accept="image/*"
                onChange={handlePhotoChange}
                id="photo-upload"
              />
              <EditButton htmlFor="photo-upload">
                ✏️
              </EditButton>
            </>
          )}
        </AvatarContainer>
        <Title>{editing ? 'Edit Profile' : 'Profile'}</Title>
        <Subtitle>Manage your SensCoder account settings</Subtitle>
      </Header>

      {editing ? (
        <Form onSubmit={(e) => { e.preventDefault(); handleSave(); }}>
          <FormGroup>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </FormGroup>
          <FormGroup>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled
            />
          </FormGroup>
          <FormGroup>
            <Label htmlFor="bio">Bio</Label>
            <Textarea
              id="bio"
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="Tell us about yourself..."
            />
          </FormGroup>
          <ButtonGroup>
            <Button type="submit" disabled={loading}>
              {loading ? 'Saving...' : 'Save Changes'}
            </Button>
            <Button type="button" onClick={() => setEditing(false)}>
              Cancel
            </Button>
          </ButtonGroup>
        </Form>
      ) : (
        <div>
          <FormGroup>
            <Label>Name</Label>
            <p style={{ color: '#9CA3AF', lineHeight: '1.6' }}>{user?.name}</p>
          </FormGroup>
          <FormGroup>
            <Label>Email</Label>
            <p style={{ color: '#9CA3AF', lineHeight: '1.6' }}>{user?.email}</p>
          </FormGroup>
          <FormGroup>
            <Label>Bio</Label>
            <p style={{ color: '#9CA3AF', lineHeight: '1.6' }}>{user?.bio || 'No bio added'}</p>
          </FormGroup>
          <ButtonGroup>
            <Button onClick={() => setEditing(true)}>Edit Profile</Button>
            <Button variant="danger" onClick={handleDelete} disabled={loading}>
              {loading ? 'Deleting...' : 'Delete Account'}
            </Button>
          </ButtonGroup>
        </div>
      )}
    </Container>
  );
};

export default Profile;