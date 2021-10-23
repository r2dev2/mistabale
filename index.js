const cursor = document.querySelector('.cursor');
window.addEventListener('mousemove', e => {
  const x = e.clientX - 15;
  const y = e.clientY - 17;
  cursor.style = `transform: translate(${x}px, ${y}px)`;
  cursor.classList.add('active');
  cursor.classList[
    document.querySelectorAll('a.focussed,a:hover').length ? 'add' : 'remove'
  ]('focussed');
});

const on = (el, event, success, failure) => window.addEventListener(event, e => {
  const { x, y, width, height } = el.getBoundingClientRect();
  const inBetween = (start, d, num) => start <= num && num <= start + d;
  if (inBetween(x, width, e.clientX) && inBetween(y, height, e.clientY)) {
    e.preventDefault();
    return success(el);
  }
  return failure(el);
});

const addFocussed = el => el.classList.add('focussed');
const rmFocussed = el => el.classList.remove('focussed');
const navigateTo = a => window.location = a;
document.querySelectorAll('a').forEach(a => {
  on(a, 'mousemove', addFocussed, rmFocussed);
  on(a, 'contextmenu', () => { }, () => { });
  on(a, 'click', navigateTo, () => { });
});
