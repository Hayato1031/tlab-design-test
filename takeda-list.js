// Progressive enhancement: every sample article remains visible without JavaScript.
const filters = document.querySelector('.post-filters');
if (filters) {
  const posts = [...document.querySelectorAll('.post-item')];
  const count = document.querySelector('.post-count');
  filters.hidden = false;
  filters.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    for (const item of filters.querySelectorAll('button')) {
      item.setAttribute('aria-pressed', String(item === button));
    }
    for (const post of posts) {
      post.hidden = button.dataset.filter !== 'all' && post.dataset.category !== button.dataset.filter;
    }
    count.textContent = posts.filter(post => !post.hidden).length + count.dataset.suffix;
  });
}
