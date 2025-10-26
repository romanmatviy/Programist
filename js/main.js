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
  
  // Smooth scrolling and contact modal fallback
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') {
        e.preventDefault();
        return;
      }
      if (targetId === '#contact') {
        const contactEl = document.querySelector('#contact');
        if (!contactEl) {
          e.preventDefault();
          openContactModal();
          return;
        }
      }
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        window.scrollTo({ top: targetElement.offsetTop - 100, behavior: 'smooth' });
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
  
  // Contact form helpers
  function ensureStatusEl(form) {
    let status = form.querySelector('.form-status');
    if (!status) {
      status = document.createElement('div');
      status.className = 'form-status';
      form.appendChild(status);
    }
    return status;
  }

  function serializeForm(form) {
    const data = new FormData(form);
    data.append('source', window.location.href);
    return data;
  }

  async function submitContactForm(form) {
    const status = ensureStatusEl(form);
    const btn = form.querySelector('button[type="submit"]');
    const prevText = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Надсилання...'; }
    status.textContent = '';
    status.classList.remove('success','error');
    try {
      const targetUrl = 'https://bot.programist.top/api/contact.php'; 
      const res = await fetch(targetUrl, {
        method: 'POST',
        body: serializeForm(form)
      });
      const json = await res.json().catch(() => ({}));
      if (!res.ok || !json.ok) {
        throw new Error(json.error || 'Сталася помилка. Спробуйте пізніше.');
      }
      status.textContent = json.message || 'Повідомлення надіслано.';
      status.classList.add('success');
      form.reset();
    } catch (err) {
      status.textContent = err.message || 'Сталася помилка. Спробуйте пізніше.';
      status.classList.add('error');
    } finally {
      if (btn) { btn.disabled = false; btn.textContent = prevText; }
    }
  }

  function initContactForms() {
    document.querySelectorAll('form.contact-form').forEach(form => {
      if (form.dataset.enhanced === '1') return;
      form.dataset.enhanced = '1';
      form.addEventListener('submit', function(e) {
        e.preventDefault();
        submitContactForm(form);
      });
    });
  }

  // Modal contact form
  function ensureContactModal() {
    let overlay = document.querySelector('.modal-overlay[data-contact-modal]');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'modal-overlay';
      overlay.setAttribute('data-contact-modal', '');
      overlay.innerHTML = `
        <div class="modal" role="dialog" aria-modal="true" aria-labelledby="contact-modal-title">
          <div class="modal-header">
            <div id="contact-modal-title" class="modal-title">Зв'язатися</div>
            <button class="modal-close" aria-label="Закрити">×</button>
          </div>
          <div class="modal-body">
            <form class="contact-form">
              <div class="form-group">
                <label for="modal-name">Ім'я</label>
                <input type="text" id="modal-name" name="name" required>
              </div>
              <div class="form-group">
                <label for="modal-email">Email</label>
                <input type="email" id="modal-email" name="email" required>
              </div>
              <div class="form-group">
                <label for="modal-message">Повідомлення</label>
                <textarea id="modal-message" name="message" rows="5" required></textarea>
              </div>
              <button type="submit" class="btn">Надіслати</button>
            </form>
          </div>
        </div>`;
      document.body.appendChild(overlay);
      overlay.addEventListener('click', (e) => { if (e.target === overlay) closeContactModal(); });
      overlay.querySelector('.modal-close').addEventListener('click', closeContactModal);
      initContactForms();
    }
    return overlay;
  }

  function openContactModal() {
    const overlay = ensureContactModal();
    overlay.classList.add('active');
  }

  function closeContactModal() {
    const overlay = document.querySelector('.modal-overlay[data-contact-modal]');
    if (overlay) overlay.classList.remove('active');
  }

  // Initialize
  initContactForms();
  // Run Schema.org generator
  generateSchemaOrgData();
});