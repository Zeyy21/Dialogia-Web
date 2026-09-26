(() => {
  const titles = {fr: 'DIALOGIA Montréal 2026 — Colloque scientifique', en: 'DIALOGIA Montréal 2026 — Scientific conference'};
  function setLanguage(language, updateUrl = true) {
    if (!['fr', 'en'].includes(language)) return;
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
  document.querySelectorAll('[data-open-day]').forEach(link => link.addEventListener('click', () => {
    document.getElementById(link.dataset.openDay).open = true;
  }));
  function openHash() {
    const target = document.getElementById(location.hash.slice(1));
    if (target?.matches('details')) target.open = true;
  }
  window.addEventListener('popstate', () => {setLanguage(new URLSearchParams(location.search).get('lang') === 'en' ? 'en' : 'fr', false); openHash();});
  window.addEventListener('hashchange', openHash);
  setLanguage(document.documentElement.lang, false);
  openHash();
})();
