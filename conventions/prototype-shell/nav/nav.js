/**
 * RHOAI sidebar navigation -- reusable JS extracted from the verified
 * skills-catalog prototype v1.
 *
 * Provides:
 *   toggleNavSection(btn)  -- expand/collapse a nav section
 *   expandNav(li, expand)  -- programmatic expand/collapse helper
 *   navigateTo(view)       -- switch active view + highlight the correct nav item
 *   DOMContentLoaded init  -- sets inline display on all expandable subnavs
 */

// ===== NAV TOGGLE =====
function toggleNavSection(btn) {
  const item = btn.closest('.pf-v6-c-nav__item.pf-m-expandable');
  const subnav = item.querySelector(':scope > .pf-v6-c-nav__subnav');
  const isExpanded = item.classList.contains('pf-m-expanded');
  if (isExpanded) {
    item.classList.remove('pf-m-expanded');
    btn.setAttribute('aria-expanded', 'false');
    if (subnav) subnav.style.display = 'none';
  } else {
    item.classList.add('pf-m-expanded');
    btn.setAttribute('aria-expanded', 'true');
    if (subnav) {
      subnav.style.display = 'block';
      // Ensure child subnavs respect their own collapsed state
      subnav.querySelectorAll('.pf-v6-c-nav__item.pf-m-expandable').forEach(child => {
        const childSub = child.querySelector(':scope > .pf-v6-c-nav__subnav');
        if (childSub) childSub.style.display = child.classList.contains('pf-m-expanded') ? 'block' : 'none';
      });
    }
  }
}

// ===== EXPAND/COLLAPSE HELPER =====
function expandNav(li, expand) {
  if (!li) return;
  const btn = li.querySelector(':scope > button');
  const sub = li.querySelector(':scope > .pf-v6-c-nav__subnav');
  if (expand) {
    li.classList.add('pf-m-expanded');
    if (btn) btn.setAttribute('aria-expanded', 'true');
    if (sub) {
      sub.style.display = 'block';
      sub.querySelectorAll('.pf-v6-c-nav__item.pf-m-expandable').forEach(child => {
        const childSub = child.querySelector(':scope > .pf-v6-c-nav__subnav');
        if (childSub) childSub.style.display = child.classList.contains('pf-m-expanded') ? 'block' : 'none';
      });
    }
  } else {
    li.classList.remove('pf-m-expanded');
    if (btn) btn.setAttribute('aria-expanded', 'false');
    if (sub) sub.style.display = 'none';
  }
}

// ===== VIEW NAVIGATION =====
function navigateTo(view) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const viewEl = document.getElementById('view-' + view);
  if (viewEl) viewEl.classList.add('active');

  // Clear all nav highlights
  document.querySelectorAll('.app-sidebar .pf-v6-c-nav__link').forEach(l => l.classList.remove('pf-m-current'));
  document.querySelectorAll('.app-sidebar .pf-v6-c-nav__item').forEach(i => i.classList.remove('pf-m-current'));

  // Collapse Settings and its sub-sections by default
  const settingsItem = document.getElementById('nav-settings');
  const skillResources = document.getElementById('nav-skill-resources');

  // Highlight the correct nav item based on view
  if (view === 'catalog' || view === 'detail') {
    expandNav(settingsItem, false);
    expandNav(skillResources, false);

    const skillsLink = document.querySelector('[data-nav="catalog"]');
    if (skillsLink) {
      skillsLink.classList.add('pf-m-current');
      skillsLink.closest('.pf-v6-c-nav__item').classList.add('pf-m-current');
      const aiHubGroup = skillsLink.closest('.pf-v6-c-nav__subnav')?.closest('.pf-v6-c-nav__item.pf-m-expandable');
      if (aiHubGroup) {
        aiHubGroup.classList.add('pf-m-current');
        expandNav(aiHubGroup, true);
      }
    }
  } else if (view === 'admin') {
    const aiHubItem = document.getElementById('nav-ai-hub');
    expandNav(aiHubItem, true);
    expandNav(settingsItem, true);
    if (settingsItem) settingsItem.classList.add('pf-m-current');
    expandNav(skillResources, true);
    if (skillResources) skillResources.classList.add('pf-m-current');

    const adminLink = document.querySelector('[data-nav="admin"]');
    if (adminLink) {
      adminLink.classList.add('pf-m-current');
      adminLink.closest('.pf-v6-c-nav__item').classList.add('pf-m-current');
    }
  }

  window.scrollTo(0, 0);
}

// ===== INIT =====
if (!window.__navInitialized) {
  window.__navInitialized = true;
  document.addEventListener('DOMContentLoaded', () => {
    // Initialize nav: set inline display on ALL expandable subnavs
    // Walk the tree top-down: if a parent is collapsed, children inherit hidden
    function initNavDisplay(container) {
      const items = container.querySelectorAll(':scope > .pf-v6-c-nav__item.pf-m-expandable');
      items.forEach(li => {
        const sub = li.querySelector(':scope > .pf-v6-c-nav__subnav');
        if (!sub) return;
        const expanded = li.classList.contains('pf-m-expanded');
        sub.style.display = expanded ? 'block' : 'none';
        if (expanded) {
          const innerList = sub.querySelector(':scope > .pf-v6-c-nav__list');
          if (innerList) initNavDisplay(innerList);
        }
      });
    }
    const navRoot = document.querySelector('.pf-v6-c-nav > .pf-v6-c-nav__list');
    if (navRoot) initNavDisplay(navRoot);
  });
}
