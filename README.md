# A&N Serviços

Static Portuguese website for a cleaning business in Florianópolis and region. Includes six service pages, a searchable 18-product catalog, contact forms, and a calendar that prepares booking requests for WhatsApp.

## Preview

From this directory:

```powershell
python -m http.server 5173 --bind 127.0.0.1
```

Open `http://127.0.0.1:5173`. Stop the server with Ctrl+C. No dependency installation or build is required.

## Maintain

- `index.html` owns the shared navbar, booking dialog, and footer. After editing shared markup, run `python scripts/complete_site.py` to copy it to the service, shop, and information pages.
- `booking.js` owns provisional working hours, the Brasília-time calendar, and WhatsApp requests. Change `bookingHours` there, then run the synchronization script to update the static hours tables too.
- `Index.js` handles the menu and homepage contact form. `compra.js` handles catalog filtering; edit products in `compra.html`.
- Social icons without business profile URLs remain unavailable. Replace those spans in the homepage footer with links and accessible labels once the URLs are supplied, then synchronize.
- Requests are sent by the visitor in WhatsApp. There is no booking database, automatic reservation, payment processing, or live team calendar. Availability must be confirmed by the business.

## Verify

```powershell
python scripts/verify_site.py
node scripts/verify_flows.cjs
node --check Index.js
node --check booking.js
node --check compra.js
```

Checks cover local routes/assets, labels and controls, shared booking/hours, metadata, calendar time boundaries, WhatsApp message creation, and product search. Browser layout and real WhatsApp handoff should also be checked on desktop and mobile.

## Before launch

Confirm official working hours, social profile URLs, and any additional business contact details. Hours are currently labeled provisional. Add genuine reviews and client logos only with appropriate approval; demonstration testimonials and logos have been removed.

Set the production domain before adding canonical URLs, absolute social preview images, and a sitemap. Upload the static files and assets to the chosen host, and configure it to serve `404.html` for missing routes. Review `privacidade.html` whenever forms, providers, analytics, or hosting behavior changes.
