const navbar = document.querySelector(".navbar");
const contactForm = document.querySelector("#contact-form");
if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!contactForm.reportValidity()) return;

    const fields = new FormData(contactForm);
    const name = fields.get("name").trim();
    const location = fields.get("location").trim();
    if (!name || !location) {
      const emptyField = contactForm.querySelector(!name ? "#contact-name" : "#contact-location");
      emptyField.setCustomValidity("Preencha este campo para continuar.");
      emptyField.reportValidity();
      emptyField.addEventListener("input", () => emptyField.setCustomValidity(""), { once: true });
      return;
    }

    const lines = [
      `Olá, A&N! Meu nome é ${name}. Gostaria de conversar sobre um orçamento.`,
      `Serviço: ${fields.get("service")}`,
      `Bairro e cidade: ${location}`,
    ];
    const phone = fields.get("phone").trim();
    const message = fields.get("message").trim();
    if (phone) lines.push(`Telefone: ${phone}`);
    if (message) lines.push(`Detalhes: ${message}`);

    const url = `https://wa.me/5548988061017?text=${encodeURIComponent(lines.join("\n"))}`;
    // A real link stays available if the browser blocks the new tab.
    const status = document.querySelector("#contact-status");
    const retry = document.createElement("a");
    retry.href = url;
    retry.target = "_blank";
    retry.rel = "noopener noreferrer";
    retry.textContent = "Abrir mensagem no WhatsApp";
    status.replaceChildren("Sua mensagem está pronta. ", retry);
    window.open(url, "_blank", "noopener,noreferrer");
  });
}

const navToggle = document.querySelector("#toggle");
const navPanel = document.querySelector("#primary-menu");

if (navbar && navToggle && navPanel) {
  const closeMenu = () => {
    navbar.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
    navToggle.setAttribute("aria-label", "Abrir menu");
  };
  navToggle.addEventListener("click", () => {
    const isOpen = navbar.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
    navToggle.setAttribute("aria-label", isOpen ? "Fechar menu" : "Abrir menu");
  });

  navPanel.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      closeMenu();
    }
  });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && navbar.classList.contains("is-open")) {
      closeMenu();
      navToggle.focus();
    }
  });
  document.addEventListener("click", event => {
    if (!navbar.contains(event.target)) closeMenu();
  });
}
