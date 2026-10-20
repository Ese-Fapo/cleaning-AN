// Provisional business hours. Closing times are exclusive; requests need team confirmation.
const bookingHours = { weekdays: { start: 8, end: 18 }, saturday: { start: 8, end: 12 } };
function bookingClock(now = new Date()) {
  const parts = Object.fromEntries(new Intl.DateTimeFormat("en-GB", {
    timeZone: "America/Sao_Paulo", year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", hourCycle: "h23"
  }).formatToParts(now).map(part => [part.type, part.value]));
  return { date: `${parts.year}-${parts.month}-${parts.day}`, minutes: Number(parts.hour) * 60 + Number(parts.minute) };
}
function bookingSlots(date, now = new Date()) {
  const clock = bookingClock(now);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || date < clock.date) return [];
  const parsed = new Date(`${date}T12:00:00Z`);
  if (Number.isNaN(parsed.getTime()) || parsed.toISOString().slice(0, 10) !== date) return [];
  const day = parsed.getUTCDay();
  if (day === 0) return [];
  const hours = day === 6 ? bookingHours.saturday : bookingHours.weekdays;
  return Array.from({ length: hours.end - hours.start }, (_, index) => hours.start + index)
    .filter(hour => date !== clock.date || hour * 60 > clock.minutes)
    .map(hour => `${String(hour).padStart(2, "0")}:00`);
}
const hourLabel = hour => `${String(hour).padStart(2, "0")}:00`;
document.querySelectorAll("[data-working-hours]").forEach(element => {
  const table = document.createElement("table");
  table.className = "working_hours_table";
  const caption = document.createElement("caption");
  caption.className = "hours_caption";
  caption.textContent = "Horários de atendimento — horário de Brasília";
  table.append(caption);
  const head = document.createElement("thead");
  const heading = document.createElement("tr");
  ["Dia", "Horário"].forEach(text => {
    const cell = document.createElement("th");
    cell.scope = "col";
    cell.textContent = text;
    heading.append(cell);
  });
  head.append(heading);
  table.append(head);
  const body = document.createElement("tbody");
  ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"].forEach((day, index) => {
    const row = document.createElement("tr");
    const label = document.createElement("th");
    label.scope = "row";
    label.textContent = day;
    const hours = document.createElement("td");
    const schedule = index === 5 ? bookingHours.saturday : bookingHours.weekdays;
    hours.textContent = index === 6 ? "Fechado" : `${hourLabel(schedule.start)}–${hourLabel(schedule.end)}`;
    row.append(label, hours);
    body.append(row);
  });
  table.append(body);
  element.replaceChildren(table);
});
const bookingDialog = document.querySelector("#booking-dialog");
if (bookingDialog) {
  const bookingForm = document.querySelector("#booking-form");
  const days = document.querySelector("#booking-days");
  const monthLabel = document.querySelector("#booking-month");
  const selectedLabel = document.querySelector("#booking-selected");
  const time = document.querySelector("#booking-time");
  const status = document.querySelector("#booking-status");
  let selectedDate = "";
  let shownMonth;
  const longDate = date => new Intl.DateTimeFormat("pt-BR", { dateStyle: "full", timeZone: "UTC" }).format(new Date(`${date}T12:00:00Z`));
  function updateTimes() {
    const previousTime = time.value;
    const slots = selectedDate ? bookingSlots(selectedDate) : [];
    time.replaceChildren(new Option(slots.length ? "Selecione um horário" : "Escolha outra data", ""));
    slots.forEach(slot => time.add(new Option(slot, slot)));
    time.disabled = !slots.length;
    if (slots.includes(previousTime)) time.value = previousTime;
    selectedLabel.textContent = selectedDate ? `${longDate(selectedDate)}${slots.length ? "" : " — sem horários para solicitar."}` : "Selecione um dia no calendário.";
  }
  function renderCalendar() {
    const year = shownMonth.getUTCFullYear();
    const month = shownMonth.getUTCMonth();
    monthLabel.textContent = new Intl.DateTimeFormat("pt-BR", { month: "long", year: "numeric", timeZone: "UTC" }).format(shownMonth);
    days.replaceChildren();
    for (let blank = 0; blank < shownMonth.getUTCDay(); blank++) {
      const spacer = document.createElement("span");
      spacer.setAttribute("aria-hidden", "true");
      days.append(spacer);
    }
    const last = new Date(Date.UTC(year, month + 1, 0)).getUTCDate();
    const today = bookingClock().date;
    for (let day = 1; day <= last; day++) {
      const date = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = day;
      button.disabled = !bookingSlots(date).length;
      button.dataset.date = date;
      button.setAttribute("aria-label", longDate(date));
      button.setAttribute("aria-pressed", String(date === selectedDate));
      if (date === today) button.setAttribute("aria-current", "date");
      button.addEventListener("click", () => {
        selectedDate = date;
        status.replaceChildren();
        updateTimes();
        renderCalendar();
        days.querySelector(`[data-date="${date}"]`).focus();
      });
      days.append(button);
    }
    document.querySelector("#booking-prev").disabled = `${year}-${String(month + 1).padStart(2, "0")}` <= today.slice(0, 7);
  }
  document.querySelectorAll("[data-booking-open]").forEach(opener => opener.addEventListener("click", event => {
    if (typeof bookingDialog.showModal !== "function") return;
    event.preventDefault();
    const preferredService = opener.dataset.bookingService;
    if (preferredService) document.querySelector("#booking-service").value = preferredService;
    shownMonth = new Date(`${bookingClock().date.slice(0, 7)}-01T12:00:00Z`);
    if (selectedDate && !bookingSlots(selectedDate).length) selectedDate = "";
    status.replaceChildren();
    renderCalendar();
    updateTimes();
    bookingDialog.showModal();
  }));
  document.querySelector(".booking_close").addEventListener("click", () => bookingDialog.close());
  document.querySelector("#booking-prev").addEventListener("click", () => { shownMonth.setUTCMonth(shownMonth.getUTCMonth() - 1); renderCalendar(); });
  document.querySelector("#booking-next").addEventListener("click", () => { shownMonth.setUTCMonth(shownMonth.getUTCMonth() + 1); renderCalendar(); });
  bookingForm.addEventListener("input", event => {
    if (typeof event.target.setCustomValidity === "function") event.target.setCustomValidity("");
    status.replaceChildren();
  });
  bookingForm.addEventListener("submit", event => {
    event.preventDefault();
    if (!selectedDate || !bookingSlots(selectedDate).includes(time.value)) {
      updateTimes();
      renderCalendar();
      status.textContent = "Escolha uma data e um horário futuro para continuar.";
      return;
    }
    const name = document.querySelector("#booking-name");
    const location = document.querySelector("#booking-location");
    [name, location].forEach(field => field.setCustomValidity(field.value.trim() ? "" : "Preencha este campo para continuar."));
    if (!bookingForm.reportValidity()) return;
    const lines = [
      `Olá, A&N! Sou ${name.value.trim()} e gostaria de solicitar um agendamento.`,
      `Serviço: ${document.querySelector("#booking-service").value}`,
      `Data de preferência: ${longDate(selectedDate)}`,
      `Horário de preferência: ${time.value} (horário de Brasília)`,
      `Bairro e cidade: ${location.value.trim()}`
    ];
    const details = document.querySelector("#booking-details").value.trim();
    if (details) lines.push(`Detalhes: ${details}`);
    lines.push("Podem confirmar a disponibilidade e o orçamento? Aguardo a confirmação da equipe.");
    const url = `https://wa.me/5548988061017?text=${encodeURIComponent(lines.join("\n"))}`;
    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "Abrir solicitação no WhatsApp";
    status.replaceChildren("Mensagem pronta para você enviar. ", link);
    window.open(url, "_blank", "noopener,noreferrer");
  });
}

const footerYear = document.querySelector("#footer-year");
if (footerYear) footerYear.textContent = new Date().getFullYear();
