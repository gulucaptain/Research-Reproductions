'use strict';
(() => {
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const studies = [...document.querySelectorAll('.study')];
  const input = document.querySelector('#search');
  const count = document.querySelector('.count');
  const empty = document.querySelector('.empty');
  const params = new URLSearchParams(location.search);
  const categories = buttons.map(button => button.dataset.filter);
  let area = categories.includes(params.get('area')) ? params.get('area') : 'all';
  input.value = params.get('q') || '';

  function apply(updateUrl = true) {
    const query = input.value.trim().toLocaleLowerCase();
    let shown = 0;
    for (const study of studies) {
      const terms = query.split(/\s+/).filter(Boolean);
      const text = study.textContent.toLocaleLowerCase();
      study.hidden = !(area === 'all' || study.dataset.category === area) || !terms.every(term => text.includes(term));
      if (!study.hidden) shown++;
    }
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === area)));
    count.textContent = query || area !== 'all' ? `${shown} of ${studies.length} studies` : `${shown} studies`;
    empty.hidden = shown !== 0;
    if (updateUrl) {
      const url = new URL(location.href);
      area === 'all' ? url.searchParams.delete('area') : url.searchParams.set('area', area);
      input.value.trim() ? url.searchParams.set('q', input.value.trim()) : url.searchParams.delete('q');
      history.replaceState(null, '', url);
    }
  }
  function reset() {
    area = 'all';
    input.value = '';
    apply();
  }
  buttons.forEach(button => button.addEventListener('click', () => {
    area = button.dataset.filter;
    apply();
  }));
  input.addEventListener('input', () => apply());
  document.querySelector('#reset-filters').addEventListener('click', reset);
  document.querySelector('#empty-reset').addEventListener('click', () => { reset(); input.focus(); });
  const links = [...document.querySelectorAll('.contents a')];
  links.forEach(link => link.addEventListener('click', reset));
  function showLinkedStudy() {
    const target = document.getElementById(location.hash.slice(1));
    if (target?.classList.contains('study') && target.hidden) reset();
  }
  window.addEventListener('hashchange', showLinkedStudy);
  window.addEventListener('popstate', () => {
    const current = new URLSearchParams(location.search);
    area = categories.includes(current.get('area')) ? current.get('area') : 'all';
    input.value = current.get('q') || '';
    apply(false);
    showLinkedStudy();
  });
  apply(false);
  showLinkedStudy();

  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) links.forEach(link => link.setAttribute('aria-current', String(link.hash === '#' + entry.target.id)));
    }
  }, { rootMargin: '-10% 0px -60% 0px' });
  studies.forEach(study => observer.observe(study));

  const dialog = document.querySelector('#figure-dialog');
  const close = document.querySelector('.dialog-close');
  let trigger;
  document.querySelectorAll('[data-figure]').forEach(button => button.addEventListener('click', () => {
    if (typeof dialog.showModal !== 'function') { window.open(button.dataset.figure, '_blank', 'noopener'); return; }
    trigger = button;
    document.querySelector('#figure-title').textContent = button.dataset.name + ' · local result';
    document.querySelector('#figure-caption').textContent = button.dataset.caption;
    dialog.querySelector('img').src = button.dataset.figure;
    dialog.querySelector('img').alt = button.dataset.caption;
    dialog.showModal();
    close.focus();
  }));
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => trigger?.focus());
})();
