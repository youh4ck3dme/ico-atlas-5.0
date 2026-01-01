import React, { useState, useEffect } from 'react';

/**
 * Custom hook pre Dark/Light mode toggle
 */
export const useTheme = () => {
  const [theme, setTheme] = useState(() => {
    // Načítať z localStorage alebo použiť systémové nastavenie
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    // Detekcia systémového preferencie
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  });

  useEffect(() => {
    // Aplikovať theme na document
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  return { theme, toggleTheme, setTheme };
};

