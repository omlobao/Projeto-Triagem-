// ========================================
// PROJETO TRIAGEM — Main JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', () => {
  // ---------- Sidebar Toggle (Mobile) ----------
  const menuToggle = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.querySelector('.sidebar-overlay');

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      if (overlay) overlay.classList.toggle('active');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar.classList.remove('open');
      overlay.classList.remove('active');
    });
  }

  // ---------- Auto-dismiss Messages ----------
  const messages = document.querySelectorAll('.message');
  messages.forEach((msg, index) => {
    // Stagger the dismissal
    setTimeout(() => {
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(-10px)';
      setTimeout(() => msg.remove(), 300);
    }, 4000 + (index * 500));
  });

  // Close message on click
  document.querySelectorAll('.close-msg').forEach(btn => {
    btn.addEventListener('click', () => {
      const msg = btn.closest('.message');
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(-10px)';
      setTimeout(() => msg.remove(), 300);
    });
  });

  // ---------- CPF Mask ----------
  document.querySelectorAll('input[name="cpf"]').forEach(input => {
    input.addEventListener('input', (e) => {
      let v = e.target.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      if (v.length > 9) {
        v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
      } else if (v.length > 6) {
        v = v.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
      } else if (v.length > 3) {
        v = v.replace(/(\d{3})(\d{1,3})/, '$1.$2');
      }
      e.target.value = v;
    });
  });

  // ---------- Phone Mask ----------
  document.querySelectorAll('input[name="telefone"], input[name="numero_telefone"]').forEach(input => {
    input.addEventListener('input', (e) => {
      let v = e.target.value.replace(/\D/g, '');
      if (v.length > 11) v = v.slice(0, 11);
      if (v.length > 6) {
        v = v.replace(/(\d{2})(\d{5})(\d{1,4})/, '($1) $2-$3');
      } else if (v.length > 2) {
        v = v.replace(/(\d{2})(\d{1,5})/, '($1) $2');
      }
      e.target.value = v;
    });
  });

  // ---------- Active Navigation ----------
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

  // ---------- Confirm Delete ----------
  document.querySelectorAll('[data-confirm]').forEach(el => {
    el.addEventListener('click', (e) => {
      if (!confirm(el.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // ---------- Form Enhancements ----------
  // Auto-style Django form fields
  document.querySelectorAll('.django-form input, .django-form select, .django-form textarea').forEach(field => {
    if (!field.closest('.form-group')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'form-group';
      field.parentNode.insertBefore(wrapper, field);

      // Move label if exists
      const label = field.previousElementSibling;
      if (label && label.tagName === 'LABEL') {
        wrapper.appendChild(label);
      }

      wrapper.appendChild(field);

      // Move help text / errors
      const next = wrapper.nextElementSibling;
      if (next && (next.classList.contains('helptext') || next.classList.contains('errorlist'))) {
        wrapper.appendChild(next);
      }
    }
  });

  // ========================================
  // Keyboard Shortcuts
  // ========================================

  const shortcuts = [
    { keys: 'F2', label: 'Nova Triagem',           url: '/triagem/nova/' },
    { keys: 'F3', label: 'Novo Atendimento',       url: '/atendimento/novo/' },
    { keys: 'F4', label: 'Dashboard',               url: '/' },
    { keys: 'F5', label: 'Lista de Triagens',       url: '/triagem/' },
    { keys: 'F6', label: 'Lista de Atendimentos',   url: '/atendimento/' },
    { keys: 'F7', label: 'Painel Administrativo',   url: '/painel/' },
    { keys: 'F8', label: 'Mostrar atalhos',          url: null },
  ];

  // Build the modal
  const modal = document.createElement('div');
  modal.id = 'shortcuts-modal';
  modal.innerHTML = `
    <div class="shortcuts-backdrop"></div>
    <div class="shortcuts-panel">
      <div class="shortcuts-header">
        <div class="shortcuts-title">
          <i class="fas fa-keyboard"></i>
          <h3>Atalhos do Teclado</h3>
        </div>
        <button class="shortcuts-close" id="shortcuts-close" type="button">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="shortcuts-body">
        ${shortcuts.map(s => `
          <div class="shortcut-row">
            <span class="shortcut-label">${s.label}</span>
            <span class="shortcut-keys"><kbd>${s.keys}</kbd></span>
          </div>
        `).join('')}
      </div>
      <div class="shortcuts-footer">
        <span>Pressione <kbd>F8</kbd> ou clique no botão <kbd><i class="fas fa-keyboard"></i></kbd> para exibir</span>
      </div>
    </div>
  `;
  document.body.appendChild(modal);

  // FAB button
  const fab = document.createElement('button');
  fab.id = 'shortcuts-fab';
  fab.className = 'shortcuts-fab';
  fab.title = 'Atalhos do teclado (F8)';
  fab.innerHTML = '<i class="fas fa-keyboard"></i>';
  // Only show FAB on authenticated pages (those with sidebar)
  if (document.querySelector('.sidebar')) {
    document.body.appendChild(fab);
  }

  function openShortcuts()  { modal.classList.add('open'); }
  function closeShortcuts() { modal.classList.remove('open'); }

  fab.addEventListener('click', openShortcuts);
  modal.querySelector('.shortcuts-backdrop').addEventListener('click', closeShortcuts);
  modal.querySelector('#shortcuts-close').addEventListener('click', closeShortcuts);

  // F-key shortcut map
  const fKeyMap = {
    'F2': '/triagem/nova/',
    'F3': '/atendimento/novo/',
    'F4': '/',
    'F5': '/triagem/',
    'F6': '/atendimento/',
    'F7': '/painel/',
  };

  // Listen for keyboard shortcuts
  document.addEventListener('keydown', (e) => {
    // F8 — toggle shortcuts modal (always works)
    if (e.key === 'F8') {
      e.preventDefault();
      modal.classList.contains('open') ? closeShortcuts() : openShortcuts();
      return;
    }

    // Escape — close modal
    if (e.key === 'Escape') {
      closeShortcuts();
      return;
    }

    // F-key navigation shortcuts
    if (fKeyMap[e.key]) {
      e.preventDefault();
      window.location.href = fKeyMap[e.key];
    }
  });
});
