const navbar = document.querySelector(".navbar");
const trustedCarousel = document.querySelector('.trusted_carousel');
if (trustedCarousel) {
  const track = trustedCarousel.querySelector('.trusted_track');
  const logos = track.querySelector('.trusted_logos');
  const duplicate = logos.cloneNode(true);
  duplicate.setAttribute('aria-hidden', 'true');
  duplicate.querySelectorAll('img').forEach((img) => {
    img.alt = '';
    img.loading = 'eager';
  });
  track.append(duplicate);
  trustedCarousel.classList.add('is-ready');
}
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

const reviewTrack = document.querySelector("#testimonials-track");
const reviewControls = document.querySelector(".testimonials_controls");

if (reviewTrack && reviewControls) {
  const cards = [...reviewTrack.querySelectorAll(".review_card")];
  const previous = reviewControls.querySelector('[data-review-direction="-1"]');
  const next = reviewControls.querySelector('[data-review-direction="1"]');
  const count = reviewControls.querySelector(".testimonials_count");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const dotsContainer = document.querySelector(".testimonials_dots");
  const autoplayButton = reviewControls.querySelector(".testimonials_autoplay");
  const reviewSection = reviewTrack.closest(".testimonials");
  let currentReview = 0;
  let autoplayTimer;
  let userPaused = false;
  let pointerInside = false;
  let focusInside = false;
  let touchActive = false;
  let sectionVisible = false;

  const scheduleAutoplay = () => {
    window.clearTimeout(autoplayTimer);
    const paused = userPaused || reducedMotion.matches;
    if (autoplayButton) {
      autoplayButton.textContent = paused ? "Reproduzir" : "Pausar";
      autoplayButton.setAttribute("aria-pressed", String(paused));
      autoplayButton.setAttribute("aria-label", paused ? "Iniciar reprodução automática" : "Pausar reprodução automática");
    }
    count.setAttribute("aria-live", paused || focusInside ? "polite" : "off");
    if (paused || pointerInside || focusInside || touchActive || !sectionVisible || document.hidden) return;
    autoplayTimer = window.setTimeout(() => {
      const atEnd = reviewTrack.scrollLeft + reviewTrack.clientWidth >= reviewTrack.scrollWidth - 2;
      goToReview(atEnd ? 0 : currentReview + 1);
      scheduleAutoplay();
    }, 5000);
  };

  const goToReview = (index) => {
    const target = cards[Math.max(0, Math.min(index, cards.length - 1))];
    reviewTrack.scrollTo({
      left: target.offsetLeft - cards[0].offsetLeft,
      behavior: reducedMotion.matches ? "instant" : "smooth"
    });
    scheduleAutoplay();
  };

  reviewTrack.setAttribute("aria-roledescription", "carrossel");
  const dots = cards.map((card, index) => {
    card.id = `depoimento-${index + 1}`;
    card.setAttribute("aria-label", `Depoimento ${index + 1} de ${cards.length}`);
    const dot = document.createElement("button");
    dot.type = "button";
    dot.setAttribute("aria-label", `Ver depoimento ${index + 1}`);
    dot.setAttribute("aria-controls", card.id);
    dot.addEventListener("click", () => goToReview(index));
    if (dotsContainer) dotsContainer.append(dot);
    return dot;
  });
  if (dotsContainer) dotsContainer.hidden = false;

  const updateReviews = () => {
    const trackLeft = reviewTrack.getBoundingClientRect().left;
    let closest = 0;
    cards.forEach((card, index) => {
      if (Math.abs(card.getBoundingClientRect().left - trackLeft) <
          Math.abs(cards[closest].getBoundingClientRect().left - trackLeft)) {
        closest = index;
      }
    });
    currentReview = closest;
    count.firstChild.textContent = `${String(closest + 1).padStart(2, "0")} `;
    dots.forEach((dot, index) => {
      dot.setAttribute("aria-current", String(index === closest));
    });
    previous.disabled = reviewTrack.scrollLeft <= 2;
    next.disabled = reviewTrack.scrollLeft + reviewTrack.clientWidth >= reviewTrack.scrollWidth - 2;
  };

  reviewControls.hidden = false;
  reviewControls.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-review-direction]");
    if (!button) return;
    goToReview(currentReview + Number(button.dataset.reviewDirection));
  });
  reviewTrack.addEventListener("keydown", (event) => {
    const destinations = {
      ArrowLeft: currentReview - 1,
      ArrowRight: currentReview + 1,
      Home: 0,
      End: cards.length - 1
    };
    if (!(event.key in destinations)) return;
    event.preventDefault();
    goToReview(destinations[event.key]);
  });
  reviewTrack.addEventListener("scroll", updateReviews, { passive: true });
  reviewTrack.addEventListener("pointerdown", () => {
    touchActive = true;
    scheduleAutoplay();
  }, { passive: true });
  const releaseTouch = () => {
    if (!touchActive) return;
    touchActive = false;
    scheduleAutoplay();
  };
  window.addEventListener("pointerup", releaseTouch, { passive: true });
  window.addEventListener("pointercancel", releaseTouch, { passive: true });
  reviewSection.addEventListener("pointerenter", (event) => {
    if (event.pointerType !== "mouse") return;
    pointerInside = true;
    scheduleAutoplay();
  });
  reviewSection.addEventListener("pointerleave", (event) => {
    if (event.pointerType !== "mouse") return;
    pointerInside = false;
    scheduleAutoplay();
  });
  reviewSection.addEventListener("focusin", () => {
    focusInside = true;
    scheduleAutoplay();
  });
  reviewSection.addEventListener("focusout", (event) => {
    focusInside = reviewSection.contains(event.relatedTarget);
    scheduleAutoplay();
  });
  if (autoplayButton) autoplayButton.addEventListener("click", () => {
    if (reducedMotion.matches) return;
    userPaused = !userPaused;
    if (!userPaused) focusInside = false;
    scheduleAutoplay();
  });
  reducedMotion.addEventListener("change", () => {
    if (autoplayButton) autoplayButton.disabled = reducedMotion.matches;
    scheduleAutoplay();
  });
  if (autoplayButton) autoplayButton.disabled = reducedMotion.matches;
  document.addEventListener("visibilitychange", scheduleAutoplay);
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(([entry]) => {
      sectionVisible = entry.isIntersecting;
      scheduleAutoplay();
    }, { threshold: 0.15 });
    observer.observe(reviewSection);
  } else {
    sectionVisible = true;
  }
  window.addEventListener("resize", () => {
    updateReviews();
    scheduleAutoplay();
  });
  updateReviews();
  scheduleAutoplay();
}
