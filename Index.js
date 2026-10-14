const navbar = document.querySelector(".navbar");
const navToggle = document.querySelector("#toggle");
const navPanel = document.querySelector("#primary-menu");

if (navbar && navToggle && navPanel) {
  navToggle.addEventListener("click", () => {
    const isOpen = navbar.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
    navToggle.setAttribute("aria-label", isOpen ? "Fechar menu" : "Abrir menu");
  });

  navPanel.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      navbar.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "Abrir menu");
    }
  });
}
