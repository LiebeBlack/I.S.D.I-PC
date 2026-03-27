/**
 * =============================================================================
 * I.S.D.I — Isla Digital | Abstract & Typographic 2D Engine
 * =============================================================================
 * Creates an advanced, minimalist, fragmented 2D conceptual background.
 * Uses high-performance instancing and procedural typography textures.
 * =========================================================================== */

'use strict';

const ParticleSystem = (() => {
  let scene, camera, renderer;
  let textGroup, geoGroup;
  let mouseX = 0, mouseY = 0;
  let targetX = 0, targetY = 0;
  let animFrame = null;
  let isInitialized = false;
  let clock;

  let elements = [];

  const CONFIG = {
    // Technical Typography (Syntax-As-Frame)
    textStrings: ['0xABC123', 'std::move()', 'I.S.D.I', 'async =>', 'await', 'int main()', 'Usar', '/>', '{...}', 'void*', 'sys_exec()'],
    textCount: 20, // Total textual floating elements
    // Erradicación Geométrica: No circles or lines, zero geometry.
    geoCount: 0,
    colorsDark: [0x00FFFF, 0xFF00FF, 0x39FF14, 0xFFD700, 0x8B5CF6, 0xFF3366], // Colores altamente vibrantes y neón
    colorsLight: [0x0052FF, 0xD4AF37, 0x0A1128, 0x8B9BB4],
  };

  /**
   * Generates a Three.js Texture from a string using Canvas 2D
   */
  function createTextTexture(text) {
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 128;
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.font = 'bold 80px "JetBrains Mono", monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(text, canvas.width / 2, canvas.height / 2);

    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter;
    texture.magFilter = THREE.LinearFilter;
    return texture;
  }

  function init(tier = 'high') {
    if (isInitialized) return;
    if (typeof THREE === 'undefined') return;

    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;

    // Adjust CONFIG based on tier
    if (tier === 'ultra') {
      CONFIG.textCount = 40;
    } else if (tier === 'med') {
      CONFIG.textStrings = ['I.S.D.I', '{...}', '0xABC', 'await'];
      CONFIG.textCount = 10;
    }

    isInitialized = true;
    clock = new THREE.Clock();

    scene = new THREE.Scene();

    // Everything in 2D layout: use OrthographicCamera
    const aspect = window.innerWidth / window.innerHeight;
    const frustumSize = 100;
    camera = new THREE.OrthographicCamera(
      frustumSize * aspect / -2, frustumSize * aspect / 2,
      frustumSize / 2, frustumSize / -2,
      0.1, 1000
    );
    camera.position.z = 10;

    renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: tier !== 'med',
      powerPreference: 'high-performance'
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    
    // Pixel ratio management
    const maxPR = tier === 'ultra' ? 2 : (tier === 'high' ? 1.8 : 1.2);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, maxPR));

    // Dramatic Lighting applied to 2D
    const ambientLight = new THREE.AmbientLight(0xffffff, tier === 'ultra' ? 0.6 : 0.4);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0xffffff, tier === 'ultra' ? 4.0 : 2.5, 300);
    pointLight1.position.set(0, 50, 20);
    scene.add(pointLight1);

    // Only one point light for med tier to save draws
    if (tier !== 'med') {
      const pointLight2 = new THREE.PointLight(0xffffff, tier === 'ultra' ? 4.0 : 2.5, 300);
      pointLight2.position.set(0, -50, 20);
      scene.add(pointLight2);
    }

    textGroup = new THREE.Group();
    geoGroup = new THREE.Group();
    scene.add(textGroup);
    scene.add(geoGroup);

    buildScene();

    window.addEventListener('resize', onResize, { passive: true });
    document.addEventListener('mousemove', onMouseMove, { passive: true });

    // Scroll interaction
    document.addEventListener('scroll', onScroll, { passive: true });

    // Web Performance: Pause when tab is invisible
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        if (animFrame) { cancelAnimationFrame(animFrame); animFrame = null; }
      } else {
        if (!animFrame && isInitialized) animate();
      }
    });

    animate();
    console.log(`[Particles] 2D Engine Initialized at ${tier.toUpperCase()} quality`);
  }

  function buildScene() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const colors = isDark ? CONFIG.colorsDark : CONFIG.colorsLight;
    const w = (window.innerWidth / window.innerHeight) * 100;
    const h = 100;

    // 1. Build Typographic Elements
    const planeGeo = new THREE.PlaneGeometry(30, 7.5);

    // We create materials per text to allow coloring
    const textMaterials = CONFIG.textStrings.map(text => {
      const tex = createTextTexture(text);
      return new THREE.MeshStandardMaterial({
        map: tex,
        transparent: true,
        opacity: 0.95, // Más opacidad para verse sólido
        roughness: 0.1,
        metalness: 0.3, // Menos metálico para no absorber tanta sombra
        emissive: 0x111111, // Auto-brillo sutil global
        alphaTest: 0.05,
        side: THREE.DoubleSide
      });
    });

    for (let i = 0; i < CONFIG.textCount; i++) {
      const mat = textMaterials[i % textMaterials.length].clone();
      mat.color.setHex(colors[Math.floor(Math.random() * colors.length)]);

      const mesh = new THREE.Mesh(planeGeo, mat);

      // Random 2D coordinates
      mesh.position.set((Math.random() - 0.5) * w, (Math.random() - 0.5) * h, 0);

      // Random slight rotation on Z to keep it flat but dynamic
      mesh.rotation.z = (Math.random() - 0.5) * 0.5;

      // Scale variations
      const s = 0.5 + Math.random() * 1.5;
      mesh.scale.set(s, s, s);

      setupElementData(mesh, w, h);
      textGroup.add(mesh);
      elements.push(mesh);
    }

    // 2. Build Abstract Geometry (Rings, Lines, Fragments)
    const geometries = [
      new THREE.RingGeometry(2, 2.2, 32),
      new THREE.CircleGeometry(1, 32),
      new THREE.PlaneGeometry(10, 0.2), // thin line
      new THREE.PlaneGeometry(0.2, 10), // thin vertical line
    ];

    // Minimalist fragmented design
    const geoMaterial = new THREE.MeshPhysicalMaterial({
      roughness: 0.1,
      metalness: 0.9,
      clearcoat: 1.0,
      transparent: true,
      opacity: 0.6,
      side: THREE.DoubleSide
    });

    for (let i = 0; i < CONFIG.geoCount; i++) {
      const geo = geometries[Math.floor(Math.random() * geometries.length)];
      const mat = geoMaterial.clone();
      mat.color.setHex(colors[Math.floor(Math.random() * colors.length)]);

      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set((Math.random() - 0.5) * w, (Math.random() - 0.5) * h, -1); // Slightly behind text
      mesh.rotation.z = Math.random() * Math.PI;

      const s = 0.5 + Math.random() * 2;
      mesh.scale.set(s, s, s);

      setupElementData(mesh, w, h);
      geoGroup.add(mesh);
      elements.push(mesh);
    }
  }

  function setupElementData(mesh, w, h) {
    mesh.userData = {
      ogX: mesh.position.x,
      ogY: mesh.position.y,
      speedX: (Math.random() - 0.5) * 0.05,
      speedY: (Math.random() - 0.5) * 0.05,
      rotSpeedZ: (Math.random() - 0.5) * 0.01,
      floatOffset: Math.random() * Math.PI * 2,
      w: w,
      h: h,
      scatterFactor: 0.2 + Math.random() * 0.8
    };
  }

  let scrollY = 0;
  function onScroll() {
    scrollY = window.scrollY * 0.05; // Scroll multiplier
  }

  function animate() {
    animFrame = requestAnimationFrame(animate);
    const time = clock.getElapsedTime();

    // Mouse magnetic interpolation (Fluid Micro-interactions)
    targetX += (mouseX * 0.05 - targetX) * 0.05;
    targetY += (mouseY * 0.05 - targetY) * 0.05;

    // Organic 2D Fluid Movement
    elements.forEach(el => {
      const data = el.userData;

      // 1. Base drifting
      data.ogX += data.speedX;
      data.ogY += data.speedY;

      // Screen wrapping (torus topology)
      if (data.ogX > data.w / 2 + 10) data.ogX = -data.w / 2 - 10;
      if (data.ogX < -data.w / 2 - 10) data.ogX = data.w / 2 + 10;
      if (data.ogY > data.h / 2 + 10) data.ogY = -data.h / 2 - 10;
      if (data.ogY < -data.h / 2 - 10) data.ogY = data.h / 2 + 10;

      // 2. Continuous slight floating 
      const floatX = Math.sin(time + data.floatOffset) * 2;
      const floatY = Math.cos(time + data.floatOffset) * 2;

      // 3. Mouse repulsion/attraction (Magnetic Fluidity)
      // targetX and targetY come from mouse
      const dx = data.ogX - targetX * data.w * 0.04;
      const dy = data.ogY + targetY * data.h * 0.04;

      // 4. Scroll reaction (parallax scatter)
      const scrollOffset = scrollY * data.scatterFactor;

      // Apply
      el.position.x = data.ogX + floatX + (dx * 0.02 * data.scatterFactor);
      el.position.y = data.ogY + floatY + (dy * 0.02 * data.scatterFactor) + scrollOffset;

      el.rotation.z += data.rotSpeedZ;

      // Minimal 3D tilt responding to mouse to catch lighting (2.5D dramatic lights)
      el.rotation.x = -targetY * 0.1;
      el.rotation.y = targetX * 0.1;
    });

    renderer.render(scene, camera);
  }

  function onResize() {
    if (!camera || !renderer) return;
    const aspect = window.innerWidth / window.innerHeight;
    const frustumSize = 100;

    // Update Orthographic boundaries
    camera.left = -frustumSize * aspect / 2;
    camera.right = frustumSize * aspect / 2;
    camera.top = frustumSize / 2;
    camera.bottom = -frustumSize / 2;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);

    // Update width/height bounds in metadata
    const w = (window.innerWidth / window.innerHeight) * 100;
    elements.forEach(el => { el.userData.w = w; });
  }

  function onMouseMove(e) {
    // Normalized [-1, 1]
    mouseX = (e.clientX / window.innerWidth) * 2 - 1;
    mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
  }

  function updateColors(theme) {
    if (!elements.length) return;
    const isDark = theme === 'dark';
    const colors = isDark ? CONFIG.colorsDark : CONFIG.colorsLight;

    elements.forEach(el => {
      const newColor = colors[Math.floor(Math.random() * colors.length)];
      el.material.color.setHex(newColor);
      if (el.material.metalness !== undefined) {
        el.material.metalness = isDark ? 0.3 : 0.2; // Conservar brillo
      }
    });

    // Añade más brillo a las luces en modo oscuro para el texto
    scene.children.forEach(child => {
      if (child.isPointLight) {
        child.intensity = isDark ? 4.5 : 2.5; // Doble de intensidad
      }
    });
  }

  function destroy() {
    if (animFrame) cancelAnimationFrame(animFrame);
    if (renderer) renderer.dispose();
    elements.forEach(b => {
      b.geometry.dispose();
      if (b.material.map) b.material.map.dispose();
      b.material.dispose();
    });
    elements = [];
    window.removeEventListener('resize', onResize);
    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('scroll', onScroll);
    isInitialized = false;
  }

  return { init, destroy, updateColors };
})();
