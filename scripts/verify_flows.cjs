const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
class Element {
  constructor() { this.handlers = {}; this.children = []; this.dataset = {}; this.attrs = {}; this.value = ''; this.disabled = false; }
  addEventListener(type, fn) { this.handlers[type] = fn; }
  setAttribute(k, v) { this.attrs[k] = v; }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; this.value = ''; }
  add(child) { this.children.push(child); }
  focus() {}
  setCustomValidity(value) { this.validity = value; }
  reportValidity() { return true; }
  querySelector(selector) { return this.children.find(e => selector.includes(e.dataset?.date)); }
}
class FixedDate extends Date {
  constructor(...args) { super(...(args.length ? args : ['2026-10-20T12:30:00Z'])); }
}
const nodes = new Map();
for (const id of ['dialog', 'form', 'days', 'month', 'selected', 'time', 'status', 'prev', 'next', 'name', 'location', 'service', 'details']) nodes.set(`#booking-${id}`, new Element());
nodes.set('.booking_close', new Element());
nodes.get('#booking-dialog').showModal = () => {};
nodes.get('#booking-dialog').close = () => {};
const opener = new Element();
opener.dataset.bookingService = 'Limpeza residencial';
const hourHosts = [new Element(), new Element()];
let opened;
const context = vm.createContext({
  document: {
    querySelector: s => nodes.get(s) || null,
    querySelectorAll: s => s === '[data-booking-open]' ? [opener] : s === '[data-working-hours]' ? hourHosts : [],
    createElement: () => new Element(),
  },
  window: { open: url => { opened = url; } }, Intl, Date: FixedDate,
  Option: class { constructor(label, value) { this.textContent = label; this.value = value; } },
});
vm.runInContext(fs.readFileSync(path.join(root, 'booking.js'), 'utf8'), context);
const slots = (date, now) => Array.from(context.bookingSlots(date, new Date(now)));
assert.equal(context.bookingClock(new Date('2026-10-21T01:30:00Z')).date, '2026-10-20');
assert.deepEqual(slots('2026-10-20', '2026-10-20T12:30:00Z'), ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']);
assert.deepEqual(slots('2026-10-24', '2026-10-20T12:30:00Z'), ['08:00', '09:00', '10:00', '11:00']);
for (const date of ['2026-10-25', '2026-10-19', '2026-02-31']) assert.deepEqual(slots(date, '2026-10-20T12:30:00Z'), []);
assert.deepEqual(slots('2026-10-20', '2026-10-20T21:00:00Z'), []);
for (const host of hourHosts) {
  const table = host.children[0];
  const rows = table.children[2].children;
  assert.equal(rows.length, 7);
  assert.equal(rows[5].children[1].textContent, '08:00–12:00');
  assert.equal(rows[6].children[1].textContent, 'Fechado');
}
opener.handlers.click({ preventDefault() {} });
assert.equal(nodes.get('#booking-service').value, 'Limpeza residencial');
nodes.get('#booking-days').children.find(e => e.dataset.date === '2026-10-21').handlers.click();
nodes.get('#booking-time').value = '09:00';
nodes.get('#booking-name').value = 'Teste & equipe';
nodes.get('#booking-location').value = 'Trindade, Florianópolis';
nodes.get('#booking-details').value = 'Olá! 2 quartos & cozinha.';
nodes.get('#booking-form').handlers.submit({ preventDefault() {} });
const url = new URL(opened), message = url.searchParams.get('text');
assert.equal(url.pathname, '/5548988061017');
for (const value of ['Teste & equipe', 'Limpeza residencial', 'Trindade, Florianópolis', 'Olá! 2 quartos & cozinha.', '09:00', 'horário de Brasília', 'confirmar a disponibilidade']) assert.ok(message.includes(value), value);
assert.equal(nodes.get('#booking-status').children[1].href, opened);
opened = undefined;
nodes.get('#booking-time').value = '23:00';
nodes.get('#booking-form').handlers.submit({ preventDefault() {} });
assert.equal(opened, undefined);

// Product search: accents, category intersection, empty state, and reset.
const search = new Element(), count = new Element(), empty = new Element(), clear = new Element();
const filters = ['Todos', 'Pisos'].map(category => { const e = new Element(); e.dataset.filter = category; e.click = () => e.handlers.click(); return e; });
const products = [['Limpeza geral', 'Álcool perfumado'], ['Pisos', 'Limpa pisos']].map(([category, title]) => ({ dataset: { category }, querySelector: () => ({ textContent: title }) }));
vm.runInNewContext(fs.readFileSync(path.join(root, 'compra.js'), 'utf8'), {
  document: {
    querySelector: s => ({ '#product-search': search, '#product-count': count, '#shop-empty': empty, '#clear-filters': clear })[s],
    querySelectorAll: s => s === '[data-filter]' ? filters : products,
  },
});
search.value = 'alcool'; search.handlers.input();
assert.equal(products[0].hidden, false); assert.equal(products[1].hidden, true);
filters[1].handlers.click(); assert.equal(empty.hidden, false);
clear.handlers.click(); assert.ok(products.every(product => !product.hidden));
console.log('PASS: working hours, timezone/date boundaries, calendar, service preselection, WhatsApp encoding/fallback, invalid times, product search/filter/reset.');
