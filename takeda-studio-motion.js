// Decorative motion never hides or delays the permanent research links.
(() => {
  const stage = document.querySelector('.studio-visual');
  if (!stage) return;
  const words = [...stage.querySelectorAll('[data-studio-word]')];
  const count = stage.querySelector('[data-studio-count]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let onScreen = true;
  let timer;
  const sync = () => {
    clearInterval(timer);
    const paused = reduced.matches || document.hidden || !onScreen;
    stage.classList.toggle('motion-paused', paused);
    if (paused) return;
    timer = setInterval(() => {
      words[current].classList.remove('is-active');
      current = (current + 1) % words.length;
      words[current].classList.add('is-active');
      count.textContent = String(current + 1).padStart(2, '0') + ' / 06';
    }, 4800);
  };
  new IntersectionObserver(([entry]) => { onScreen = entry.isIntersecting; sync(); }, {threshold:0}).observe(stage);
  reduced.addEventListener('change', sync);
  document.addEventListener('visibilitychange', sync);
  sync();
})();
