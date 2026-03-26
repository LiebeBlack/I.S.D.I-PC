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
   * Test GPU performance by rendering to a WebGL canvas.
   * Returns 'high' or 'low' based on GPU tier.
   */
  function detectGPU() {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      
      // Fallback a low solo si WebGL está completamente deshabilitado
      if (!gl) return 'low';

      const cores = navigator.hardwareConcurrency || 4;
      const memory = navigator.deviceMemory || 4;
      const isMobile = /Android|iPhone|iPad|iPod|webOS|BlackBerry|Opera Mini|IEMobile/i.test(navigator.userAgent);

      // BAJADA DE LÍMITES CORTESÍA DEL MODO 2020:
      // Si es PC de Escritorio/Laptop, permitimos siempre el renderizado pesado
      if (!isMobile) return 'high';

      // En Móvil: Solo lo apagamos si tiene menos de 4 núcleos o < 4GB de RAM (Gama muy baja pre-2020)
      if (isMobile && (cores >= 4 || memory >= 4)) return 'high';

      // Default para calculadoras muy antiguas:
      return 'low';
    } catch (e) {
      console.warn('[HW Detect] GPU detection failed, defaulting to low:', e);
      return 'low';
    }
  }

  /**
   * Apply the detected tier to the DOM.
   */
  function apply() {
    const tier = detectGPU();
    document.body.classList.add(tier === 'high' ? 'high-end' : 'low-end');
    document.body.dataset.gpuTier = tier;

    // Activate appropriate background
    const staticBg = document.getElementById('static-bg');
    const particleCanvas = document.getElementById('particle-canvas');

    if (tier === 'high') {
      // Fallback Inteligente: Show Vivid Mesh while WebGL computes
      if (staticBg) staticBg.classList.add('active');
      if (particleCanvas) particleCanvas.classList.add('active');

      // Initialize Three.js particles
      if (typeof ParticleSystem !== 'undefined') {
        ParticleSystem.init();
        // Fade out static mesh fallback after 3D is fully rendering
        setTimeout(() => {
          if (staticBg) staticBg.classList.remove('active');
        }, 1800);
      }
    } else {
      // Low-end uses the Vivid Mesh Gradient permanently
      if (staticBg) staticBg.classList.add('active');
    }

    // Update performance pill
    const dot = document.querySelector('.perf-pill__dot');
    const label = document.querySelector('.perf-pill__label');
    if (dot && label) {
      dot.classList.add(tier === 'high' ? 'perf-pill__dot--high' : 'perf-pill__dot--low');
      label.textContent = tier === 'high' ? 'GPU: High-End' : 'GPU: Optimized';
    }

    console.log(`[HW Detect] GPU Tier: ${tier}`);
    return tier;
  }

  return { detect: detectGPU, apply };
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
  function init() {
    const loader = document.querySelector('.loader');
    if (!loader) return;

    window.addEventListener('load', () => {
      setTimeout(() => {
        loader.classList.add('hidden');
        // Remove from DOM after transition
        setTimeout(() => loader.remove(), 600);
      }, 600);
    });

    // Fallback: Hide loader after 4 seconds max
    setTimeout(() => {
      if (loader && !loader.classList.contains('hidden')) {
        loader.classList.add('hidden');
        setTimeout(() => loader.remove(), 600);
      }
    }, 4000);
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
  function init() {
    // Disable Context Menu
    document.addEventListener('contextmenu', e => e.preventDefault());

    // Disable Image Dragging
    document.addEventListener('dragstart', e => {
      if (e.target.tagName === 'IMG') e.preventDefault();
    });

    // Disable Shortcuts (Ctrl+C, Ctrl+X, Ctrl+U, Cmd+C, Cmd+X, Cmd+U)
    document.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey)) {
        const key = e.key.toLowerCase();
        if (key === 'c' || key === 'x' || key === 'u') {
          e.preventDefault();
        }
      }
    });
  }

  return { init };
})();

/* =============================================================================
 * Initialize Everything on DOM Ready
 * =========================================================================== */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Loading screen (do first)
  LoadingScreen.init();

  // 2. Theme (must be early)
  ThemeManager.init();

  // 3. Hardware detection
  HardwareDetector.apply();

  // 4. Cursor follower
  CursorFollower.init();

  // 5. Navigation
  Navigation.init();

  // 6. Scroll animations
  ScrollAnimations.init();

  // 7. Lazy loading
  LazyLoader.init();

  // 8. Smooth scroll
  initSmoothScroll();

  // 9. Counters
  initCounters();

  // 10. Typing effect (if hero typing element exists)
  const typingEl = document.getElementById('hero-typing');
  if (typingEl) {
    createTypingEffect(typingEl, [
      'Ciberseguridad',
      'Hardware Avanzado',
      'Arquitectura Limpia',
      'Python & Flet',
      'Isla Digital'
    ], 90, 2500);
  }

  console.log('%c I.S.D.I — Isla Digital ', 'background: linear-gradient(135deg, #006AFF, #7B2FFF); color: #fff; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: bold;');
  console.log('%c Developed by LiebeBlack ', 'color: #00F0FF; font-family: monospace;');

  // 11. Activate Security
  SecurityManager.init();
});
