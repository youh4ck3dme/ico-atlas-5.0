import React from 'react';

/**
 * Loading Skeleton komponenta pre lepšiu UX
 */
const LoadingSkeleton = ({ type = 'default' }) => {
  if (type === 'search') {
    return (
      <div className="animate-pulse">
        <div className="h-12 bg-slate-200 rounded-lg mb-4"></div>
        <div className="h-12 bg-slate-200 rounded-lg"></div>
      </div>
    );
  }

  if (type === 'card') {
    return (
      <div className="bg-white rounded-lg shadow-corp border border-slate-200 p-6 animate-pulse">
        <div className="h-6 bg-slate-200 rounded w-3/4 mb-4"></div>
        <div className="h-4 bg-slate-200 rounded w-1/2 mb-2"></div>
        <div className="h-4 bg-slate-200 rounded w-2/3"></div>
      </div>
    );
  }

  if (type === 'graph') {
    return (
      <div className="bg-white rounded-lg shadow-corp border border-slate-200 p-8 animate-pulse">
        <div className="h-6 bg-slate-200 rounded w-1/4 mb-6"></div>
        <div className="h-96 bg-slate-100 rounded-lg flex items-center justify-center">
          <div className="text-slate-400 text-sm">Načítavam graf...</div>
        </div>
      </div>
    );
  }

  // Default skeleton
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-4 bg-slate-200 rounded w-3/4"></div>
      <div className="h-4 bg-slate-200 rounded w-1/2"></div>
      <div className="h-4 bg-slate-200 rounded w-5/6"></div>
    </div>
  );
};

export default LoadingSkeleton;

