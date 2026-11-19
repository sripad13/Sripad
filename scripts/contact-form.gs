/**
 * Contact form backend for work.falsewinger.com.
 *
 * Paste this into Extensions > Apps Script of the Google Sheet that receives
 * the messages, then Deploy > New deployment > Web app:
 *   Execute as: Me    Who has access: Anyone
 * Copy the web app URL into SCRIPT_URL in form.html.
 *
 * Column headers in row 1 must match the names below exactly
 * (Timestamp is added automatically by Google Forms; here we write it ourselves).
 */
const SHEET_NAME = 'Form Responses 1';   // the tab that holds the messages
const MAX_LEN = { name: 200, email: 200, company: 200, message: 3000 };

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);

    // Honeypot: bots fill the hidden "website" field. Pretend success, store nothing.
    if (d.website) return reply({ ok: true });

    const fields = {
      'Name': clean(d.name, MAX_LEN.name),
      'Email': clean(d.email, MAX_LEN.email),
      'Company name': clean(d.company, MAX_LEN.company),
      'Message': clean(d.message, MAX_LEN.message)
    };
    if (!fields['Name'] || !fields['Message'] || !isEmail(fields['Email'])) {
      return reply({ ok: false, error: 'invalid' });
    }

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    const row = headers.map(h => h === 'Timestamp' ? new Date() : (fields[h] !== undefined ? fields[h] : ''));
    sheet.appendRow(row);

    return reply({ ok: true });
  } catch (err) {
    return reply({ ok: false, error: 'server' });
  }
}

function clean(value, max) {
  return String(value || '').trim().slice(0, max);
}

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
