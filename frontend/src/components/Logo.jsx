import React from 'react';
import { Globe, Sparkles } from 'lucide-react';

const Logo = ({ size = 'default', showText = true, className = '' }) => {
  const sizes = {
    small: { icon: 20, text: 'text-sm' },
    default: { icon: 48, text: 'text-2xl' },
    large: { icon: 64, text: 'text-4xl' },
    xl: { icon: 80, text: 'text-6xl' }
  };

  const config = sizes[size] || sizes.default;

  return (
    <div className={`flex flex-col items-center justify-center ${className}`}>
      {/* Logo Icon - Atlas s zemeguľou */}
      <div className="relative mb-2">
        {/* Outer golden ring */}
        <div className="absolute inset-0 rounded-full border-4 border-[#D4AF37]/30 blur-sm"></div>
        <div className="absolute inset-0 rounded-full border-2 border-[#D4AF37]/50"></div>
        
        {/* Central globe with Atlas figure */}
        <div 
          className={`relative ${size === 'small' ? 'w-12 h-12' : size === 'xl' ? 'w-24 h-24' : 'w-20 h-20'} rounded-full bg-gradient-to-br from-[#1a1a2e] via-[#16213e] to-[#0A0A0A] flex items-center justify-center border-2 border-[#D4AF37] shadow-[0_0_30px_rgba(212,175,55,0.6)]`}
          style={{
            background: 'radial-gradient(circle at 30% 30%, #D4AF37 0%, #1a1a2e 40%, #0A0A0A 100%)'
          }}
        >
          {/* Stars background */}
          {Array.from({ length: 8 }).map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full bg-[#FFD700] animate-pulse"
              style={{
                left: `${Math.random() * 80 + 10}%`,
                top: `${Math.random() * 80 + 10}%`,
                width: '2px',
                height: '2px',
                opacity: Math.random() * 0.8 + 0.2,
                animationDelay: `${Math.random() * 2}s`,
                animationDuration: `${Math.random() * 3 + 2}s`,
              }}
            />
          ))}
          
          {/* Globe icon */}
          <Globe 
            className="text-[#FFD700] relative z-10" 
            size={config.icon}
            style={{ filter: 'drop-shadow(0 0 10px #D4AF37)' }}
          />
          
          {/* Sparkles around */}
          <Sparkles 
            className="absolute -top-1 -right-1 text-[#FFD700] animate-spin" 
            size={16}
            style={{ 
              filter: 'drop-shadow(0 0 8px #D4AF37)',
              animationDuration: '3s'
            }} 
          />
          <Sparkles 
            className="absolute -bottom-1 -left-1 text-[#D4AF37] animate-pulse" 
            size={12}
            style={{ filter: 'drop-shadow(0 0 6px #FFD700)' }} 
          />
        </div>

        {/* Laurel wreaths (stylized) */}
        <div className="absolute -left-8 top-1/2 -translate-y-1/2 w-6 h-12 border-l-2 border-t-2 border-b-2 border-[#D4AF37]/40 rounded-l-full"></div>
        <div className="absolute -right-8 top-1/2 -translate-y-1/2 w-6 h-12 border-r-2 border-t-2 border-b-2 border-[#D4AF37]/40 rounded-r-full"></div>
      </div>

      {/* Text */}
      {showText && (
        <div className="text-center">
          <h1 className={`${config.text} font-bold bg-gradient-to-r from-[#D4AF37] via-[#FFD700] to-[#D4AF37] bg-clip-text text-transparent animate-gradient`}>
            ILUMINATE SYSTEM
          </h1>
          {size === 'large' || size === 'xl' ? (
            <p className="text-sm text-[#D4AF37]/70 mt-1 font-light">Cross-Border Intelligence Platform</p>
          ) : null}
        </div>
      )}
    </div>
  );
};

export default Logo;

