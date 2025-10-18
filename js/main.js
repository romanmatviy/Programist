// Main JavaScript file

document.addEventListener('DOMContentLoaded', function() {
  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const navMenu = document.querySelector('nav ul');
  
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      navMenu.classList.toggle('active');
      mobileMenuToggle.classList.toggle('active');
    });
  }
  
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 100,
          behavior: 'smooth'
        });
      }
    });
  });
  
  // Lazy loading images
  if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });
    
    lazyImages.forEach(img => {
      imageObserver.observe(img);
    });
  }
  
  // Schema.org JSON-LD generator for SEO pages
  function generateSchemaOrgData() {
    const schemaElements = document.querySelectorAll('[data-schema]');
    
    schemaElements.forEach(element => {
      const schemaType = element.dataset.schema;
      let schemaData = {};
      
      switch(schemaType) {
        case 'LocalBusiness':
          schemaData = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": element.dataset.name || "Програміст Роман",
            "description": element.dataset.description || "Професійна розробка сайтів",
            "url": window.location.href,
            "address": {
              "@type": "PostalAddress",
              "addressLocality": element.dataset.city || "Львів",
              "addressRegion": element.dataset.region || "Львівська область",
              "addressCountry": "Україна"
            },
            "telephone": element.dataset.phone || "+380938800822",
            "email": element.dataset.email || "info@matviy.pp.ua"
          };
          break;
          
        case 'Service':
          schemaData = {
            "@context": "https://schema.org",
            "@type": "Service",
            "serviceType": element.dataset.serviceType || "Розробка сайтів",
            "provider": {
              "@type": "Person",
              "name": "Роман Матвій"
            },
            "areaServed": {
              "@type": "City",
              "name": element.dataset.city || "Львів"
            },
            "description": element.dataset.description || "Професійна розробка сайтів"
          };
          break;
          
        case 'BreadcrumbList':
          const breadcrumbs = document.querySelectorAll('.breadcrumbs a');
          const items = [];
          
          breadcrumbs.forEach((crumb, index) => {
            items.push({
              "@type": "ListItem",
              "position": index + 1,
              "name": crumb.textContent,
              "item": crumb.href
            });
          });
          
          schemaData = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": items
          };
          break;
      }
      
      if (Object.keys(schemaData).length > 0) {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(schemaData);
        document.head.appendChild(script);
      }
    });
  }
  
  // Run Schema.org generator
  generateSchemaOrgData();
});