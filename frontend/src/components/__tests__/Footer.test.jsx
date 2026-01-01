import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Footer from '../Footer';

// Wrapper pre komponenty s routerom
const RouterWrapper = ({ children }) => (
  <BrowserRouter>{children}</BrowserRouter>
);

describe('Footer', () => {
  it('renders footer component', () => {
    render(
      <RouterWrapper>
        <Footer />
      </RouterWrapper>
    );
    
    expect(screen.getByRole('contentinfo')).toBeInTheDocument();
  });

  it('displays legal documents links', () => {
    render(
      <RouterWrapper>
        <Footer />
      </RouterWrapper>
    );
    
    expect(screen.getByText('Všeobecné obchodné podmienky')).toBeInTheDocument();
    expect(screen.getByText('Zásady ochrany osobných údajov')).toBeInTheDocument();
    expect(screen.getByText('Vyhlásenie o odmietnutí zodpovednosti')).toBeInTheDocument();
    expect(screen.getByText('Cookie Policy')).toBeInTheDocument();
    expect(screen.getByText('Data Processing Agreement (B2B)')).toBeInTheDocument();
  });

  it('displays contact information', () => {
    render(
      <RouterWrapper>
        <Footer />
      </RouterWrapper>
    );
    
    expect(screen.getByText(/privacy@crossbordernexus.com/)).toBeInTheDocument();
  });

  it('displays copyright information', () => {
    render(
      <RouterWrapper>
        <Footer />
      </RouterWrapper>
    );
    
    const currentYear = new Date().getFullYear();
    expect(screen.getByText(new RegExp(currentYear.toString()))).toBeInTheDocument();
    expect(screen.getByText(/Iluminati Corp s\.r\.o\./i)).toBeInTheDocument();
  });

  it('has correct link attributes', () => {
    render(
      <RouterWrapper>
        <Footer />
      </RouterWrapper>
    );
    
    const vopLink = screen.getByText('Všeobecné obchodné podmienky');
    expect(vopLink.closest('a')).toHaveAttribute('href', '/vop');
  });
});

