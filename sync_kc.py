#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync the KC LOCATIONS sheet's "MASTER (synced)" tab into dashboard.html.

Usage:  python3 sync_kc.py <master.tsv>

Get master.tsv by exporting the tab:
  https://docs.google.com/spreadsheets/d/1ZG4jiOAOoivqkiaK0pnq8ZpwJ48vYvobyoaOsvs6v_A/export?format=tsv&gid=<GID>
(needs to be signed in — download it in the browser, then point this script at it.)

Then the usual: build_producer.py -> gate.py -> git push.

NOTE ON PRIVACY: this sheet holds private individuals' mobile numbers. The synced
block lands INSIDE the password-gated bundle. Do NOT publish the sheet to the web
as a public CSV to get "live" sync — that would put those numbers on the open web.
"""
import sys, csv, io, re, html, datetime, os

SRC = sys.argv[1] if len(sys.argv) > 1 else None
DASH = os.path.expanduser('~/ClaudeCodes/PN/dashboard.html')
START, END = '<!--KC:START-->', '<!--KC:END-->'

def esc(s): return html.escape((s or '').strip())

def build(rows):
    groups = {}
    for r in rows:
        groups.setdefault(r.get('SET (our board)', '?') or '?', []).append(r)
    n = sum(len(v) for v in groups.values())
    stamp = datetime.date.today().strftime('%b %-d, %Y')
    out = [START]
    out.append('<div class="card foldable" id="kcsheet"><h2>📇 KC — Locations &amp; Contacts '
               f'<span class="tag">{n} rows synced from the shared sheet · {stamp}</span></h2>')
    out.append('<p class="note" style="margin:0 0 10px">Mirrored from the <b>MASTER (synced)</b> tab of '
               '<a href="https://docs.google.com/spreadsheets/d/1ZG4jiOAOoivqkiaK0pnq8ZpwJ48vYvobyoaOsvs6v_A/edit" '
               'target="_blank">KC LOCATIONS — CONTACTS</a>. The sheet is the source of truth; this is a read-only '
               'mirror. Re-run <code>sync_kc.py</code> to refresh.</p>')
    for g in sorted(groups):
        rs = groups[g]
        out.append(f'<details class="fold"><summary>{esc(g)} <span class="note">({len(rs)})</span></summary>'
                   '<div class="foldbody"><table><tr><th>Location</th><th>Address</th><th>Contact</th>'
                   '<th>Phone</th><th>Email</th><th>Notes</th><th>Links</th></tr>')
        for r in rs:
            links = []
            if r.get('ALBUM', '').startswith('http'): links.append(f'<a href="{esc(r["ALBUM"])}" target="_blank">album ↗</a>')
            if r.get('LINK', '').startswith('http'):  links.append(f'<a href="{esc(r["LINK"])}" target="_blank">listing ↗</a>')
            ph = esc(r.get('PHONE', '')); em = esc(r.get('EMAIL', ''))
            phl = f'<a href="tel:{re.sub(chr(92)+"D","",ph)}">{ph}</a>' if ph else ''
            eml = f'<a href="mailto:{em}">{em}</a>' if '@' in em else em
            out.append('<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                esc(r.get('LOCATION', '')) or '<i style="color:var(--muted)">—</i>', esc(r.get('ADDRESS', '')),
                esc(r.get('CONTACT', '')), phl, eml, esc(r.get('NOTES', '')), ' · '.join(links)))
        out.append('</table></div></details>')
    out.append('</div>')
    out.append(END)
    return '\n'.join(out), n

def main():
    if not SRC or not os.path.exists(SRC):
        sys.exit('usage: sync_kc.py <master.tsv>   (export the MASTER (synced) tab first)')
    with io.open(SRC, encoding='utf-8', newline='') as f:
        rows = [r for r in csv.DictReader(f, delimiter='\t') if any((v or '').strip() for v in r.values())]
    block, n = build(rows)
    s = io.open(DASH, encoding='utf-8').read()
    if START in s and END in s:
        s = s[:s.index(START)] + block + s[s.index(END) + len(END):]
        how = 'replaced'
    else:
        anchor = s.index('<div class="card foldable" id="scout"') if 'id="scout"' in s else s.index('</body>')
        s = s[:anchor] + block + '\n    ' + s[anchor:]
        how = 'inserted'
    io.open(DASH, 'w', encoding='utf-8').write(s)
    print('%s KC block — %d rows across %d sets' % (how, n, len({r.get("SET (our board)") for r in rows})))

if __name__ == '__main__':
    main()
