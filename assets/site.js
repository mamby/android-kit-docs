(() => {
  const menu = document.querySelector('.mobile-nav');
  const narrow = window.matchMedia('(max-width: 850px)');
  const updateMenu = () => { menu.open = !narrow.matches; };
  updateMenu();
  narrow.addEventListener('change', updateMenu);

  document.querySelectorAll('.content table').forEach(table => {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-scroll';
    wrapper.tabIndex = 0;
    wrapper.setAttribute('role', 'region');
    wrapper.setAttribute('aria-label', 'Scrollable table');
    table.before(wrapper);
    wrapper.append(table);
  });

  const input = document.querySelector('#site-search');
  const results = document.querySelector('#search-results');
  const status = document.querySelector('#search-status');
  let indexPromise;
  let revision = 0;
  const close = () => {
    results.hidden = true;
    input.setAttribute('aria-expanded', 'false');
  };
  const getIndex = () => {
    if (!indexPromise) {
      indexPromise = fetch(document.body.dataset.searchUrl).then(response => {
        if (!response.ok) throw new Error('Search unavailable');
        return response.json();
      }).catch(error => {
        indexPromise = undefined;
        throw error;
      });
    }
    return indexPromise;
  };
  const search = async () => {
    const current = ++revision;
    const query = input.value.trim().toLocaleLowerCase('en');
    if (!query) {
      results.replaceChildren();
      status.textContent = '';
      close();
      return;
    }
    try {
      const index = await getIndex();
      if (current !== revision) return;
      const words = query.split(/\s+/);
      const matches = index.map(page => {
        const title = page.title.toLocaleLowerCase('en');
        const content = `${page.title} ${page.description} ${page.content}`.toLocaleLowerCase('en');
        if (!words.every(word => content.includes(word))) return null;
        return { page, score: title === query ? 3 : title.includes(query) ? 2 : words.some(word => title.includes(word)) ? 1 : 0 };
      }).filter(Boolean).sort((a, b) => b.score - a.score || a.page.title.localeCompare(b.page.title)).slice(0, 8);
      results.replaceChildren();
      for (const { page } of matches) {
        const link = document.createElement('a');
        link.href = page.url;
        const title = document.createElement('strong');
        title.textContent = page.title;
        const description = document.createElement('span');
        description.textContent = page.description || page.section;
        link.append(title, description);
        results.append(link);
      }
      if (!matches.length) {
        const message = document.createElement('p');
        message.textContent = 'No matching guides. Try a component or API name.';
        results.append(message);
      }
      results.hidden = false;
      input.setAttribute('aria-expanded', 'true');
      status.textContent = matches.length ? `${matches.length} matching guides.` : 'No matching guides.';
    } catch {
      if (current !== revision) return;
      close();
      status.textContent = 'Search is unavailable. Use the documentation menu.';
    }
  };
  input.addEventListener('input', search);
  input.addEventListener('focus', () => { if (input.value.trim()) search(); });
  input.addEventListener('keydown', event => {
    if (event.key === 'Escape') { ++revision; close(); }
    if (event.key === 'ArrowDown' && !results.hidden) {
      const first = results.querySelector('a');
      if (first) { event.preventDefault(); first.focus(); }
    }
  });
  results.addEventListener('keydown', event => {
    if (event.key === 'Escape') { input.focus(); ++revision; close(); }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.search')) { ++revision; close(); }
  });
})();
