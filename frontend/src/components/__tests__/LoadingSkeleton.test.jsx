import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import LoadingSkeleton from '../LoadingSkeleton';

describe('LoadingSkeleton', () => {
  it('renders default skeleton', () => {
    const { container } = render(<LoadingSkeleton />);
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
  });

  it('renders search skeleton when type is search', () => {
    const { container } = render(<LoadingSkeleton type="search" />);
    const skeleton = container.querySelector('.animate-pulse');
    expect(skeleton).toBeInTheDocument();
    expect(skeleton.querySelectorAll('.h-12').length).toBeGreaterThan(0);
  });

  it('renders card skeleton when type is card', () => {
    const { container } = render(<LoadingSkeleton type="card" />);
    expect(container.querySelector('.bg-white')).toBeInTheDocument();
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();
  });

  it('renders graph skeleton when type is graph', () => {
    render(<LoadingSkeleton type="graph" />);
    expect(screen.getByText('Načítavam graf...')).toBeInTheDocument();
  });

  it('renders different skeleton for each type', () => {
    const { rerender, container } = render(<LoadingSkeleton type="default" />);
    expect(container.querySelector('.animate-pulse')).toBeInTheDocument();

    rerender(<LoadingSkeleton type="search" />);
    expect(container.querySelectorAll('.h-12').length).toBeGreaterThan(0);

    rerender(<LoadingSkeleton type="card" />);
    expect(container.querySelector('.bg-white')).toBeInTheDocument();

    rerender(<LoadingSkeleton type="graph" />);
    expect(screen.getByText('Načítavam graf...')).toBeInTheDocument();
  });
});

