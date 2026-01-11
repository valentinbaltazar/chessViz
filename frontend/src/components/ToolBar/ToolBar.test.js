import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Toolbar from './ToolBar';

// Mock the API module
jest.mock('../../services/api', () => ({
  fetchUser: jest.fn(),
  checkUser: jest.fn(),
}));

import { fetchUser, checkUser } from '../../services/api';

describe('Toolbar Component', () => {
  const mockOnUserChange = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders username input', () => {
    render(<Toolbar onUserChange={mockOnUserChange} currentUser="river650" />);
    expect(screen.getByLabelText(/Chess.com Username/i)).toBeInTheDocument();
  });

  test('renders load player button', () => {
    render(<Toolbar onUserChange={mockOnUserChange} currentUser="river650" />);
    expect(screen.getByRole('button', { name: /Load Player/i })).toBeInTheDocument();
  });

  test('displays current user', () => {
    render(<Toolbar onUserChange={mockOnUserChange} currentUser="river650" />);
    expect(screen.getByText(/Current Player:/i)).toBeInTheDocument();
    expect(screen.getByText('river650')).toBeInTheDocument();
  });

  test('shows error when submitting empty username', async () => {
    render(<Toolbar onUserChange={mockOnUserChange} currentUser="river650" />);

    const submitButton = screen.getByRole('button', { name: /Load Player/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Please enter a username/i)).toBeInTheDocument();
    });
  });

  test('calls checkUser and onUserChange when user exists', async () => {
    checkUser.mockResolvedValue({ exists: true, username: 'testuser' });

    render(<Toolbar onUserChange={mockOnUserChange} currentUser="river650" />);

    const input = screen.getByLabelText(/Chess.com Username/i);
    fireEvent.change(input, { target: { value: 'testuser' } });

    const submitButton = screen.getByRole('button', { name: /Load Player/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(checkUser).toHaveBeenCalledWith('testuser');
      expect(mockOnUserChange).toHaveBeenCalledWith('testuser', true);
    });
  });

  test('fetches new user when they do not exist', async () => {
    checkUser.mockResolvedValue({ exists: false, username: 'newuser' });
    fetchUser.mockResolvedValue({ status: 'success', message: 'Downloaded games' });

    render(<Toolbar onUserChange={mockOnUserChange} currentUser="river650" />);

    const input = screen.getByLabelText(/Chess.com Username/i);
    fireEvent.change(input, { target: { value: 'newuser' } });

    const submitButton = screen.getByRole('button', { name: /Load Player/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(checkUser).toHaveBeenCalledWith('newuser');
      expect(fetchUser).toHaveBeenCalledWith('newuser');
    });
  });

  test('handles API error gracefully', async () => {
    checkUser.mockRejectedValue(new Error('Player not found'));

    render(<Toolbar onUserChange={mockOnUserChange} currentUser="river650" />);

    const input = screen.getByLabelText(/Chess.com Username/i);
    fireEvent.change(input, { target: { value: 'baduser' } });

    const submitButton = screen.getByRole('button', { name: /Load Player/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/Player not found/i)).toBeInTheDocument();
    });
  });
});
