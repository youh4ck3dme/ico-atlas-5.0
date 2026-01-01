import { useState, useEffect } from 'react';

/**
 * Hook pre offline mode detection a handling
 */
export function useOffline() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [wasOffline, setWasOffline] = useState(false);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      if (wasOffline) {
        // Notifikácia o obnovení pripojenia
        console.log('✅ Pripojenie obnovené');
        setWasOffline(false);
      }
    };

    const handleOffline = () => {
      setIsOnline(false);
      setWasOffline(true);
      console.log('⚠️ Pripojenie stratené - offline mode');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [wasOffline]);

  return { isOnline, wasOffline };
}

/**
 * Hook pre offline queue management
 */
export function useOfflineQueue() {
  const [queue, setQueue] = useState([]);

  const addToQueue = (action) => {
    setQueue((prev) => [...prev, { ...action, timestamp: Date.now() }]);
  };

  const processQueue = async () => {
    if (queue.length === 0 || !navigator.onLine) return;

    const itemsToProcess = [...queue];
    setQueue([]);

    for (const item of itemsToProcess) {
      try {
        await item.execute();
      } catch (error) {
        console.error('Error processing queue item:', error);
        // Re-add to queue on failure
        setQueue((prev) => [...prev, item]);
      }
    }
  };

  useEffect(() => {
    if (navigator.onLine && queue.length > 0) {
      processQueue();
    }
  }, [navigator.onLine]);

  return { queue, addToQueue, processQueue };
}

