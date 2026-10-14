/* Wedding Widgets — shared helpers (theme, fonts, language, time zones) */
(function () {
  const P = new URLSearchParams(location.search);
  const FONTS = {
    sage: "Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Pinyon+Script&family=Jost:wght@400;500;600",
    oldmoney: "Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Pinyon+Script&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400",
    bordeaux: "Playfair+Display:ital,wght@0,400;0,500;1,400&family=Pinyon+Script&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400",
    terracotta: "Gilda+Display&family=Mrs+Saint+Delafield&family=Karla:wght@400;500;600&family=Cormorant+Garamond:ital@1",
    midnight: "Cinzel:wght@400;500&family=Great+Vibes&family=Montserrat:wght@400;500;600&family=Cormorant+Garamond:ital@1",
    dustyblue: "Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Parisienne&family=Lato:wght@400;700",
  };
  const theme = FONTS[P.get("theme")] ? P.get("theme") : "sage";
  document.documentElement.setAttribute("data-theme", theme);
  if (P.get("shape")) document.documentElement.setAttribute("data-shape", P.get("shape"));
  const l = document.createElement("link"); l.rel = "stylesheet"; l.href = `https://fonts.googleapis.com/css2?family=${FONTS[theme]}&display=swap`; document.head.appendChild(l);
  // custom colours (optional): accent=hex, ink=hex
  const css = [];
  [["accent", "--accent"], ["ink", "--ink"], ["btn", "--btn"], ["btnink", "--btnInk"], ["surface", "--surface"], ["line", "--line"]].forEach(([k, v]) => {
    const c = P.get(k); if (c && /^[0-9a-f]{3,8}$/i.test(c)) css.push(`${v}:#${c}`);
  });
  if (css.length) { const s = document.createElement("style"); s.textContent = `:root,[data-theme]{${css.join(";")}}`; document.head.appendChild(s); }
  const bg = P.get("bg"); // transparent (default) | solid | card | hex
  document.addEventListener("DOMContentLoaded", () => {
    let topLevel = true; try { topLevel = window.self === window.top; } catch (e) { topLevel = false; }
    if (bg === "solid" || (!bg && topLevel)) { document.body.classList.add("solid"); frame(); }
    else if (bg === "card") document.body.classList.add("card-bg");
    else if (bg && /^[0-9a-f]{3,8}$/i.test(bg)) document.body.style.background = "#" + bg;
  });

  const lang = (P.get("lang") || "en").slice(0, 2);

  // Full-page mode (opened from a button on the Canva website): couple names on top, "back" link below
  const FRAME = {
    countdown: { en: "Counting down to our wedding", fr: "Compte à rebours jusqu’au grand jour", es: "Cuenta atrás para nuestra boda", de: "Countdown bis zu unserer Hochzeit", it: "Il conto alla rovescia per le nostre nozze" },
    calendar: { en: "", fr: "", es: "", de: "", it: "" },
    music: { en: "Our song", fr: "Notre chanson", es: "Nuestra canción", de: "Unser Lied", it: "La nostra canzone" },
    rsvp: { en: "", fr: "", es: "", de: "", it: "" },
    back: { en: "Back to our website", fr: "Retour au site", es: "Volver a la web", de: "Zurück zur Website", it: "Torna al sito" },
  };
  function frame() {
    const b = document.body, kind = b.dataset.frame; if (!kind || kind === "off") return;
    const couple = (P.get("couple") || P.get("title") || "").replace(/\s+[—–-]\s+.*$/, "").trim();
    const kick = (FRAME[kind] || {})[lang] ?? (FRAME[kind] || {}).en ?? "";
    const inner = document.createElement("div"); inner.className = "pg-body";
    while (b.firstChild) inner.appendChild(b.firstChild);
    const head = document.createElement("header"); head.className = "pg-head";
    head.innerHTML = (couple ? `<div class="pg-couple">${esc(couple)}</div>` : "") + (kick ? `<div class="pg-kicker">${esc(kick)}</div>` : "");
    const back = document.createElement("a"); back.className = "pg-back"; back.href = document.referrer || "#";
    back.textContent = "← " + (FRAME.back[lang] || FRAME.back.en);
    back.addEventListener("click", (e) => { if (history.length > 1) { e.preventDefault(); history.back(); } else if (!document.referrer) { e.preventDefault(); window.close(); } });
    if (head.innerHTML) b.appendChild(head);
    b.appendChild(inner); b.appendChild(back);
    b.classList.add("framed");
  }
  document.documentElement.lang = lang;

  function tzOffset(date, tz) {
    const p = new Intl.DateTimeFormat("en-US", { timeZone: tz, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" }).formatToParts(date);
    const g = (k) => +p.find((x) => x.type === k).value;
    return Date.UTC(g("year"), g("month") - 1, g("day"), g("hour"), g("minute"), g("second")) - date.getTime();
  }
  function zoned(local, tz) {
    if (!local) return null;
    const [d, tm = "00:00"] = local.split("T");
    const [Y, M, D] = d.split("-").map(Number); const [h, mi, s = 0] = tm.split(":").map(Number);
    const guess = Date.UTC(Y, M - 1, D, h || 0, mi || 0, s);
    if (!tz) return new Date(Y, M - 1, D, h || 0, mi || 0, s);
    try { const off = tzOffset(new Date(guess), tz); let utc = guess - off; const off2 = tzOffset(new Date(utc), tz); if (off2 !== off) utc = guess - off2; return new Date(utc); }
    catch (e) { return new Date(Y, M - 1, D, h || 0, mi || 0, s); }
  }
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  function toast(msg) { let t = document.querySelector(".toast"); if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); } t.textContent = msg; t.classList.add("show"); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove("show"), 2000); }
  function fail(msg) { document.body.insertAdjacentHTML("afterbegin", `<div class="err-box">⚠️ ${esc(msg)}</div>`); }
  const ICS = (d) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");

  window.W = { P, theme, lang, zoned, esc, toast, fail, ICS, t: (dict) => dict[lang] || dict.en };
})();
