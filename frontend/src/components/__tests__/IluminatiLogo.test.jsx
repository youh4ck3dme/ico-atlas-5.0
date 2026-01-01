import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import IluminatiLogo from '../IluminatiLogo';

describe('IluminatiLogo', () => {
  it('renders logo component', () => {
    const { container } = render(<IluminatiLogo />);
    const svg = container.querySelector('svg');
    expect(svg).toBeInTheDocument();
  });

  it('renders SVG with correct attributes', () => {
    const { container } = render(<IluminatiLogo size={50} />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('width', '50');
    expect(svg).toHaveAttribute('height', '50');
  });

  it('applies className prop correctly', () => {
    const { container } = render(<IluminatiLogo className="test-class" />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveClass('test-class');
  });

  it('renders with default size when not specified', () => {
    const { container } = render(<IluminatiLogo />);
    const svg = container.querySelector('svg');
    expect(svg).toHaveAttribute('width', '40');
    expect(svg).toHaveAttribute('height', '40');
  });
});

