import React, { useEffect } from 'react';

/**
 * Custom hook pre keyboard shortcuts
 * 
 * @param {Object} shortcuts - Objekt s mapovaním klávesových skratiek
 * @example
 * useKeyboardShortcuts({
 *   'Ctrl+K': () => setSearchFocused(true),
 *   'Escape': () => closeModal(),
 *   '/': (e) => { e.preventDefault(); focusSearch(); }
 * })
 */
export const useKeyboardShortcuts = (shortcuts) => {
  useEffect(() => {
    const handleKeyDown = (event) => {
      // Vytvoriť kľúč pre skratku (napr. "Ctrl+K", "Escape")
      const key = event.key;
      const ctrl = event.ctrlKey || event.metaKey; // Cmd na Mac
      const shift = event.shiftKey;
      const alt = event.altKey;

      // Skúsiť nájsť presnú skratku
      let shortcutKey = null;

      if (ctrl && shift) {
        shortcutKey = `Ctrl+Shift+${key}`;
      } else if (ctrl && alt) {
        shortcutKey = `Ctrl+Alt+${key}`;
      } else if (ctrl) {
        shortcutKey = `Ctrl+${key}`;
      } else if (shift) {
        shortcutKey = `Shift+${key}`;
      } else if (alt) {
        shortcutKey = `Alt+${key}`;
      } else {
        shortcutKey = key;
      }

      // Vyhľadať skratku v mape
      if (shortcuts[shortcutKey]) {
        event.preventDefault();
        shortcuts[shortcutKey](event);
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [shortcuts]);
};

/**
 * Predefinované skratky pre ILUMINATI SYSTEM
 */
export const SHORTCUTS = {
  SEARCH: 'Ctrl+K', // alebo Cmd+K na Mac
  ESCAPE: 'Escape',
  FOCUS_SEARCH: '/',
  EXPORT_CSV: 'Ctrl+E',
  EXPORT_PDF: 'Ctrl+P',
  TOGGLE_THEME: 'Ctrl+Shift+T',
  CLOSE_MODAL: 'Escape',
  ZOOM_IN: 'Ctrl+Plus',
  ZOOM_OUT: 'Ctrl+Minus',
  RESET_ZOOM: 'Ctrl+0',
};

export default useKeyboardShortcuts;

