let clientX = null;
let clientY = null;

const cursor = document.querySelector('.cursor');
const focussed = 'a.focussed,a:hover,.resource.focussed';

const updateCursor = (clientX, clientY, scrollX, scrollY) => {
  if ([clientX, clientY].includes(null)) return;
  const x = clientX - 15 + scrollX;
  const y = clientY - 17 + scrollY;
  cursor.style = `transform: translate(${x}px, ${y}px)`;
  cursor.classList.add('active');
  cursor.classList[
    document.querySelectorAll(focussed).length ? 'add' : 'remove'
  ]('focussed');
};

window.addEventListener('mousemove', e => updateCursor(
  clientX = e.clientX, clientY = e.clientY, window.scrollX, window.scrollY
));

window.addEventListener('scroll', () => updateCursor(
  clientX, clientY, window.scrollX, window.scrollY
));

const on = (el, event, success, failure) => window.addEventListener(event, e => {
  const { x, y, width, height } = el.getBoundingClientRect();
  const inBetween = (start, d, num) => start <= num && num <= start + d;
  if (inBetween(x, width, e.clientX) && inBetween(y, height, e.clientY))
  {
    e.preventDefault();
    return success(el);
  }
  return failure(el);
});

const addFocussed = el => el.classList.add('focussed');
const rmFocussed = el => el.classList.remove('focussed');
const navigateTo = a => window.location.href = a?.href ?? a.querySelector('a')?.href;
document.querySelectorAll('a,.resource').forEach(a => {
  on(a, 'mousemove', addFocussed, rmFocussed);
  on(a, 'contextmenu', () => { }, () => { });
  on(a, 'click', navigateTo, () => { });
});
