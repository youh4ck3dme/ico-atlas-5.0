import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const RateLimitIndicator = () => {
  const { isAuthenticated, token } = useAuth();
  const [limits, setLimits] = useState(null);
  const [usage, setUsage] = useState({ searches_used: 0, searches_per_day: 10 });

  useEffect(() => {
    if (isAuthenticated && token) {
      loadLimits();
    }
  }, [isAuthenticated, token]);

  const loadLimits = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/auth/tier/limits', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setLimits(data);
        // Simulácia usage (v produkcii by to bolo z backendu)
        setUsage({
          searches_used: 5, // Príklad
          searches_per_day: data.searches_per_day === -1 ? 999 : data.searches_per_day,
        });
      }
    } catch (error) {
      console.error('Error loading limits:', error);
    }
  };

  if (!isAuthenticated || !limits) {
    return null;
  }

  const percentage = limits.searches_per_day === -1 
    ? 0 
    : (usage.searches_used / limits.searches_per_day) * 100;
  const isWarning = percentage >= 80;
  const isError = percentage >= 100;

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-lg p-4 border border-white/20">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-white">Daily Searches</span>
        <span className={`text-sm font-semibold ${
          isError ? 'text-red-400' : isWarning ? 'text-yellow-400' : 'text-green-400'
        }`}>
          {limits.searches_per_day === -1 
            ? 'Unlimited' 
            : `${usage.searches_used} / ${limits.searches_per_day}`}
        </span>
      </div>
      {limits.searches_per_day !== -1 && (
        <>
          <div className="w-full bg-white/10 rounded-full h-2 mb-2">
            <div
              className={`h-2 rounded-full transition-all ${
                isError ? 'bg-red-500' : isWarning ? 'bg-yellow-500' : 'bg-green-500'
              }`}
              style={{ width: `${Math.min(percentage, 100)}%` }}
            ></div>
          </div>
          {isWarning && (
            <p className="text-xs text-yellow-300">
              {isError 
                ? 'Daily limit reached. Upgrade to continue searching.' 
                : 'Approaching daily limit. Consider upgrading.'}
            </p>
          )}
        </>
      )}
    </div>
  );
};

export default RateLimitIndicator;

