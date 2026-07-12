// nav.js - Shared navigation for MCP Ecosystem Knowledge Hub
// Generates sidebar, header, breadcrumbs, quick-jump, and staleness indicators

const SITE_MAP = [
  { section: 'Understand It', id: 'understand', pages: [
    { title: 'What Is the MCP Registry?', path: 'understand/what-is-the-registry.html' },
    { title: 'Data Model', path: 'understand/data-model.html' },
    { title: 'Jobs to be Done', path: 'understand/jobs-to-be-done.html' },
  ]},
  { section: 'Sell It', id: 'sell', pages: [
    { title: 'The Governance Story', path: 'sell/governance-story.html' },
  ]},
  { section: 'Build It', id: 'build', pages: [
    { title: 'MVP Scope & Prototype', path: 'build/mvp-scope-prototype.html' },
  ]},
  { section: 'Govern It', id: 'govern', pages: [
    { title: 'Lifecycle & Governance', path: 'govern/lifecycle-governance.html' },
    { title: 'Integrations', path: 'govern/integrations.html' },
  ]},
  { section: 'Plan It', id: 'plan', pages: [
    { title: 'Roadmap', path: 'plan/roadmap.html' },
    { title: 'Jira Tracker (Strats)', path: 'plan/jira-tracker.html' },
    { title: 'Gaps & Open Questions', path: 'plan/gaps-open-questions.html' },
  ]},
];

// Special pages not in sections
const SPECIAL_PAGES = [
  { title: 'Home', path: 'index.html' },
  { title: 'Quick Reference', path: 'reference.html' },
];

const HUB_NETWORK = [
  { title: '🏠 MCP Ecosystem Hub', path: '../../mcp-ecosystem/hub/' },
  { title: '🔌 MCP Gateway Hub', path: '../../mcp-gateway/rhcl/' },
  { title: '📦 MCP Catalog Hub', path: '../../mcp-catalog/hub/' },
  { title: '⚙️ MCP Lifecycle Operator Hub', path: '../../mcp-lifecycle-operator/hub/' },
  { title: '📋 MCP Registry Hub', path: '../../mcp-registry/hub/', self: true },
];

/**
 * Sidebar section collapse state, persisted per browser tab via sessionStorage
 * so expand/collapse choices survive navigation between pages.
 */
const SIDEBAR_STATE_KEY = 'registry-hub-sidebar-state';

function getSidebarState() {
  try {
    return JSON.parse(sessionStorage.getItem(SIDEBAR_STATE_KEY) || '{}');
  } catch (e) {
    return {};
  }
}

function setSidebarSectionState(sectionId, expanded) {
  try {
    const state = getSidebarState();
    state[sectionId] = expanded;
    sessionStorage.setItem(SIDEBAR_STATE_KEY, JSON.stringify(state));
  } catch (e) {
    // sessionStorage unavailable (e.g. private browsing); state just won't persist
  }
}

/**
 * Determines the base path prefix for linking to root-level resources
 * from the current page.
 * @returns {string} '../' if in a subdirectory, './' if at root
 */
function getBasePath() {
  const path = window.location.pathname;
  const parts = path.split('/');
  const dir = parts[parts.length - 2];

  // Check if we're in a section subdirectory
  if (['understand', 'sell', 'build', 'govern', 'plan'].includes(dir)) {
    return '../';
  }
  return './';
}

/**
 * Finds the current page in the site map by matching the pathname.
 * Handles both local file:// paths and GitHub Pages paths.
 * @returns {Object|null} { section, sectionId, page } or null if not found
 */
function findCurrentPage() {
  const path = window.location.pathname;
  const pathParts = path.split('/');
  const filename = pathParts[pathParts.length - 1];
  const dir = pathParts[pathParts.length - 2];

  // Try to match as section/page.html
  const fullPath = `${dir}/${filename}`;
  for (const section of SITE_MAP) {
    for (const page of section.pages) {
      if (page.path === fullPath || page.path.endsWith(filename)) {
        return { section: section.section, sectionId: section.id, page };
      }
    }
  }

  // Try to match special pages (index.html, reference.html)
  for (const specialPage of SPECIAL_PAGES) {
    if (specialPage.path === filename || path.endsWith(filename)) {
      return { section: null, sectionId: null, page: specialPage };
    }
  }

  return null;
}

/**
 * Builds the sidebar HTML and injects it into #hub-sidebar.
 * Uses BEM classes from styles.css: hub-sidebar__nav, hub-sidebar__section, etc.
 */
function buildSidebar() {
  const sidebar = document.getElementById('hub-sidebar');
  if (!sidebar) return;

  const current = findCurrentPage();
  const basePath = getBasePath();
  const sidebarState = getSidebarState();

  let html = '<nav class="hub-sidebar__nav"><ul>';

  // Add home link
  html += `<li class="hub-sidebar__section">`;
  html += `<a href="${basePath}index.html" class="hub-sidebar__link ${current?.page?.path === 'index.html' ? 'active' : ''}">🏠 Home</a>`;
  html += `</li>`;

  // Add each section with its pages
  for (const section of SITE_MAP) {
    const isCurrentSection = current?.sectionId === section.id;
    const isExpanded = Object.prototype.hasOwnProperty.call(sidebarState, section.id)
      ? sidebarState[section.id]
      : isCurrentSection;
    html += `<li class="hub-sidebar__section">`;
    html += `<div class="hub-sidebar__section-title" data-section="${section.id}" style="cursor: pointer;">`;
    html += `<span class="section-toggle">${isExpanded ? '▼' : '▶'}</span> `;
    html += `${section.section}`;
    html += `</div>`;
    html += `<ul class="section-pages" data-section="${section.id}" style="display: ${isExpanded ? 'block' : 'none'}; list-style: none;">`;

    for (const page of section.pages) {
      const isActive = current?.page?.path === page.path;
      html += `<li><a href="${basePath}${page.path}" class="hub-sidebar__link ${isActive ? 'active' : ''}">${page.title}</a></li>`;
    }

    html += `</ul>`;
    html += `</li>`;
  }

  // Add reference link
  html += `<li class="hub-sidebar__section">`;
  html += `<a href="${basePath}reference.html" class="hub-sidebar__link ${current?.page?.path === 'reference.html' ? 'active' : ''}">📚 Quick Reference</a>`;
  html += `</li>`;

  // Add Hub Network section
  html += `<li class="hub-sidebar__section" style="margin-top: var(--space-xl); border-top: 1px solid var(--border-subtle); padding-top: var(--space-lg);">`;
  html += `<div class="hub-sidebar__section-title">Hub Network</div>`;
  html += `<ul style="list-style: none; margin: 0; padding: 0;">`;
  for (const hub of HUB_NETWORK) {
    if (hub.self) {
      html += `<li><span class="hub-sidebar__link active" style="opacity: 0.5; cursor: default;">${hub.title} (current)</span></li>`;
    } else if (hub.comingSoon) {
      html += `<li><span class="hub-sidebar__link" style="opacity: 0.4; cursor: default;">${hub.title} (coming soon)</span></li>`;
    } else {
      html += `<li><a href="${hub.path}" class="hub-sidebar__link">${hub.title}</a></li>`;
    }
  }
  html += `</ul></li>`;

  html += '</ul></nav>';

  sidebar.innerHTML = html;

  // Add toggle handlers for expandable sections
  document.querySelectorAll('.hub-sidebar__section-title[data-section]').forEach(header => {
    header.addEventListener('click', () => {
      const sectionId = header.getAttribute('data-section');
      const pages = document.querySelector(`.section-pages[data-section="${sectionId}"]`);
      const toggle = header.querySelector('.section-toggle');
      const nowExpanded = pages.style.display === 'none';

      if (nowExpanded) {
        pages.style.display = 'block';
        toggle.textContent = '▼';
      } else {
        pages.style.display = 'none';
        toggle.textContent = '▶';
      }
      setSidebarSectionState(sectionId, nowExpanded);
    });
  });
}

/**
 * Builds the header HTML with site title, section tabs, and quick-jump.
 * Uses BEM classes from styles.css: hub-header__title, hub-header__tabs, hub-header__tab
 */
function buildHeader() {
  const header = document.getElementById('hub-header');
  if (!header) return;

  const current = findCurrentPage();
  const basePath = getBasePath();

  let html = '';

  // Mobile hamburger menu (styled inline since CSS doesn't have it yet)
  html += '<button class="mobile-menu-toggle" aria-label="Toggle navigation" style="display: none; background: none; border: none; color: var(--text-primary); font-size: 1.5rem; cursor: pointer; padding: 0.5rem;">☰</button>';

  // Site title
  html += `<div class="hub-header__title">`;
  html += `<a href="${basePath}index.html" style="text-decoration: none; color: inherit;">`;
  html += `<span class="hub-header__logo">MCP</span> Registry`;
  html += `</a>`;
  html += `</div>`;

  // Section tabs
  html += '<nav class="hub-header__tabs">';
  for (const section of SITE_MAP) {
    const isActive = current?.sectionId === section.id;
    const firstPage = section.pages[0];
    html += `<a href="${basePath}${firstPage.path}" class="hub-header__tab ${isActive ? 'active' : ''}">${section.section}</a>`;
  }
  html += '</nav>';

  // Quick-jump dropdown (styled inline since CSS doesn't have it yet)
  html += '<select class="quick-jump-select" aria-label="Quick jump to page" style="background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 0.5rem; border-radius: 4px; font-family: var(--font-text); font-size: var(--fs-body);">';
  html += '<option value="">Jump to...</option>';

  html += '<optgroup label="General">';
  for (const specialPage of SPECIAL_PAGES) {
    const isSelected = current?.page?.path === specialPage.path;
    html += `<option value="${basePath}${specialPage.path}" ${isSelected ? 'selected' : ''}>${specialPage.title}</option>`;
  }
  html += '</optgroup>';

  for (const section of SITE_MAP) {
    html += `<optgroup label="${section.section}">`;
    for (const page of section.pages) {
      const isSelected = current?.page?.path === page.path;
      html += `<option value="${basePath}${page.path}" ${isSelected ? 'selected' : ''}>${page.title}</option>`;
    }
    html += '</optgroup>';
  }

  html += '</select>';

  header.innerHTML = html;

  // Add quick-jump handler
  const select = header.querySelector('.quick-jump-select');
  select.addEventListener('change', (e) => {
    if (e.target.value) {
      window.location.href = e.target.value;
    }
  });

  // Add mobile menu handler
  const menuToggle = header.querySelector('.mobile-menu-toggle');
  const sidebar = document.getElementById('hub-sidebar');

  // Show hamburger on mobile
  const mediaQuery = window.matchMedia('(max-width: 900px)');
  function handleMobile(e) {
    if (e.matches) {
      menuToggle.style.display = 'block';
    } else {
      menuToggle.style.display = 'none';
      sidebar.classList.remove('open');
    }
  }
  mediaQuery.addEventListener('change', handleMobile);
  handleMobile(mediaQuery);

  menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });
}

/**
 * Builds the breadcrumb navigation.
 * Styles inline since CSS doesn't have breadcrumb classes yet.
 */
function buildBreadcrumb() {
  const breadcrumb = document.querySelector('.breadcrumb');
  if (!breadcrumb) return;

  const current = findCurrentPage();
  const basePath = getBasePath();

  // Apply inline styles for breadcrumb (until CSS is added)
  breadcrumb.style.fontSize = 'var(--fs-small)';
  breadcrumb.style.color = 'var(--text-muted)';
  breadcrumb.style.marginBottom = 'var(--space-lg)';

  let html = `<a href="${basePath}index.html" style="color: var(--rh-blue-light); text-decoration: none;">Home</a>`;

  if (current?.section) {
    html += ` <span style="margin: 0 0.5rem;">›</span> `;

    // Link to first page in section
    const sectionObj = SITE_MAP.find(s => s.id === current.sectionId);
    if (sectionObj) {
      const firstPage = sectionObj.pages[0];
      html += `<a href="${basePath}${firstPage.path}" style="color: var(--rh-blue-light); text-decoration: none;">${current.section}</a>`;
    }

    if (current.page) {
      html += ` <span style="margin: 0 0.5rem;">›</span> `;
      html += `<span style="color: var(--text-primary);">${current.page.title}</span>`;
    }
  } else if (current?.page && current.page.path !== 'index.html') {
    html += ` <span style="margin: 0 0.5rem;">›</span> `;
    html += `<span style="color: var(--text-primary);">${current.page.title}</span>`;
  }

  breadcrumb.innerHTML = html;
}

/**
 * Computes staleness indicator color based on the data-verified attribute.
 */
function computeStaleness() {
  const footer = document.querySelector('.page-footer');
  if (!footer) return;

  const verifiedDate = footer.getAttribute('data-verified');
  if (!verifiedDate) return;

  const indicator = footer.querySelector('.staleness-indicator');
  if (!indicator) return;

  try {
    const verified = new Date(verifiedDate);
    const now = new Date();
    const daysSince = Math.floor((now - verified) / (1000 * 60 * 60 * 24));

    // Remove all staleness classes
    indicator.classList.remove('staleness-green', 'staleness-yellow', 'staleness-red');

    // Add appropriate class based on age
    if (daysSince < 14) {
      indicator.classList.add('staleness-green');
    } else if (daysSince <= 28) {
      indicator.classList.add('staleness-yellow');
    } else {
      indicator.classList.add('staleness-red');
    }

    // Visible label alongside the colored dot (::before, styles.css)
    let label;
    if (daysSince <= 0) {
      label = 'Verified today';
    } else if (daysSince === 1) {
      label = 'Verified 1 day ago';
    } else {
      label = `Verified ${daysSince} days ago`;
    }
    indicator.textContent = label;
  } catch (e) {
    console.error('Invalid data-verified date:', verifiedDate, e);
  }
}

/**
 * Initialize navigation on page load.
 */
function initNav() {
  buildSidebar();
  buildHeader();
  buildBreadcrumb();
  computeStaleness();
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initNav);
} else {
  initNav();
}
