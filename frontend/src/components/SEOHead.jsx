import { useEffect } from 'react';

/**
 * SEO Head komponenta pre dynamické meta tagy
 */
export const SEOHead = ({ 
  title = 'ILUMINATI SYSTEM - Transparentnosť pre slovenské podnikanie',
  description = 'Komplexná hĺbková analýza obchodných partnerov, vlastníckych štruktúr a finančného zdravia firiem v regióne strednej Európy (SK, CZ, PL, HU).',
  keywords = 'IČO, obchodný register, risk analýza, vlastnícke štruktúry, cross-border, V4, Slovensko, Česká republika, Poľsko, Maďarsko',
  ogImage = '/favicon.svg',
  canonical = '',
}) => {
  useEffect(() => {
    // Update document title
    document.title = title;

    // Update or create meta tags
    const updateMetaTag = (name, content, isProperty = false) => {
      const attribute = isProperty ? 'property' : 'name';
      let meta = document.querySelector(`meta[${attribute}="${name}"]`);
      
      if (!meta) {
        meta = document.createElement('meta');
        meta.setAttribute(attribute, name);
        document.head.appendChild(meta);
      }
      meta.setAttribute('content', content);
    };

    // Basic meta tags
    updateMetaTag('description', description);
    updateMetaTag('keywords', keywords);
    
    // Open Graph tags
    updateMetaTag('og:title', title, true);
    updateMetaTag('og:description', description, true);
    updateMetaTag('og:image', ogImage, true);
    updateMetaTag('og:type', 'website', true);
    updateMetaTag('og:url', canonical || window.location.href, true);
    updateMetaTag('og:site_name', 'ILUMINATI SYSTEM', true);
    
    // Twitter Card tags
    updateMetaTag('twitter:card', 'summary_large_image');
    updateMetaTag('twitter:title', title);
    updateMetaTag('twitter:description', description);
    updateMetaTag('twitter:image', ogImage);
    
    // Canonical URL
    if (canonical) {
      let link = document.querySelector('link[rel="canonical"]');
      if (!link) {
        link = document.createElement('link');
        link.setAttribute('rel', 'canonical');
        document.head.appendChild(link);
      }
      link.setAttribute('href', canonical);
    }

    // Language
    updateMetaTag('language', 'sk');
    updateMetaTag('robots', 'index, follow');
    
    // Author
    updateMetaTag('author', 'ILUMINATI SYSTEM');
    
    // Viewport (ak nie je už nastavený)
    let viewport = document.querySelector('meta[name="viewport"]');
    if (!viewport) {
      viewport = document.createElement('meta');
      viewport.setAttribute('name', 'viewport');
      viewport.setAttribute('content', 'width=device-width, initial-scale=1.0');
      document.head.appendChild(viewport);
    }
  }, [title, description, keywords, ogImage, canonical]);

  return null; // Tento komponent nič nerenderuje
};

export default SEOHead;

