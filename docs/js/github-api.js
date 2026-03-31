/**
 * =============================================================================
 * I.S.D.I — Isla Digital | GitHub API Integration
 * =============================================================================
 * Real-time repository file viewer using the GitHub REST API.
 * Displays file tree, file contents, and repository metadata.
 * =========================================================================== */

'use strict';

const GitHubViewer = (() => {
  // Repository configuration
  const REPO_OWNER = 'LiebeBlack';
  const REPO_NAME = 'I.S.D.I-PC';
  const API_BASE = 'https://api.github.com';
  const RAW_BASE = `https://raw.githubusercontent.com/${REPO_OWNER}/${REPO_NAME}/main`;

  // Cache for API responses
  const cache = new Map();
  const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

  // File type icons (clean text indicators)
  const FILE_ICONS = {
    'py': 'PY',
    'js': 'JS',
    'html': 'HTM',
    'css': 'CSS',
    'md': 'MD',
    'json': 'CFG',
    'yml': 'YML',
    'yaml': 'YML',
    'txt': 'TXT',
    'sql': 'SQL',
    'db': 'DB',
    'png': 'IMG',
    'jpg': 'IMG',
    'jpeg': 'IMG',
    'gif': 'IMG',
    'svg': 'SVG',
    'ico': 'ICO',
    'gitignore': 'GIT',
    'env': 'ENV',
    'toml': 'CFG',
    'cfg': 'CFG',
    'ini': 'CFG',
    'sh': 'SH',
    'bat': 'BAT',
    'lock': 'LCK',
    'default': '—'
  };

  /**
   * Fetch with caching.
   */
  async function fetchCached(url) {
    const cached = cache.get(url);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
      return cached.data;
    }

    try {
      const response = await fetch(url, {
        headers: { 'Accept': 'application/vnd.github.v3+json' }
      });

      if (!response.ok) {
        throw new Error(`GitHub API Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      cache.set(url, { data, timestamp: Date.now() });
      return data;
    } catch (error) {
      console.error('[GitHub API]', error);
      throw error;
    }
  }

  /**
   * Fetch repository metadata.
   */
  async function getRepoInfo() {
    return fetchCached(`${API_BASE}/repos/${REPO_OWNER}/${REPO_NAME}`);
  }

  /**
   * Fetch repository contents at a given path.
   */
  async function getContents(path = '') {
    const url = `${API_BASE}/repos/${REPO_OWNER}/${REPO_NAME}/contents/${path}`;
    return fetchCached(url);
  }

  /**
   * Fetch raw file content.
   */
  async function getRawContent(path) {
    const url = `${RAW_BASE}/${path}`;
    const cached = cache.get(url);
    if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
      return cached.data;
    }

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Failed to fetch: ${response.status}`);
      const text = await response.text();
      cache.set(url, { data: text, timestamp: Date.now() });
      return text;
    } catch (error) {
      console.error('[GitHub API] Raw content error:', error);
      throw error;
    }
  }

  /**
   * Get recent commits.
   */
  async function getCommits(count = 10) {
    return fetchCached(`${API_BASE}/repos/${REPO_OWNER}/${REPO_NAME}/commits?per_page=${count}`);
  }

  /**
   * Get file icon by extension.
   */
  function getFileIcon(filename) {
    if (!filename) return FILE_ICONS.default;
    const ext = filename.split('.').pop().toLowerCase();
    return FILE_ICONS[ext] || FILE_ICONS.default;
  }

  /**
   * Format file size.
   */
  function formatSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

  /**
   * Format date relative.
   */
  function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    const mins = Math.floor(diff / 60000);
    const hours = Math.floor(mins / 60);
    const days = Math.floor(hours / 24);

    if (mins < 1) return 'hace un momento';
    if (mins < 60) return `hace ${mins}m`;
    if (hours < 24) return `hace ${hours}h`;
    if (days < 30) return `hace ${days}d`;
    return date.toLocaleDateString('es-ES', { year: 'numeric', month: 'short', day: 'numeric' });
  }

  /**
   * Initialize the repository viewer UI.
   */
  async function init() {
    const container = document.getElementById('repo-viewer');
    if (!container) return;

    try {
      showLoading();
      await Promise.all([loadRepoInfo(), loadFileTree()]);
    } catch (error) {
      showError(error.message);
    }
  }

  /**
   * Load and display repository information.
   */
  async function loadRepoInfo() {
    const banner = document.getElementById('repo-banner');
    if (!banner) return;

    try {
      const repo = await getRepoInfo();

      banner.innerHTML = `
        <div class="repo-banner__info">
          <img src="${repo.owner.avatar_url}" alt="${repo.owner.login}" class="repo-banner__avatar" loading="lazy" />
          <div>
            <div class="repo-banner__name">${SecurityManager.sanitize(repo.full_name)}</div>
            <div class="repo-banner__desc">${SecurityManager.sanitize(repo.description) || 'I.S.D.I — Isla Digital'}</div>
          </div>
        </div>
        <div class="repo-banner__stats">
          <div class="repo-stat">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <span>${repo.stargazers_count}</span>
          </div>
          <div class="repo-stat">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>
            <span>${repo.forks_count}</span>
          </div>
          <div class="repo-stat">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            <span>${repo.watchers_count}</span>
          </div>
          <div class="repo-stat">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            <span>${SecurityManager.sanitize(repo.language) || 'Python'}</span>
          </div>
        </div>
      `;
    } catch (error) {
      banner.innerHTML = `
        <div class="repo-banner__info">
          <div class="repo-banner__name">${REPO_OWNER}/${REPO_NAME}</div>
          <div class="repo-banner__desc">No se pudo cargar la información del repositorio</div>
        </div>
      `;
    }
  }

  /**
   * Load and render the file tree.
   */
  async function loadFileTree(path = '') {
    const treeContainer = document.getElementById('file-tree-content');
    if (!treeContainer) return;

    try {
      if (!path) {
        treeContainer.innerHTML = '<div class="skeleton" style="height: 300px;"></div>';
      }

      const contents = await getContents(path);
      const items = Array.isArray(contents) ? contents : [contents];

      // Sort: directories first, then files alphabetically
      items.sort((a, b) => {
        if (a.type === 'dir' && b.type !== 'dir') return -1;
        if (a.type !== 'dir' && b.type === 'dir') return 1;
        return a.name.localeCompare(b.name);
      });

      if (!path) {
        treeContainer.innerHTML = '';
      }

      const fragment = document.createDocumentFragment();

      items.forEach(item => {
        const el = document.createElement('div');
        el.className = 'tree-item';
        el.dataset.path = item.path;
        el.dataset.type = item.type;

        const sizeLabel = item.size ? ` (${formatSize(item.size)})` : '';
        let icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>'; // Default file
        if (item.type === 'dir') {
          icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>';
        } else {
          const ext = item.name.split('.').pop().toLowerCase();
          if (ext === 'py') icon = '<span style="color: #3776AB">🐍</span>';
          if (ext === 'js') icon = '<span style="color: #F7DF1E">JS</span>';
          if (ext === 'md') icon = '<span style="color: #555">MD</span>';
          if (ext === 'html') icon = '<span style="color: #E34F26"><></span>';
        }

        el.innerHTML = `
          <span class="tree-item__icon">${icon}</span>
          <span class="tree-item__name">${SecurityManager.sanitize(item.name)}${sizeLabel}</span>
        `;

        if (item.type === 'dir') {
          el.addEventListener('click', () => toggleDirectory(el, item.path));
        } else {
          el.addEventListener('click', () => loadFileContent(item.path, item.name));
        }

        fragment.appendChild(el);

        // Container for subdirectory contents
        if (item.type === 'dir') {
          const childContainer = document.createElement('div');
          childContainer.className = 'tree-item__children';
          childContainer.id = `tree-children-${item.path.replace(/[\/\.]/g, '-')}`;
          fragment.appendChild(childContainer);
        }
      });

      if (!path) {
        treeContainer.appendChild(fragment);
      }

      return fragment;
    } catch (error) {
      if (!path) {
        treeContainer.innerHTML = `
          <div style="padding: var(--space-md); color: var(--text-tertiary); text-align: center;">
            <p>Error al cargar archivos</p>
            <p style="font-size: var(--text-xs); margin-top: var(--space-xs);">${error.message}</p>
            <button onclick="GitHubViewer.init()" class="btn btn--ghost" style="margin-top: var(--space-sm);">
              Reintentar
            </button>
          </div>
        `;
      }
    }
  }

  /**
   * Toggle directory expand/collapse.
   */
  async function toggleDirectory(element, path) {
    const childId = `tree-children-${path.replace(/[\/\.]/g, '-')}`;
    const childContainer = document.getElementById(childId);
    if (!childContainer) return;

    if (childContainer.classList.contains('expanded')) {
      childContainer.classList.remove('expanded');
      element.querySelector('.tree-item__icon').textContent = 'DIR';
      return;
    }

    // Load children if not yet loaded
    if (!childContainer.children.length) {
      childContainer.innerHTML = '<div class="skeleton" style="height: 24px; margin: 4px 0;"></div>';
      childContainer.classList.add('expanded');

      try {
        const contents = await getContents(path);
        const items = Array.isArray(contents) ? contents : [contents];

        items.sort((a, b) => {
          if (a.type === 'dir' && b.type !== 'dir') return -1;
          if (a.type !== 'dir' && b.type === 'dir') return 1;
          return a.name.localeCompare(b.name);
        });

        childContainer.innerHTML = '';

        items.forEach(item => {
          const el = document.createElement('div');
          el.className = 'tree-item';
          el.dataset.path = item.path;
          el.dataset.type = item.type;

          const icon = item.type === 'dir' ? 'DIR' : getFileIcon(item.name);
          const sizeLabel = item.size ? ` (${formatSize(item.size)})` : '';

          el.innerHTML = `
            <span class="tree-item__icon">${icon}</span>
            <span class="tree-item__name">${item.name}${sizeLabel}</span>
          `;

          if (item.type === 'dir') {
            el.addEventListener('click', (e) => {
              e.stopPropagation();
              toggleDirectory(el, item.path);
            });
          } else {
            el.addEventListener('click', (e) => {
              e.stopPropagation();
              loadFileContent(item.path, item.name);
            });
          }

          childContainer.appendChild(el);

          if (item.type === 'dir') {
            const subChildContainer = document.createElement('div');
            subChildContainer.className = 'tree-item__children';
            subChildContainer.id = `tree-children-${item.path.replace(/[\/\.]/g, '-')}`;
            childContainer.appendChild(subChildContainer);
          }
        });
      } catch (error) {
        childContainer.innerHTML = `<div style="color: var(--text-muted); padding: 4px 12px; font-size: 12px;">Error: ${error.message}</div>`;
      }
    } else {
      childContainer.classList.add('expanded');
    }

    element.querySelector('.tree-item__icon').textContent = '▸';
  }

  /**
   * Load and display file content in the preview panel.
   */
  async function loadFileContent(path, filename) {
    const preview = document.getElementById('file-preview');
    const previewPath = document.getElementById('file-preview-path');
    const previewContent = document.getElementById('file-preview-content');
    if (!preview || !previewContent) return;

    // Update active state
    document.querySelectorAll('.tree-item.active').forEach(el => el.classList.remove('active'));
    const activeItem = document.querySelector(`.tree-item[data-path="${path}"]`);
    if (activeItem) activeItem.classList.add('active');

    // Update path display
    if (previewPath) previewPath.textContent = path;

    // Show loading
    previewContent.innerHTML = `
      <div class="skeleton" style="height: 16px; width: 80%; margin-bottom: 8px;"></div>
      <div class="skeleton" style="height: 16px; width: 60%; margin-bottom: 8px;"></div>
      <div class="skeleton" style="height: 16px; width: 90%; margin-bottom: 8px;"></div>
      <div class="skeleton" style="height: 16px; width: 70%; margin-bottom: 8px;"></div>
      <div class="skeleton" style="height: 16px; width: 85%;"></div>
    `;

    try {
      // Check file extension for binary files
      const ext = filename.split('.').pop().toLowerCase();
      const binaryExts = ['png', 'jpg', 'jpeg', 'gif', 'ico', 'svg', 'webp', 'db', 'sqlite'];

      if (binaryExts.includes(ext)) {
        if (['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'].includes(ext)) {
          previewContent.innerHTML = `
            <div style="text-align: center; padding: var(--space-xl);">
              <img src="${RAW_BASE}/${path}" alt="${filename}" style="max-width: 100%; max-height: 400px; border-radius: var(--radius-md);" />
              <p style="margin-top: var(--space-sm); color: var(--text-tertiary); font-size: var(--text-sm);">
                ${filename}
              </p>
            </div>
          `;
        } else {
          previewContent.innerHTML = `
            <div class="file-preview__placeholder">
              <span style="font-size: 3rem; font-family: var(--font-mono); opacity: 0.2;">BIN</span>
              <span>Archivo binario — no se puede previsualizar</span>
              <a href="https://github.com/${REPO_OWNER}/${REPO_NAME}/blob/main/${path}" 
                 target="_blank" class="btn btn--ghost" style="margin-top: var(--space-sm);">
                Ver en GitHub →
              </a>
            </div>
          `;
        }
        return;
      }

      const content = await getRawContent(path);

      // Escape HTML
      const escaped = content
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

      // Add line numbers
      const lines = escaped.split('\n');
      const numbered = lines.map((line, i) =>
        `<span style="color: var(--text-muted); user-select: none; display: inline-block; min-width: 3em; text-align: right; margin-right: 1em; opacity: 0.5;">${i + 1}</span>${line}`
      ).join('\n');

      previewContent.innerHTML = `<pre style="margin: 0; white-space: pre-wrap; word-break: break-all;">${numbered}</pre>`;

    } catch (error) {
      previewContent.innerHTML = `
        <div class="file-preview__placeholder">
          <span style="font-size: 3rem; font-family: var(--font-mono); opacity: 0.2">ERR</span>
          <span>Error al cargar el archivo</span>
          <p style="font-size: var(--text-xs); color: var(--text-muted);">${error.message}</p>
        </div>
      `;
    }
  }

  /**
   * Show loading state.
   */
  function showLoading() {
    const treeContainer = document.getElementById('file-tree-content');
    if (treeContainer) {
      treeContainer.innerHTML = `
        <div class="skeleton" style="height: 24px; margin-bottom: 6px;"></div>
        <div class="skeleton" style="height: 24px; margin-bottom: 6px;"></div>
        <div class="skeleton" style="height: 24px; margin-bottom: 6px;"></div>
        <div class="skeleton" style="height: 24px; margin-bottom: 6px;"></div>
        <div class="skeleton" style="height: 24px;"></div>
      `;
    }
  }

  /**
   * Show error state.
   */
  function showError(message) {
    const treeContainer = document.getElementById('file-tree-content');
    if (treeContainer) {
      treeContainer.innerHTML = `
        <div style="padding: var(--space-md); text-align: center; color: var(--text-tertiary);">
          <p>${message}</p>
          <button onclick="GitHubViewer.init()" class="btn btn--ghost" style="margin-top: var(--space-sm);">
            Reintentar
          </button>
        </div>
      `;
    }
  }

  /**
   * Load recent commits.
   */
  async function loadCommits() {
    const container = document.getElementById('commits-list');
    if (!container) return;

    try {
      container.innerHTML = `
        <div class="skeleton" style="height: 60px; margin-bottom: 8px;"></div>
        <div class="skeleton" style="height: 60px; margin-bottom: 8px;"></div>
        <div class="skeleton" style="height: 60px;"></div>
      `;

      const commits = await getCommits(8);

      container.innerHTML = commits.map(commit => `
        <a href="${commit.html_url}" target="_blank" rel="noopener" class="commit-item" style="
          display: flex;
          align-items: flex-start;
          gap: var(--space-sm);
          padding: var(--space-sm) var(--space-md);
          border-bottom: 1px solid var(--border-secondary);
          text-decoration: none;
          color: var(--text-primary);
          transition: background-color var(--transition-fast);
        " onmouseover="this.style.backgroundColor='var(--accent-glow)'" onmouseout="this.style.backgroundColor='transparent'">
          <img src="${commit.author?.avatar_url || commit.committer?.avatar_url || ''}" 
               alt="" 
               style="width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0; margin-top: 2px;"
               loading="lazy"
               onerror="this.style.display='none'" />
          <div style="flex: 1; min-width: 0;">
            <div style="font-size: var(--text-sm); font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${SecurityManager.sanitize(commit.commit.message.split('\n')[0])}
            </div>
            <div style="font-size: var(--text-xs); color: var(--text-tertiary); font-family: var(--font-mono); margin-top: 2px;">
              ${SecurityManager.sanitize(commit.commit.author.name)} · ${formatDate(commit.commit.author.date)} · 
              <span style="color: var(--accent-primary);">${commit.sha.substring(0, 7)}</span>
            </div>
          </div>
        </a>
      `).join('');

    } catch (error) {
      container.innerHTML = `
        <div style="padding: var(--space-md); text-align: center; color: var(--text-tertiary);">
          <p>No se pudieron cargar los commits</p>
        </div>
      `;
    }
  }

  return { init, loadCommits, loadFileTree, loadFileContent };
})();
