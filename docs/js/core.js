/**
 * =============================================================================
 * I.S.D.I — Isla Digital | Core Module
 * =============================================================================
 * Hardware detection, theme management, cursor follower, lazy loading,
 * navigation, and scroll animations.
 * =============================================================================
 */

'use strict';

/* =============================================================================
 * Hardware Detection Module
 * Detects GPU capability to toggle high-end vs low-end rendering modes.
 * =========================================================================== */
const HardwareDetector = (() => {
  /**
   * Advanced GPU and System detection.
   * Returns tiered performance classification: 'ultra' | 'high' | 'med' | 'low'.
   */
  function analyzeSystem() {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

      if (!gl) return 'low';

      // Advanced GPU Info
      const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
      let gpuName = '';
      if (debugInfo) {
        gpuName = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL).toLowerCase();
      }

      const cores = navigator.hardwareConcurrency || 4;
      const memory = navigator.deviceMemory || 4;
      const isMobile = /Android|iPhone|iPad|iPod|webOS|BlackBerry|Opera Mini|IEMobile/i.test(navigator.userAgent);
      const isApple = gpuName.includes('apple') || gpuName.includes('metal');
      const isHighEndGPU = gpuName.includes('nvidia') || gpuName.includes('radeon') || gpuName.includes('geforce') || gpuName.includes('rtx');
      const isUHD600 = gpuName.includes('uhd 600') || gpuName.includes('uhd 605'); // Specifically requested
      const isIntegrated = (gpuName.includes('intel') || gpuName.includes('iris') || gpuName.includes('uhd') || gpuName.includes('graphics')) && !isUHD600;

      // Accessibility Check
      const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (prefersReducedMotion) return 'med';

      // TIER: ULTRA (All Desktop/Laptop systems and High-end Dedicated GPUs)
      if (!isMobile || isHighEndGPU) {
        return 'ultra';
      }

      // TIER: HIGH (Modern Apple Silicon Mobile or High-end Flagship Phones)
      if (isApple || (isMobile && cores >= 8 && memory >= 6)) {
        return 'high';
      }

      // TIER: MED (Modern Mid-range Phones)
      if (isIntegrated || (isMobile && cores >= 4 && memory >= 4)) {
        return 'med';
      }

      // TIER: LOW (Ancient hardware / Battery Saver)
      return 'low';
    } catch (e) {
      console.warn('[HW Detect] Advanced detection failed:', e);
      return 'high';
    }
  }

  /**
  /**
  /**
   * Applies the performance tier to the DOM and CSS.
   * Can be forced with a direct tier string (e.g., 'ultra' for admin mode).
   */
  function apply(forcedTier = null) {
    // Check local admin state from SecurityManager
    const isLocalAdmin = (typeof SecurityManager !== 'undefined' && SecurityManager.isAdminMode());
    const tier = forcedTier || (isLocalAdmin ? 'ultra' : analyzeSystem());

    const body = document.body;
    const staticBg = document.querySelector('.static-bg');
    const particleCanvas = document.getElementById('particle-canvas');

    // Clean up old classes
    body.classList.remove('ultra-end', 'high-end', 'med-end', 'low-end');

    // Apply new class
    body.classList.add(`${tier}-end`);
    body.dataset.gpuTier = tier;
    console.log(`%c[HW Detect] Render Engine: ${tier.toUpperCase()}`, "background: #7B2FFF; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: bold;");

    // Update performance label
    const dot = document.querySelector('.perf-pill__dot');
    const label = document.querySelector('.perf-pill__label');
    if (dot && label) {
      const colors = { ultra: '#00F0FF', high: '#28CA41', med: '#FFBD2E', low: '#FF5F57' };
      dot.style.backgroundColor = colors[tier];
      label.textContent = `GPU: ${tier.toUpperCase()}`;

      dot.className = 'perf-pill__dot';
      dot.classList.add(`perf-pill__dot--${tier === 'ultra' || tier === 'high' ? 'high' : 'low'}`);
    }

    // Effect management: Ultra/High use Particles, others use Static
    if (tier === 'ultra' || tier === 'high') {
      if (typeof ParticleSystem !== 'undefined') {
        ParticleSystem.init(tier);
        if (particleCanvas) particleCanvas.classList.add('active');
        // Smooth transition: remove static bg after particles are ready
        setTimeout(() => {
          if (staticBg) staticBg.classList.remove('active');
        }, 1500); 
      }
    } else {
      // For low/med, keep static bg and stop particles
      if (staticBg) staticBg.classList.add('active');
      if (particleCanvas) particleCanvas.classList.remove('active');
      if (typeof ParticleSystem !== 'undefined' && ParticleSystem.stop) ParticleSystem.stop();
    }
  }

  return { apply };
})();

/* =============================================================================
 * Theme Manager
 * Reads prefers-color-scheme and provides manual toggle.
 * Persists choice in localStorage.
 * =========================================================================== */
const ThemeManager = (() => {
  const STORAGE_KEY = 'isdi-theme';

  function getSystemTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function getSavedTheme() {
    return localStorage.getItem(STORAGE_KEY);
  }

  function apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);

    // Update toggle button icon
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.innerHTML = theme === 'dark'
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
      toggleBtn.setAttribute('aria-label',
        theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
    }

    // If particles are active, update their color
    if (typeof ParticleSystem !== 'undefined' && ParticleSystem.updateColors) {
      ParticleSystem.updateColors(theme);
    }
  }

  function toggle() {
    const current = document.documentElement.getAttribute('data-theme') || getSystemTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    apply(next);
  }

  function init() {
    const saved = getSavedTheme();
    const theme = saved || getSystemTheme();
    apply(theme);

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!getSavedTheme()) {
        apply(e.matches ? 'dark' : 'light');
      }
    });

    // Bind toggle button
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggle);
    }
  }

  return { init, toggle, apply };
})();

/* =============================================================================
 * Cursor Follower
 * Intelligent cursor that transforms into a magnifier over
 * cybersecurity/hardware sections.
 * =========================================================================== */
const CursorFollower = (() => {
  let cursor = null;
  let mouseX = 0, mouseY = 0;
  let cursorX = 0, cursorY = 0;
  let animFrame = null;

  function init() {
    // Skip on touch devices
    if (window.matchMedia('(hover: none) and (pointer: coarse)').matches) return;

    cursor = document.querySelector('.cursor-follower');
    if (!cursor) return;

    document.addEventListener('mousemove', onMouseMove, { passive: true });
    document.addEventListener('mousedown', () => cursor.classList.add('clicking'));
    document.addEventListener('mouseup', () => cursor.classList.remove('clicking'));

    // Show cursor after mouse movement
    document.addEventListener('mousemove', () => {
      cursor.classList.add('visible');
    }, { once: true });

    animate();
  }

  function onMouseMove(e) {
    mouseX = e.clientX;
    mouseY = e.clientY;

    // Check what we're hovering over
    const target = e.target.closest('[data-cursor]');
    if (target && target.dataset.cursor === 'magnifier') {
      cursor.classList.add('magnifier');
    } else {
      cursor.classList.remove('magnifier');
    }

    // Interactive custom cursor state (hovering over clicking elements)
    const isInteractive = e.target.closest('a, button, input, textarea, select, details, [role="button"], .tree-item');
    if (isInteractive) {
      cursor.classList.add('interactive');
    } else {
      cursor.classList.remove('interactive');
    }
  }

  function animate() {
    // Smooth interpolation (lerp)
    const speed = 0.15;
    cursorX += (mouseX - cursorX) * speed;
    cursorY += (mouseY - cursorY) * speed;

    if (cursor) {
      cursor.style.setProperty('--cx', `${cursorX}px`);
      cursor.style.setProperty('--cy', `${cursorY}px`);
    }

    animFrame = requestAnimationFrame(animate);
  }

  function destroy() {
    if (animFrame) cancelAnimationFrame(animFrame);
    document.removeEventListener('mousemove', onMouseMove);
  }

  return { init, destroy };
})();

/* =============================================================================
 * Navigation Controller
 * Handles scroll effects, mobile menu, and page transitions.
 * =========================================================================== */
const Navigation = (() => {
  function init() {
    const nav = document.querySelector('.nav');
    const hamburger = document.querySelector('.nav__hamburger');
    const links = document.querySelector('.nav__links');
    const overlay = document.querySelector('.mobile-overlay');

    if (!nav) return;

    // Scroll effect
    let lastScroll = 0;
    const onScroll = () => {
      const scrollY = window.scrollY;
      if (scrollY > 50) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
      lastScroll = scrollY;
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // Initial check

    // Mobile menu toggle
    if (hamburger && links) {
      hamburger.addEventListener('click', () => {
        const isOpen = links.classList.contains('open');
        links.classList.toggle('open');
        hamburger.classList.toggle('open');
        if (overlay) overlay.classList.toggle('active');
        document.body.style.overflow = isOpen ? '' : 'hidden';
      });

      // Close on overlay click
      if (overlay) {
        overlay.addEventListener('click', () => {
          links.classList.remove('open');
          hamburger.classList.remove('open');
          overlay.classList.remove('active');
          document.body.style.overflow = '';
        });
      }

      // Close mobile menu on link click
      links.querySelectorAll('.nav__link').forEach(link => {
        link.addEventListener('click', () => {
          links.classList.remove('open');
          hamburger.classList.remove('open');
          if (overlay) overlay.classList.remove('active');
          document.body.style.overflow = '';
        });
      });
    }

    // Highlight active link
    highlightActiveLink();

    // Page transition effect
    initPageTransitions();
  }

  function highlightActiveLink() {
    const path = window.location.pathname;
    const filename = path.split('/').pop() || 'index.html';

    document.querySelectorAll('.nav__link').forEach(link => {
      const href = link.getAttribute('href');
      if (href === filename ||
        (filename === '' && href === 'index.html') ||
        (filename === 'index.html' && href === 'index.html')) {
        link.classList.add('active');
      }
    });
  }

  function initPageTransitions() {
    const transition = document.querySelector('.page-transition');
    if (!transition) return;

    // Intercept internal links
    document.querySelectorAll('a[href$=".html"]').forEach(link => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('http') || href.startsWith('#')) return;

      link.addEventListener('click', (e) => {
        e.preventDefault();
        transition.classList.add('active');
        setTimeout(() => {
          window.location.href = href;
        }, 400);
      });
    });

    // Fade in on page load
    window.addEventListener('load', () => {
      transition.classList.remove('active');
    });
  }

  return { init };
})();

/* =============================================================================
 * Scroll Reveal Animations
 * Uses IntersectionObserver to trigger CSS-based reveal animations.
 * =========================================================================== */
const ScrollAnimations = (() => {
  function init() {
    const revealElements = document.querySelectorAll(
      '.reveal, .reveal-left, .reveal-right, .reveal-scale'
    );

    if (!revealElements.length) return;

    // Respect reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      revealElements.forEach(el => el.classList.add('visible'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -60px 0px' }
    );

    revealElements.forEach(el => observer.observe(el));
  }

  return { init };
})();

/* =============================================================================
 * Lazy Loading
 * Implements native lazy loading with fallback IntersectionObserver.
 * =========================================================================== */
const LazyLoader = (() => {
  function init() {
    // Native lazy loading for images
    document.querySelectorAll('img[data-src]').forEach(img => {
      img.setAttribute('loading', 'lazy');
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              const src = img.dataset.src;
              if (src) {
                img.src = src;
                img.removeAttribute('data-src');
              }
              observer.unobserve(img);
            }
          });
        },
        { rootMargin: '200px' }
      );
      observer.observe(img);
    });

    // Lazy load sections
    document.querySelectorAll('[data-lazy-section]').forEach(section => {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              section.classList.add('loaded');
              observer.unobserve(section);
            }
          });
        },
        { rootMargin: '100px' }
      );
      observer.observe(section);
    });
  }

  return { init };
})();

/* =============================================================================
 * Loading Screen
 * Handles the initial loading state transition.
 * =========================================================================== */
const LoadingScreen = (() => {
  const phrases = [
    'Analizando arquitectura de hardware...',
    'Sincronizando modelos de datos...',
    'Estableciendo protocolos de seguridad...',
    'Optimizando núcleo de renderizado...',
    'Verificando integridad de archivos...',
    'Cargando módulos de ciberseguridad...'
  ];

  function init() {
    const loader = document.querySelector('.loader');
    const loaderText = document.querySelector('.loader__text');
    if (!loader) return;

    // Cycle messages
    let i = 0;
    const interval = setInterval(() => {
      if (loaderText) {
        loaderText.textContent = phrases[i % phrases.length];
        i++;
      }
    }, 800);

    window.addEventListener('load', () => {
      setTimeout(() => {
        clearInterval(interval);
        if (loaderText) loaderText.textContent = 'Sistema Listo';

        setTimeout(() => {
          loader.classList.add('hidden');
          // Remove from DOM after transition
          setTimeout(() => loader.remove(), 600);
        }, 300);
      }, 1200);
    });

    // Fallback
    setTimeout(() => {
      clearInterval(interval);
      if (loader && !loader.classList.contains('hidden')) {
        loader.classList.add('hidden');
        setTimeout(() => loader.remove(), 600);
      }
    }, 6000);
  }

  return { init };
})();

/* =============================================================================
 * Smooth Scroll for Anchor Links
 * =========================================================================== */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

/* =============================================================================
 * Counter Animation (Stats)
 * =========================================================================== */
function initCounters() {
  const counters = document.querySelectorAll('[data-counter]');
  if (!counters.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  counters.forEach(counter => observer.observe(counter));
}

function animateCounter(el) {
  const target = parseInt(el.dataset.counter, 10);
  const suffix = el.dataset.suffix || '';
  const duration = 2000;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out quart
    const eased = 1 - Math.pow(1 - progress, 4);
    const current = Math.floor(eased * target);
    el.textContent = current + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = target + suffix;
    }
  }

  requestAnimationFrame(update);
}

/* =============================================================================
 * Typing Effect
 * =========================================================================== */
function createTypingEffect(element, texts, speed = 80, pause = 2000) {
  if (!element) return;

  let textIndex = 0;
  let charIndex = 0;
  let isDeleting = false;

  function type() {
    const currentText = texts[textIndex];

    if (isDeleting) {
      element.textContent = currentText.substring(0, charIndex - 1);
      charIndex--;
    } else {
      element.textContent = currentText.substring(0, charIndex + 1);
      charIndex++;
    }

    let timeout = isDeleting ? speed / 2 : speed;

    if (!isDeleting && charIndex === currentText.length) {
      timeout = pause;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      textIndex = (textIndex + 1) % texts.length;
      timeout = speed;
    }

    setTimeout(type, timeout);
  }

  type();
}

/* =============================================================================
 * Security Manager
 * Prevents content copying, context menu, and keyboard shortcuts.
 * =========================================================================== */
const SecurityManager = (() => {
  let _isLocalAdmin = false;
  try {
    _isLocalAdmin = sessionStorage.getItem('isdi_admin') === 'true';
  } catch (e) { }

  // Public accessor for other modules to know if we are in admin mode
  function isAdminMode() { return _isLocalAdmin; }

  let trapInterval;
  let scrubbingInterval;
  let contentBackup = null;

  function init() {
    // 0. RESET SECURITY STATE (To ensure manual reload or new session clears old locks)
    try { sessionStorage.removeItem('isdi_locking'); } catch (e) { }

    let buffer = '';
    document.addEventListener('keydown', e => {
      buffer += e.key.toLowerCase();
      if (buffer.endsWith('aidmin')) {
        try { sessionStorage.setItem('isdi_admin', 'true'); } catch (e) { }
        console.log("%c[I.S.D.I] ACCESO CONCEDIDO — REINICIANDO CON PERMISOS MAESTROS", "color: #00FF00; font-weight: bold; font-size: 16px;");
        location.reload(); // Reload for perfect rendering
      }
      if (buffer.length > 10) buffer = buffer.substring(1);
    });

    if (_isLocalAdmin) {
      console.log("%c[I.S.D.I] MODO ADMINISTRADOR ACTIVO — SEGURIDAD DESACTIVADA", "color: #00FF00; font-weight: bold;");
      // PURGE SESSION: So that a manual reload (F5) locks the site again
      try { sessionStorage.removeItem('isdi_admin'); } catch (e) { }

      HardwareDetector.apply('ultra');
      return;
    }

    // 2. High-Frequency DevTools Detection & Persistent Scrubbing
    detectDevTools();
    window.addEventListener('resize', detectDevTools);

    scrubbingInterval = setInterval(() => {
      if (!isAdmin) {
        detectDevTools();
      }
    }, 100);

    // 3. Disable Context Menu Silently
    document.addEventListener('contextmenu', e => {
      if (isAdmin) return;
      e.preventDefault();
      // No showWarning() here, just block it.
    });

    // 4. Disable Shortcuts
    document.addEventListener('keydown', e => {
      if (isAdmin) return;
      const key = e.key.toLowerCase();
      if (
        (e.ctrlKey && (key === 'c' || key === 'x' || key === 'u' || key === 's')) ||
        (e.ctrlKey && e.shiftKey && (key === 'i' || key === 'j' || key === 'c')) ||
        (key === 'f12')
      ) {
        e.preventDefault();
        triggerLock(); // Trigger physical wipe and show warning
        return false;
      }
    });

    // 5. Advanced Anti-Source Debugger Trap (Freezes Sources tab)
    trapInterval = setInterval(() => {
      if (!isAdmin) {
        (function () {
          (function a() {
            try {
              (function b(i) {
                if (("" + i / i).length !== 1 || i % 20 === 0) {
                  (function () { }).constructor("debugger")();
                } else {
                  (function () { }).constructor("debugger")();
                }
                b(++i);
              })(0);
            } catch (e) { }
          })();
        })();

        // Secondary aggressive trap
        const t = function () {
          const x = new Function("debugger");
          x();
        };
        setTimeout(t, 20);
      }
    }, 100);
  }

  function detectDevTools() {
    if (_isLocalAdmin) return;
    
    // Total Sensitivity Threshold
    const threshold = 100;
    const isDetected = (window.outerWidth - window.innerWidth > threshold) || 
                       (window.outerHeight - window.innerHeight > threshold);

    if (isDetected) {
      // NUCLEAR PURGE: Redirecting to a standalone file unloads original sources from the browser memory.
      if (!sessionStorage.getItem('isdi_locking')) {
        try { sessionStorage.setItem('isdi_locking', 'true'); } catch(e) {}
        
        // Kill execution
        window.stop();
        
        // Clear DOM context first
        document.documentElement.innerHTML = '';
        
        // Attempt forced redirection (most reliable for Sources purge)
        try {
            window.location.replace('security-lock.html');
        } catch(e) {
            // Fallback for browsers with strict file:/// origin policies
            window.open('security-lock.html', '_self');
        }

        throw new Error("Security Protocol Active: Sources Purged.");
      }
    }
  }

  function triggerLock() {
    if (_isLocalAdmin) return;
    // ABSOLUTE WIPE: If any inspector-like dimension is detected, wipe the entire HTML
    if (document.body && !contentBackup) {
      contentBackup = Array.from(document.body.children);
      // Wipe the entire document!
      document.documentElement.innerHTML = `
          <head>
            <title>Acceso Restringido</title>
            <style>
              body { background: #000; margin:0; display: flex; align-items: center; justify-content: center; height: 100vh; font-family: monospace; color: #ff0000; text-align: center; }
              .overlay { border: 2px solid #7B2FFF; padding: 40px; border-radius: 20px; background: rgba(0,0,0,0.8); box-shadow: 0 0 100px rgba(123, 47, 255, 0.5); }
              .btn { background: #7B2FFF; color: #000; border: none; padding: 14px 40px; border-radius: 10px; font-weight: 800; text-transform: uppercase; cursor: pointer; margin-top: 30px; }
            </style>
          </head>
          <body>
            <div class="overlay">
              <h1 style="font-size: 3rem; margin-bottom: 20px;">!</h1>
              <h2 style="font-size: 1.5rem; text-transform: uppercase; letter-spacing: 2px;">Acceso Restringido</h2>
              <p style="color: #ccc; max-width: 500px; line-height: 1.6;">El sistema ha detectado un intento de interacción externa. Operación bloqueada por protocolos de seguridad.</p>
              <button class="btn" onclick="location.reload()">Recargar Página</button>
              <p style="font-size: 0.7rem; color: #7B2FFF; margin-top: 30px; opacity: 0.6;">ESTADO: BLOQUEO ABSOLUTO DE DOM</p>
            </div>
          </body>
        `;
      throw new Error("Security Protocol Active: Inspection Blocked.");
    }
  }

  function showWarning() {
    if (_isLocalAdmin) return;
    let overlay = document.querySelector('.security-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'security-overlay';
      overlay.innerHTML = `
        <div class="security-overlay__icon">!</div>
        <h2 class="security-overlay__title">Acceso Restringido: Acción No Autorizada</h2>
        <p class="security-overlay__msg">
          El sistema ha detectado un intento de interacción externa o guardado de código. 
          Por políticas de seguridad y protección de arquitectura, estas funciones están deshabilitadas.
        </p>
        <button class="security-overlay__btn" onclick="location.reload()">Recargar Página</button>
        <div class="security-overlay__footer">ESTADO: OPERACIÓN BLOQUEADA</div>
      `;
      document.body.appendChild(overlay);
    }
    overlay.classList.add('active');
  }

  function sanitize(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  return { init, isAdminMode, sanitize };
})();

/* =============================================================================
 * Error Monitor
 * Silent logging and recovery.
 * =========================================================================== */
const ErrorMonitor = (() => {
  function init() {
    window.onerror = (msg, url, lineNo, columnNo, error) => {
      // Suppress Security-related "errors" or browser-origin noise
      if (msg && (
        msg.includes('Security Protocol') ||
        msg.includes('Script error') ||
        msg.includes('Unsafe attempt') ||
        msg.includes('unique security origins')
      )) {
        return true;
      }
      console.error(`[ISDI Error] ${msg} at ${lineNo}:${columnNo}`);
      return true; // Prevent the firing of the default event handler
    };

    window.onunhandledrejection = (event) => {
      const reason = event.reason ? event.reason.toString() : '';
      if (
        reason.includes('Security Protocol') ||
        reason.includes('Script error') ||
        reason.includes('Unsafe attempt')
      ) {
        event.preventDefault();
        return;
      }
      console.error(`[ISDI Async Error] ${reason}`);
    };
  }
  return { init };
})();

/* =============================================================================
 * Initialize Everything on DOM Ready
 * =========================================================================== */
document.addEventListener('DOMContentLoaded', () => {
  // 0. Error Monitor
  ErrorMonitor.init();

  // 1. Loading screen (do first)
  LoadingScreen.init();

  // 2. Security
  SecurityManager.init();

  // 3. Theme (must be early)
  ThemeManager.init();

  // 4. Hardware detection
  HardwareDetector.apply();

  // 5. Cursor follower disabled for static perfection
  // CursorFollower.init();
 
  // 6. Navigation
  Navigation.init();
 
  // 6. Scroll animations disabled for static perfection
  // ScrollAnimations.init();
 
  // 7. Lazy loading
  LazyLoader.init();
 
  // 8. Smooth scroll
  initSmoothScroll();
 
  // 9. Counters
  initCounters();
 
  // 10. Typing effect disabled: using static keyword
  const typingEl = document.getElementById('hero-typing');
  if (typingEl) {
    typingEl.textContent = 'Ciberseguridad';
  }

  console.log('%c I.S.D.I — Isla Digital ', 'background: linear-gradient(135deg, #006AFF, #7B2FFF); color: #fff; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: bold;');
  console.log('%c Developed by LiebeBlack ', 'color: #00F0FF; font-family: monospace;');
});
