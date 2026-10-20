const search = document.querySelector('#product-search');
const filters = [...document.querySelectorAll('[data-filter]')];
const products = [...document.querySelectorAll('.product-card')];
const count = document.querySelector('#product-count');
const empty = document.querySelector('#shop-empty');
let category = 'Todos';
const normalize = (value) => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
function filterProducts() {
  const query = normalize(search.value.trim());
  let visible = 0;
  products.forEach((product) => {
    const matches = (category === 'Todos' || product.dataset.category === category) && normalize(product.querySelector('.product-info').textContent).includes(query);
    product.hidden = !matches;
    if (matches) visible++;
  });
  count.textContent = `${visible} ${visible === 1 ? 'produto encontrado' : 'produtos encontrados'}`;
  empty.hidden = visible !== 0;
}
// Keep the visible count in sync if products are added or removed from the catalog.
filterProducts();
filters.forEach((button) => button.addEventListener('click', () => {
  category = button.dataset.filter;
  filters.forEach((filter) => filter.setAttribute('aria-pressed', String(filter === button)));
  filterProducts();
}));
search.addEventListener('input', filterProducts);
document.querySelector('#clear-filters').addEventListener('click', () => {
  search.value = '';
  filters[0].click();
  search.focus();
});
