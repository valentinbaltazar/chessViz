import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DataType from './DataType';

describe('DataType Component', () => {
  const mockOnSubmit = jest.fn();
  const mockOnFilterChange = jest.fn();
  const defaultFilters = {
    timeClass: 'rapid',
    timeControl: '600',
    playerColor: 'white',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders analysis type dropdown', () => {
    render(
      <DataType
        onSubmit={mockOnSubmit}
        onFilterChange={mockOnFilterChange}
        filters={defaultFilters}
        disabled={false}
      />
    );

    expect(screen.getByLabelText(/Analysis Type/i)).toBeInTheDocument();
  });

  test('renders all plot options', () => {
    render(
      <DataType
        onSubmit={mockOnSubmit}
        onFilterChange={mockOnFilterChange}
        filters={defaultFilters}
        disabled={false}
      />
    );

    expect(screen.getByText('ELO Progression')).toBeInTheDocument();
    expect(screen.getByText('Wins by Color')).toBeInTheDocument();
    expect(screen.getByText('Opening Stats')).toBeInTheDocument();
    expect(screen.getByText('Time Analysis')).toBeInTheDocument();
    expect(screen.getByText('Opening Tree')).toBeInTheDocument();
  });

  test('renders time class filter', () => {
    render(
      <DataType
        onSubmit={mockOnSubmit}
        onFilterChange={mockOnFilterChange}
        filters={defaultFilters}
        disabled={false}
      />
    );

    expect(screen.getByLabelText(/Time Class/i)).toBeInTheDocument();
    expect(screen.getByText('Rapid')).toBeInTheDocument();
    expect(screen.getByText('Blitz')).toBeInTheDocument();
    expect(screen.getByText('Bullet')).toBeInTheDocument();
  });

  test('submit button is disabled when no plot selected', () => {
    render(
      <DataType
        onSubmit={mockOnSubmit}
        onFilterChange={mockOnFilterChange}
        filters={defaultFilters}
        disabled={false}
      />
    );

    const submitButton = screen.getByRole('button', { name: /Analyze/i });
    expect(submitButton).toBeDisabled();
  });

  test('submit button is disabled when component is disabled', () => {
    render(
      <DataType
        onSubmit={mockOnSubmit}
        onFilterChange={mockOnFilterChange}
        filters={defaultFilters}
        disabled={true}
      />
    );

    const submitButton = screen.getByRole('button', { name: /Analyze/i });
    expect(submitButton).toBeDisabled();
  });

  test('calls onSubmit when form is submitted with selection', () => {
    render(
      <DataType
        onSubmit={mockOnSubmit}
        onFilterChange={mockOnFilterChange}
        filters={defaultFilters}
        disabled={false}
      />
    );

    // Select an option
    const select = screen.getByLabelText(/Analysis Type/i);
    fireEvent.change(select, { target: { value: 'elo' } });

    // Submit
    const submitButton = screen.getByRole('button', { name: /Analyze/i });
    fireEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith('elo');
  });

  test('calls onFilterChange when time class changes', () => {
    render(
      <DataType
        onSubmit={mockOnSubmit}
        onFilterChange={mockOnFilterChange}
        filters={defaultFilters}
        disabled={false}
      />
    );

    const timeClassSelect = screen.getByLabelText(/Time Class/i);
    fireEvent.change(timeClassSelect, { target: { value: 'blitz' } });

    expect(mockOnFilterChange).toHaveBeenCalled();
  });
});
