/* ============================================================
   I.S.D.I // ISLA DIGITAL — Application JavaScript
   Animations, Interactivity, Dynamic Content
   ============================================================ */

(() => {
  'use strict';

  /**
   * Application Configuration & Content Engine
   */
  const CONFIG = {
    scrollThreshold: 60,
    revealThreshold: 0.1,
    particleCount: 80,
    animationDuration: 2500
  };

  const MODULES_DATA = {
    hardware: {
      icon: 'ico-cpu',
      alpha: {
        title: 'La Gran Máquina: Los Motores de la Nave',
        intro: 'Imagina que la computadora es una nave espacial. Para viajar entre las estrellas, necesita motores que piensen, memorias que recuerden el camino y un armazón que proteja todo.',
        architecture: 'Dentro, el "Cerebro Central" (CPU) da todas las órdenes. Los cables son como venas por donde corre la energía y la información.',
        security: 'Una nave debe estar limpia y cuidada. No permitimos que entre polvo ni elementos extraños que puedan dañar los motores.',
        fact: '¡Las computadoras usan luces invisibles para enviarse mensajes, como hadas de datos!'
      },
      delta: {
        title: 'Arquitectura de Sistemas: El Ciclo de Datos',
        intro: 'El hardware no es solo metal y silicio; es una estructura lógica diseñada para procesar información a velocidades increíbles mediante impulsos eléctricos.',
        architecture: 'La placa base actúa como el sistema nervioso, conectando el CPU, la RAM y el almacenamiento.',
        security: 'El sobrecalentamiento y las fluctuaciones de energía son riesgos gestionados mediante sistemas de enfriamiento.',
        fact: 'Un bit es la unidad mínima de información, ¡un simple Sí o No!'
      },
      omega: {
        title: 'Ingeniería de Sistemas y Microarquitectura',
        intro: 'La computación moderna se basa en la abstracción de niveles, desde puertas lógicas hasta complejos sistemas operativos.',
        architecture: 'Arquitectura de Von Neumann: la separación entre procesamiento y memoria. Ciclos de reloj y ancho de banda.',
        security: 'Vulnerabilidades como Spectre/Meltdown. La seguridad comienza en el diseño del chip.',
        fact: 'Una contraseña fuerte tarda siglos en ser descifrada por una computadora normal.'
      }
    },
    logic: {
      icon: 'ico-terminal',
      alpha: {
        title: 'El Idioma Secreto de las Luces',
        intro: 'Las computadoras solo hablan un idioma de dos letras: Encendido y Apagado. Es como un código de espejos que permite contar historias complejas.',
        architecture: 'Cuando agrupamos estas luces, formamos instrucciones. Como una receta de cocina.',
        security: 'Nos aseguramos de que las instrucciones sean claras y honestas.',
        fact: '¡La primera programadora fue una mujer llamada Ada Lovelace!'
      },
      delta: {
        title: 'Lógica Procedimental y Algoritmos',
        intro: 'Un algoritmo es una secuencia finita de instrucciones definidas y no ambiguas que representan un modelo de solución para un problema.',
        architecture: 'Estructuras de control: bucles, condicionales y funciones.',
        security: 'Un código mal estructurado puede ocultar errores lógicos que comprometen la estabilidad.',
        fact: 'La palabra "Algoritmo" viene de Al-Juarismi, un matemático persa.'
      },
      omega: {
        title: 'Pensamiento Computacional y Estructuras Complejas',
        intro: 'El software moderno se construye sobre paradigmas de programación que optimizan la eficiencia y la mantenibilidad.',
        architecture: 'Complejidad algorítmica (Notación Big O) y estructuras de datos.',
        security: 'Seguridad por diseño: validar cada entrada y prever Buffer Overflow.',
        fact: 'El término "Bug" se popularizó cuando encontraron una polilla dentro de una computadora en 1947.'
      }
    },
    network: {
      icon: 'ico-globe',
      alpha: {
        title: 'Hilos Invisibles entre Estrellas',
        intro: 'El internet es como una red de pesca gigante que envuelve al mundo, conectando cada nave y cada planeta para que podamos enviarnos mensajes.',
        architecture: 'La información viaja en pequeños paquetes, como cartas en naves mensajeras rápidas.',
        security: 'Nunca abrimos la puerta a naves desconocidas y usamos un lenguaje secreto.',
        fact: 'Existen cables gigantes debajo del mar que conectan todos los continentes.'
      },
      delta: {
        title: 'Conectividad y Protocolos de Red',
        intro: 'Las redes permiten el intercambio de recursos mediante protocolos como TCP/IP que aseguran datos íntegros.',
        architecture: 'Modelo cliente-servidor: tu dispositivo solicita información a un servidor remoto.',
        security: 'Es vital utilizar HTTPS y firewalls para filtrar tráfico malicioso.',
        fact: '¡El primer mensaje de Arpanet fue "LO"!'
      },
      omega: {
        title: 'Topología de Redes y Seguridad Perimetral',
        intro: 'La infraestructura global de red es un sistema de sistemas autónomos interconectados. Modelo OSI.',
        architecture: 'Enrutamiento dinámico, DNS, latencia y la transición de IPv4 a IPv6.',
        security: 'Defensa en Profundidad: VPNs, IDS y segmentación de redes.',
        fact: 'El protocolo TCP/IP fue diseñado para sobrevivir a un ataque nuclear.'
      }
    },
    cybersecurity: {
      icon: 'ico-lock',
      alpha: {
        title: 'El Escudo de Cristal',
        intro: 'En nuestro viaje digital, llevamos un escudo de cristal que brilla cuando somos cuidadosos. Proteger nuestra información es vital.',
        architecture: 'Llaves secretas y puertas cerradas. No compartimos nuestras llaves con nadie.',
        security: 'La amabilidad es nuestra mejor regla. Si algo nos incomoda, avisamos a los adultos.',
        fact: '¡Captcha significa: Prueba de Turing para diferenciar computadoras de humanos!'
      },
      delta: {
        title: 'Ciberseguridad Activa y Privacidad',
        intro: 'La ciberseguridad protege sistemas, redes y programas de ataques digitales.',
        architecture: 'Autenticación multifactor (MFA) y criptografía.',
        security: 'Desconfiar de correos sospechosos (Phishing) es fundamental.',
        fact: 'La mayoría de ataques exitosos son por Ingeniería Social, no fallas técnicas.'
      },
      omega: {
        title: 'Criptografía Avanzada y Gestión de Amenazas',
        intro: 'La seguridad es un proceso continuo. El principio de "Confianza Cero" (Zero Trust) rige la arquitectura moderna.',
        architecture: 'Cifrado asimétrico, hashing y certificados digitales.',
        security: 'Análisis de malware, respuesta ante incidentes y Ransomware.',
        fact: 'La computación cuántica podría romper la mayoría de los cifrados actuales.'
      }
    },
    os: {
      icon: 'ico-monitor',
      alpha: {
        title: 'El Director de Orquesta Digital',
        intro: 'El Sistema Operativo es como el director de una orquesta, asegurándose de que cada músico toque en el momento justo.',
        architecture: 'Reparte tiempo y espacio. Decide quién puede hablar y quién debe esperar.',
        security: 'Pone vallas invisibles entre los programas para que si uno falla, los demás sigan.',
        fact: 'El primer sistema operativo fue creado por General Motors en 1956.'
      },
      delta: {
        title: 'Gestión de Recursos y Kernel',
        intro: 'El SO gestiona el hardware y actúa como intermediario entre usuario y máquina.',
        architecture: 'El Kernel: planificación de procesos (Scheduling) y gestión de RAM.',
        security: 'Listas de control de acceso (ACL) para gestión de permisos.',
        fact: '¡Linux está en todas partes! Desde Android hasta la Estación Espacial Internacional.'
      },
      omega: {
        title: 'Microkernels, Virtualización y Abstracción',
        intro: 'Los SO modernos implementan capas de abstracción para múltiples entornos sobre un mismo hardware.',
        architecture: 'Espacio de usuario vs espacio de kernel. Syscalls.',
        security: 'Sandboxing, contenedores y vulnerabilidades de escalada de privilegios.',
        fact: 'Windows originalmente se iba a llamar "Interface Manager".'
      }
    },
    ai: {
      icon: 'ico-bot',
      alpha: {
        title: 'Máquinas que Aprenden a Mirar',
        intro: 'La IA es como un robot que estudia millones de fotos y cuentos para aprender a reconocer cosas.',
        architecture: 'No es magia, son matemáticas. La IA busca patrones en los datos.',
        security: 'Debemos enseñar a la IA a ser justa y darle información honesta.',
        fact: '¡Una IA ha ganado a los mejores jugadores del mundo en Ajedrez y Go!'
      },
      delta: {
        title: 'Redes Neuronales y Aprendizaje Automático',
        intro: 'La IA usa algoritmos inspirados en el cerebro humano para procesar datos y tomar decisiones.',
        architecture: 'Machine Learning: datos para entrenar modelos con redes neuronales.',
        security: 'El sesgo algorítmico es un riesgo ético. La transparencia es fundamental.',
        fact: 'El término "Inteligencia Artificial" se acuñó en Dartmouth en 1956.'
      },
      omega: {
        title: 'Ética del Algoritmo y Deep Learning',
        intro: 'La IA generativa y los LLM están transformando la sociedad y el concepto de verdad.',
        architecture: '"Caja Negra" en modelos de aprendizaje profundo. Transformadores.',
        security: 'Data Poisoning y Deepfakes son amenazas críticas.',
        fact: '¡Las redes neuronales existen como idea desde los años 40!'
      }
    },
    programming: {
      icon: 'ico-code',
      alpha: {
        title: 'Dibujando con Instrucciones',
        intro: 'Programar es como darle un mapa del tesoro a un robot. Si le dices pasos claros, ¡encontrará el cofre!',
        architecture: 'Flechas y colores para hablar con las máquinas. Cada bloque es una acción.',
        security: 'Las instrucciones deben ser seguras. Nunca pedir algo que pueda dañar.',
        fact: '¡El primer lenguaje de programación se llamó Plankalkül!'
      },
      delta: {
        title: 'Variables, Tipos y Control de Flujo',
        intro: 'Las variables son cajas donde guardamos información: números, nombres, estados.',
        architecture: 'El flujo de ejecución decide qué camino toma el programa.',
        security: 'Validar los datos es vital para evitar errores críticos.',
        fact: 'Python es popular porque se lee casi como el inglés.'
      },
      omega: {
        title: 'Paradigmas de Programación y Escalabilidad',
        intro: 'La POO permite modelar el mundo real creando sistemas modulares y mantenibles.',
        architecture: 'Clases, herencia y polimorfismo para trabajo colaborativo a gran escala.',
        security: 'Encapsulamiento: variables privadas protegen datos sensibles.',
        fact: 'C++ corre la mayoría de los motores de videojuegos modernos.'
      }
    },
    ethics: {
      icon: 'ico-scale',
      alpha: {
        title: 'Ciudadanos del Espacio Digital',
        intro: 'En la Isla Digital, todos somos vecinos. Ser amable y ayudar hace que nuestra ciudad brille.',
        architecture: 'Las reglas son como puentes: nos permiten cruzar de forma segura.',
        security: 'Si alguien es grosero o te pide secretos, ¡pulsa el botón de ayuda!',
        fact: 'La netiqueta es el conjunto de reglas para ser educado en internet.'
      },
      delta: {
        title: 'Propiedad Intelectual y Huella Digital',
        intro: 'Todo lo que haces en internet deja un rastro, como huellas en la arena.',
        architecture: 'Respetar el trabajo de los demás es fundamental.',
        security: 'Configura tu privacidad. Tu información es un tesoro valioso.',
        fact: 'Lo que publicas hoy puede ser visto por alguien en el futuro distante.'
      },
    omega: {
      title: 'Algoritmos, Sesgo y Sociedad Tecnológica',
      intro: 'La tecnología no es neutral; refleja los valores de quienes la crean.',
      architecture: 'Burbujas de Filtro: sistemas que solo muestran lo que queremos ver.',
      security: 'Transparencia en la IA: explicar por qué un algoritmo toma decisiones.',
      fact: 'El sesgo de confirmación nos hace creer lo que ya encaja con nuestras ideas.'
    }
  }
};

const MODULE_DISPLAY_NAMES = {
  hardware: 'Hardware',
  logic: 'Lógica',
  network: 'Redes',
  cybersecurity: 'Ciberseguridad',
  os: 'Sistemas',
  ai: 'IA',
  programming: 'Código',
  ethics: 'Ética'
};

  /**
   * DOM Utilities
   */
  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => document.querySelectorAll(selector);

  /**
   * Navigation Logic
   */
  function initNavigation() {
    const navbar = $('#navbar');
    const toggle = $('#mobileToggle');
    const links = $('#navLinks');
    
    if (!navbar || !toggle || !links) return;

    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > CONFIG.scrollThreshold);
    }, { passive: true });

    toggle.addEventListener('click', () => {
      const isOpen = links.classList.toggle('open');
      toggle.classList.toggle('open');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Keyboard accessibility for mobile toggle
    toggle.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggle.click();
      }
    });

    $$('#navLinks a').forEach(link => {
      link.addEventListener('click', () => {
        toggle.classList.remove('open');
        links.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /**
   * Animation & Reveal Logic
   */
  function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: CONFIG.revealThreshold,
      rootMargin: '0px 0px -50px 0px'
    });

    $$('.reveal').forEach(el => observer.observe(el));
  }

  /**
   * Background Particles Engine
   */
  function initParticles() {
    const isMobile = window.innerWidth < 768;
    const canvas = $('#particles-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d', { alpha: true }); // Performance hint
    let particles = [];
    let animationId;
    
    const countModifier = isMobile ? 0.4 : 1;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initParticleArray();
    };

    const createParticle = () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: Math.random() * 1.5 + 0.5,
      speedX: (Math.random() - 0.5) * 0.18,
      speedY: (Math.random() - 0.5) * 0.18,
      opacity: Math.random() * 0.5 + 0.1,
    });

    const initParticleArray = () => {
      const baseCount = Math.min(CONFIG.particleCount, Math.floor(canvas.width * canvas.height / 15000));
      const count = Math.floor(baseCount * countModifier);
      particles = Array.from({ length: count }, createParticle);
    };

    const drawParticles = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach(p => {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 200, 83, ${p.opacity})`;
        ctx.fill();

        p.x += p.speedX;
        p.y += p.speedY;

        if (p.x < 0 || p.x > canvas.width) p.speedX *= -1;
        if (p.y < 0 || p.y > canvas.height) p.speedY *= -1;
      });

      // Connections logic
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(0, 200, 83, ${0.06 * (1 - dist / 120)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }
      animationId = requestAnimationFrame(drawParticles);
    };

    resize();
    drawParticles();

    window.addEventListener('resize', resize);
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) cancelAnimationFrame(animationId);
      else drawParticles();
    });
  }

  /**
   * Educational Content Area
   */
  function initModuleTabs() {
    const tabContainer = $('#moduleTabs');
    const contentArea = $('#moduleContent');
    if (!tabContainer || !contentArea) return;

    // Render Tabs dynamically
    tabContainer.innerHTML = Object.keys(MODULES_DATA).map((key, index) => {
      const activeClass = index === 0 ? 'active' : '';
      const selected = index === 0 ? 'true' : 'false';
      return `<button class="module-tab ${activeClass}" 
                      data-module="${key}" 
                      role="tab" 
                      aria-selected="${selected}" 
                      aria-controls="moduleContent">${MODULE_DISPLAY_NAMES[key] || key}</button>`;
    }).join('');

    const tabs = $$('.module-tab');
    if (!tabs.length) return;

    const renderModule = (moduleKey) => {
      const data = MODULES_DATA[moduleKey];
      if (!data) return;

      const protocols = ['alpha', 'delta', 'omega'];
      const labels = { alpha: 'Alpha (3-7)', delta: 'Delta (8-12)', omega: 'Omega (13-16)' };
      const colors = { alpha: 'green', delta: 'blue', omega: 'orange' };
      const svgIcon = (id, size = 20) => `<svg width="${size}" height="${size}" aria-hidden="true"><use href="#${id}"/></svg>`;

      contentArea.innerHTML = `
        <div class="module-info">
          <span class="label label-green">// UNIDAD EDUCATIVA</span>
          <h3>${data.alpha.title}</h3>
          <p class="module-intro">${data.alpha.intro}</p>

          <div class="module-detail-cards">
            ${protocols.map(p => `
              <div class="module-detail-card">
                <div class="module-detail-icon">${svgIcon(data.icon)}</div>
                <div>
                  <div class="module-detail-title">${labels[p]}</div>
                  <div class="module-detail-text">${data[p].intro}</div>
                </div>
              </div>
            `).join('')}
          </div>

          <div class="glass-alert" style="margin-top: var(--sp-4); padding: var(--sp-2); border-radius: var(--r-md); background: var(--c-yellow-dim); border: 1px solid rgba(255,214,0,0.15); text-align:center;">
            <div style="display:flex;align-items:center;justify-content:center;gap:0.5rem;margin-bottom:0.3rem;">
              ${svgIcon('ico-zap', 16)}
              <strong style="font-size:0.82rem;color:var(--c-yellow);">¿SABÍAS QUE...?</strong>
            </div>
            <p style="font-size:0.88rem;color:var(--c-text-secondary);font-style:italic;margin-bottom:0;">${data.alpha.fact}</p>
          </div>
        </div>

        <div class="module-preview">
          <div class="glass" style="padding: var(--sp-4); text-align:center;">
            <div style="display:flex;align-items:center;justify-content:center;gap:0.8rem;margin-bottom:var(--sp-3);">
              <span style="color:var(--c-green);">${svgIcon(data.icon, 28)}</span>
              <div>
                <div style="font-family:var(--f-mono);font-size:0.75rem;color:var(--c-text-dim);font-weight:700;">ESTRUCTURA DEL MÓDULO</div>
                <div style="font-weight:700;">${data.delta.title}</div>
              </div>
            </div>

            ${protocols.map(p => `
              <div style="padding: var(--sp-2); border-radius: var(--r-sm); margin-bottom: 0.5rem; background: var(--c-${colors[p]}-dim); border-left: 3px solid var(--c-${colors[p]}); text-align:center;">
                <div style="font-size:0.78rem;font-weight:700;color:var(--c-${colors[p]});margin-bottom:0.1rem;">${labels[p].toUpperCase()}</div>
                <div style="font-size:0.82rem;color:var(--c-text-secondary);">${data[p].architecture}</div>
              </div>
            `).join('')}

            <div style="margin-top: var(--sp-3); padding: var(--sp-2); border-radius: var(--r-sm); background: var(--c-orange-dim); border: 1px solid rgba(255,61,0,0.15); text-align:center;">
              <div style="display:flex;align-items:center;justify-content:center;gap:0.4rem;font-size:0.78rem;font-weight:700;color:var(--c-orange);margin-bottom:0.1rem;">
                ${svgIcon('ico-shield', 14)} SEGURIDAD
              </div>
              <div style="font-size:0.82rem;color:var(--c-text-secondary);">${data.omega.security}</div>
            </div>
          </div>
        </div>
      `;
    };

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const currentActive = $('.module-tab.active');
        if (currentActive === tab) return;

        currentActive?.classList.remove('active');
        currentActive?.setAttribute('aria-selected', 'false');
        
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');

        contentArea.style.opacity = '0';
        contentArea.style.transform = 'translateY(15px)';

        setTimeout(() => {
          renderModule(tab.dataset.module);
          contentArea.style.opacity = '1';
          contentArea.style.transform = 'translateY(0)';
        }, 420);
      });
    });

    contentArea.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    renderModule('hardware');
  }

  /**
   * Terminal Simulation
   */
  function initTerminal() {
    const body = $('#terminalBody');
    const windowEl = $('#terminalWindow');
    if (!body || !windowEl) return;

    const lines = [
      { text: '$ isdi --init --protocol=ALL', class: 'terminal-prompt', delay: 0 },
      { text: '> [SISTEMA] Iniciando Núcleo I.S.D.I v4.0.2... LISTO', class: 'terminal-success', delay: 660 },
      { text: '> [RECORRIDO] Sincronizando protocolos pedagógicos... LISTO', class: 'terminal-info', delay: 1330 },
      { text: '> [SEGURIDAD] Estableciendo perímetro digital seguro... LISTO', class: 'terminal-success', delay: 2000 },
      { text: '> [DATOS] Indexando biblioteca de conocimientos... LISTO', class: 'terminal-info', delay: 2660 },
      { text: '> [CONTENT] Cargando 8 unidades × 3 protocolos = 24 módulos', class: 'terminal-info', delay: 3330 },
      { text: '> [CRYPTO] Cifrado AES-256 activo en todas las comunicaciones', class: 'terminal-warning', delay: 4000 },
      { text: '> [DATABASE] isla_digital.db sincronizada — SQLite3 operativo', class: 'terminal-success', delay: 4660 },
      { text: '> [OK] SISTEMA PREPARADO. Esperando selección de protocolo...', class: 'terminal-success', delay: 5330 },
      { text: '', class: 'cursor', delay: 6000 }
    ];

    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) {
        body.innerHTML = '';
        lines.forEach((line) => {
          setTimeout(() => {
            const div = document.createElement('div');
            div.className = 'terminal-line';
            div.innerHTML = line.class === 'cursor' 
              ? '<span class="terminal-prompt">$ </span><span class="terminal-cursor"></span>'
              : `<span class="${line.class}">${line.text}</span>`;
            body.appendChild(div);
            body.scrollTop = body.scrollHeight;
          }, line.delay);
        });
        observer.unobserve(windowEl);
      }
    }, { threshold: 0.3 });

    observer.observe(windowEl);
  }

  /**
   * Interactions: FAQ & Smooth Scroll
   */
  function initInteractions() {
    // FAQ
    $$('.faq-question').forEach(btn => {
      btn.addEventListener('click', () => {
        const item = btn.closest('.faq-item');
        const isOpen = item.classList.contains('open');

        $$('.faq-item').forEach(fi => fi.classList.remove('open'));
        $$('.faq-question').forEach(q => q.setAttribute('aria-expanded', 'false'));

        if (!isOpen) {
          item.classList.add('open');
          btn.setAttribute('aria-expanded', 'true');
        }
      });
    });

    // Smooth Scroll
    $$('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        if (href === '#') return;
        e.preventDefault();
        $(href)?.scrollIntoView({ behavior: 'smooth' });
      });
    });
  }

  /**
   * Curriculum Tags Interactivity
   */
  function initCurriculumInteractions() {
    const tags = $$('.interactive-tag');
    
    tags.forEach(tag => {
      tag.addEventListener('click', () => {
        const parentBody = tag.closest('.curriculum-body');
        if (!parentBody) return;

        const titleEl = parentBody.querySelector('.curriculum-title');
        const descEl = parentBody.querySelector('.curriculum-desc');
        
        const newTitle = tag.dataset.title;
        const newDesc = tag.dataset.desc;

        // Visual feedback on tag
        parentBody.querySelectorAll('.interactive-tag').forEach(t => t.classList.remove('active'));
        tag.classList.add('active');

        // Animate content change
        [titleEl, descEl].forEach(el => {
          el.style.opacity = '0';
          el.style.transform = 'translateY(-5px)';
        });

        setTimeout(() => {
          if (titleEl) titleEl.textContent = newTitle;
          if (descEl) descEl.textContent = newDesc;
          
          [titleEl, descEl].forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
            el.style.transition = 'all 0.5s ease';
          });
        }, 330);
      });
      
      // Add pointer cursor via JS if not in CSS
      tag.style.cursor = 'pointer';
    });
  }

  /**
   * Stats Counters
   */
  function initCounters() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.count, 10);
          let current = 0;
          const step = Math.max(1, Math.ceil(target / (CONFIG.animationDuration / 30)));

          const timer = setInterval(() => {
            current += step;
            if (current >= target) {
              current = target;
              clearInterval(timer);
            }
            el.textContent = current;
          }, 30);

          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    $$('.impact-value[data-count]').forEach(c => observer.observe(c));
  }

  /**
   * Active Navigation Highlighting
   */
  function initActiveNav() {
    const navLinks = $$('.nav-links a');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          navLinks.forEach(link => {
            link.style.color = (link.getAttribute('href') === `#${id}`) ? 'var(--c-green)' : '';
          });
        }
      });
    }, { threshold: 0.2, rootMargin: '-80px 0px -50% 0px' });

    $$('section[id]').forEach(s => {
      if (s) observer.observe(s);
    });
  }

  /**
   * App Bootstrap
   */
  function boot() {
    // Simulated system boot logs for splash screen
    console.log("IDENTIFICANDO NÚCLEO I.S.D.I...");
    setTimeout(() => console.log("ESTABLECIENDO CONEXIÓN SEGURA..."), 400);
    setTimeout(() => console.log("RECOLECTANDO MÓDULOS PEDAGÓGICOS..."), 800);
    setTimeout(() => console.log("PREPARANDO ENTORNO INTERACTIVO..."), 1200);
    setTimeout(() => console.log("¡SISTEMA LISTO PARA EXPLORACIÓN!"), 1600);

    initNavigation();
    initScrollReveal();
    initParticles();
    initModuleTabs();
    initTerminal();
    initInteractions();
    initCurriculumInteractions();
    initCounters();
    initActiveNav();
  }

  // Load Strategy
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
