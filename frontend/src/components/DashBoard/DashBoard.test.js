import React from 'react';
import { render, screen } from '@testing-library/react';
import DashBoard from './DashBoard';

describe('DashBoard Component', () => {
  test('renders welcome message when no plot selected', () => {
    render(<DashBoard plotType={null} username="river650" />);
    expect(screen.getByText(/Welcome to ChessViz/i)).toBeInTheDocument();
  });

  test('renders feature list when no plot selected', () => {
    render(<DashBoard plotType={null} username="river650" />);
    expect(screen.getByText(/ELO Progression/i)).toBeInTheDocument();
    expect(screen.getByText(/Wins by Color/i)).toBeInTheDocument();
    expect(screen.getByText(/Opening Stats/i)).toBeInTheDocument();
    expect(screen.getByText(/Time Analysis/i)).toBeInTheDocument();
    expect(screen.getByText(/Opening Tree/i)).toBeInTheDocument();
  });

  test('renders ELO description when elo plot selected', () => {
    render(<DashBoard plotType="elo" username="river650" />);
    expect(screen.getByText(/ELO Progression/i)).toBeInTheDocument();
    expect(screen.getByText(/rating progression/i)).toBeInTheDocument();
  });

  test('renders wins description when wins plot selected', () => {
    render(<DashBoard plotType="wins" username="river650" />);
    expect(screen.getByText(/Wins by Color/i)).toBeInTheDocument();
    expect(screen.getByText(/monthly wins/i)).toBeInTheDocument();
  });

  test('renders openings description when openings plot selected', () => {
    render(<DashBoard plotType="openings" username="river650" />);
    expect(screen.getByText(/Opening Performance/i)).toBeInTheDocument();
    expect(screen.getByText(/win rate/i)).toBeInTheDocument();
  });

  test('renders time analysis description when time plot selected', () => {
    render(<DashBoard plotType="time" username="river650" />);
    expect(screen.getByText(/Time Analysis/i)).toBeInTheDocument();
    expect(screen.getByText(/hour of day/i)).toBeInTheDocument();
  });

  test('renders tree description when tree plot selected', () => {
    render(<DashBoard plotType="tree" username="river650" />);
    expect(screen.getByText(/Opening Repertoire Tree/i)).toBeInTheDocument();
    expect(screen.getByText(/move sequence/i)).toBeInTheDocument();
  });

  test('displays current username', () => {
    render(<DashBoard plotType="elo" username="river650" />);
    expect(screen.getByText('river650')).toBeInTheDocument();
  });
});
