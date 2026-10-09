(() => {
  const titles = {fr: 'DIALOGIA Montréal 2026 — Colloque scientifique', en: 'DIALOGIA Montréal 2026 — Scientific conference'};
  const headers = [...document.querySelectorAll('.header')];
  function closeMenus(returnFocus = false) {
    headers.forEach(header => {
      if (!header.hasAttribute('data-menu-open')) return;
      const toggle = header.querySelector('[data-menu-toggle]');
      header.removeAttribute('data-menu-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', toggle.dataset.openLabel);
      if (returnFocus) toggle.focus({preventScroll: true});
    });
  }
  headers.forEach(header => {
    const toggle = header.querySelector('[data-menu-toggle]');
    toggle.addEventListener('click', () => {
      const willOpen = !header.hasAttribute('data-menu-open');
      closeMenus();
      if (willOpen) {
        header.setAttribute('data-menu-open', '');
        toggle.setAttribute('aria-expanded', 'true');
        toggle.setAttribute('aria-label', toggle.dataset.closeLabel);
        header.querySelector('.section-nav a').focus({preventScroll: true});
      }
    });
    header.querySelector('[data-menu]').addEventListener('click', event => {
      const link = event.target.closest('a');
      if (!link) return;
      const wasOpen = header.hasAttribute('data-menu-open');
      closeMenus(wasOpen);
      if (wasOpen && link.hash && link.origin === location.origin && link.pathname === location.pathname) {
        document.getElementById(link.hash.slice(1))?.focus({preventScroll: true});
      }
    });
    header.addEventListener('focusout', event => {
      if (event.relatedTarget && !header.contains(event.relatedTarget)) closeMenus();
    });
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenus(true);
  });
  document.addEventListener('pointerdown', event => {
    if (!event.target.closest('.header')) closeMenus();
  });
  window.matchMedia('(min-width: 1200px)').addEventListener('change', () => closeMenus());
  function setLanguage(language, updateUrl = true) {
    if (!['fr', 'en'].includes(language)) return;
    closeMenus();
    const previous = document.documentElement.lang;
    document.documentElement.lang = language;
    document.title = titles[language];
    const description = language === 'fr'
      ? 'Dialogue interreligieux « assisté par » et « en dialogue avec » l’IA. 19–21 OCTOBRE 2026 · UNIVERSITÉ DE MONTRÉAL'
      : 'Interreligious Dialogue “Assisted by” and “in Dialogue with” AI. 19–21 OCTOBER 2026 · UNIVERSITY OF MONTREAL';
    document.querySelector('meta[name="description"]').content = description;
    document.querySelectorAll('[data-language]').forEach(section => {
      section.hidden = section.dataset.language !== language;
    });
    document.querySelectorAll(`[data-language="${previous}"] details[id]`).forEach(detail => {
      const counterpart = document.getElementById(detail.id.replace(new RegExp(`-${previous}$`), `-${language}`));
      if (counterpart) counterpart.open = detail.open;
    });
    if (updateUrl) {
      const url = new URL(location.href);
      url.searchParams.set('lang', language);
      url.hash = url.hash.replace(/-(fr|en)$/, `-${language}`);
      history.pushState({}, '', url);
      const focusTarget = document.querySelector(`[data-language="${language}"] [data-set-language="${language}"]`);
      focusTarget?.focus({preventScroll: true});
    }
  }
  document.querySelectorAll('[data-set-language]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      setLanguage(link.dataset.setLanguage);
    });
  });
  document.querySelectorAll('[data-open-day], [data-open-details]').forEach(link => link.addEventListener('click', () => {
    document.getElementById(link.dataset.openDetails || link.dataset.openDay).open = true;
  }));
  document.querySelectorAll('[data-carousel]').forEach(carousel => {
    const track = carousel.querySelector('.institution-track');
    const cards = [...track.children];
    const previous = carousel.querySelector('[data-carousel-prev]');
    const next = carousel.querySelector('[data-carousel-next]');
    const count = carousel.querySelector('[data-carousel-count]');
    const progress = carousel.querySelector('[data-carousel-progress]');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    function update() {
      if (!track.clientWidth) return;
      const bounds = track.getBoundingClientRect();
      const visible = cards.map((card, index) => ({index, bounds: card.getBoundingClientRect()}))
        .filter(card => card.bounds.right > bounds.left + 5 && card.bounds.left < bounds.right - 5);
      const first = visible[0]?.index ?? 0;
      const last = visible.at(-1)?.index ?? first;
      count.textContent = `${first + 1}${last === first ? '' : '–' + (last + 1)} / ${cards.length}`;
      progress.style.width = `${(last + 1) / cards.length * 100}%`;
      previous.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
    }
    function move(direction) {
      const stride = cards[1].offsetLeft - cards[0].offsetLeft;
      const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      const perPage = Math.max(1, Math.floor((track.clientWidth + gap) / stride));
      track.scrollBy({left: direction * stride * perPage, behavior: reduceMotion.matches ? 'instant' : 'smooth'});
    }
    previous.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    track.addEventListener('scroll', update, {passive: true});
    track.addEventListener('keydown', event => {
      if (event.target !== track) return;
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        move(event.key === 'ArrowLeft' ? -1 : 1);
      } else if (event.key === 'Home' || event.key === 'End') {
        event.preventDefault();
        track.scrollTo({left: event.key === 'Home' ? 0 : track.scrollWidth, behavior: reduceMotion.matches ? 'instant' : 'smooth'});
      }
    });
    new ResizeObserver(update).observe(track);
    update();
  });
  function openHash() {
    const target = document.getElementById(location.hash.slice(1));
    if (target?.matches('details')) target.open = true;
  }
  window.addEventListener('popstate', () => {setLanguage(new URLSearchParams(location.search).get('lang') === 'en' ? 'en' : 'fr', false); openHash();});
  window.addEventListener('hashchange', openHash);
  setLanguage(document.documentElement.lang, false);
  openHash();
})();
