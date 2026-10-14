/**
 * WEDDING RSVP → GOOGLE SHEETS  (free, no coding needed)
 *
 * SETUP (about 3 minutes — see HOW-IT-WORKS.md for screenshots-style steps)
 *  1. Create a new Google Sheet (sheets.new). Name it e.g. "Wedding RSVPs".
 *  2. Menu: Extensions → Apps Script. Delete everything there and paste THIS whole file.
 *  3. Change the 3 settings just below, then click 💾 Save.
 *  4. Click "Run" with the function  setup  selected (first time Google asks for permission → Allow).
 *  5. Click Deploy → New deployment → type "Web app"
 *       Execute as: Me      Who has access: Anyone
 *     → Deploy → copy the "Web app URL".
 *  6. Paste that URL in site-config.js →  rsvp.googleSheetUrl: "PASTE-HERE"
 *  Done. Every reply appears as new rows (one row per guest) + the Summary tab updates itself.
 */

// ---------- SETTINGS -------------------------------------------------------
const NOTIFY_EMAIL = "";            // your email to get a message for every new RSVP ("" = off)
const SEND_GUEST_CONFIRMATION = true; // email guests a copy of their reply
const COUPLE_NAMES = "Amelia & James";
// ---------------------------------------------------------------------------

const HEADERS = ["Received", "Household", "Email", "Phone", "Guest name", "Attending", "Meal", "Dietary needs",
                 "Shuttle", "Song request", "Message", "Language", "Invited as"];

function setup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName("RSVPs") || ss.insertSheet("RSVPs");
  sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]).setFontWeight("bold").setBackground("#EFE9DF");
  sh.setFrozenRows(1);
  let sum = ss.getSheetByName("Summary") || ss.insertSheet("Summary");
  sum.clear();
  sum.getRange("A1:B1").setValues([["Summary", "Count"]]).setFontWeight("bold").setBackground("#EFE9DF");
  sum.getRange("A2:B6").setFormulas([
    ["=\"Households replied\"", "=COUNTUNIQUE(FILTER(RSVPs!B2:B, RSVPs!B2:B<>\"\"))"],
    ["=\"Guests attending\"", "=COUNTIF(RSVPs!F2:F, \"yes\")"],
    ["=\"Guests declined\"", "=COUNTIF(RSVPs!F2:F, \"no\")"],
    ["=\"Need the shuttle (guests)\"", "=COUNTIFS(RSVPs!I2:I, \"yes\", RSVPs!F2:F, \"yes\")"],
    ["=\"Dietary notes\"", "=COUNTIFS(RSVPs!H2:H, \"<>\", RSVPs!F2:F, \"yes\")"],
  ]);
  sum.getRange("D1:E1").setValues([["Meal", "Count"]]).setFontWeight("bold").setBackground("#EFE9DF");
  sum.getRange("D2").setFormula("=IFERROR(QUERY(RSVPs!F2:G, \"select G, count(G) where F = 'yes' and G <> '' group by G label count(G) ''\", 0), \"\")");
  sum.autoResizeColumns(1, 5);
}

function doPost(e) {
  const lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    const d = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName("RSVPs") || (setup(), ss.getSheetByName("RSVPs"));
    const when = new Date();
    // Keep only the latest reply per email: remove this household's earlier rows
    if (d.email && sh.getLastRow() > 1) {
      const emails = sh.getRange(2, 3, sh.getLastRow() - 1, 1).getValues();
      for (let r = emails.length - 1; r >= 0; r--) {
        if (String(emails[r][0]).trim().toLowerCase() === String(d.email).trim().toLowerCase()) sh.deleteRow(r + 2);
      }
    }
    const rows = (d.guests || []).map(g => [when, d.household, d.email, d.phone, g.name, g.attending, g.meal, g.dietary,
                                             d.shuttle, d.song, d.message, d.lang, d.invitedAs]);
    if (rows.length) sh.getRange(sh.getLastRow() + 1, 1, rows.length, HEADERS.length).setValues(rows);

    const lines = (d.guests || []).map(g => `• ${g.name}: ${g.attending === "yes" ? "attending" : "not attending"}${g.meal ? " — " + g.meal : ""}${g.dietary ? " (" + g.dietary + ")" : ""}`).join("\n");
    if (NOTIFY_EMAIL) MailApp.sendEmail(NOTIFY_EMAIL, `New RSVP: ${d.household}`, `${lines}\n\nShuttle: ${d.shuttle || "-"}\nSong: ${d.song || "-"}\nMessage: ${d.message || "-"}\nEmail: ${d.email}`);
    if (SEND_GUEST_CONFIRMATION && d.email) {
      const fr = d.lang === "fr";
      MailApp.sendEmail(d.email, fr ? `Votre réponse — mariage ${COUPLE_NAMES}` : `Your RSVP — ${COUPLE_NAMES}'s wedding`,
        (fr ? `Merci ! Voici votre réponse :\n\n` : `Thank you! Here is your reply:\n\n`) + lines +
        (fr ? `\n\nUn changement ? Renvoyez simplement le formulaire sur notre site.` : `\n\nNeed to change something? Just send the form again on our website.`));
    }
    return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) })).setMimeType(ContentService.MimeType.JSON);
  } finally { lock.releaseLock(); }
}

function doGet() { return ContentService.createTextOutput("RSVP endpoint is running ✔"); }
