import re
s=open("/Users/josh/ClaudeCodes/PN/dashboard.html").read()
def remove_card(html,title):
    h2=html.find('<h2>'+title)
    if h2<0: return html
    start=html.rfind('<div class="card',0,h2); depth=0
    for m in re.finditer(r'<div\b|</div>', html[start:]):
        depth += -1 if m.group(0).startswith('</') else 1
        if depth==0:
            end=start+m.end()
            while end<len(html) and html[end] in ' \n\r\t': end+=1
            return html[:start]+html[end:]
    return html
for t in ['Open decisions','Hires / department heads','Rolodex']: s=remove_card(s,t)
s=re.sub(r'\s*<div class="tile"><div class="n">\$2\.0M</div>.*?</div></div>','',s,count=1)
s=re.sub(r'\s*<div class="flag"><b>Continuity flag:</b>.*?</div>','',s,count=1,flags=re.DOTALL)
s=s.replace('Days to $500K deposit','Days to cash-flow deposit').replace("<b>$500K cash-flow deposit</b> due","<b>Cash-flow deposit</b> due")
s=s.replace('<th>Eps</th><th>Budget</th>','<th>Eps</th>')
mtbl=re.search(r'<h2>All sets.*?</table>', s, re.DOTALL)
if mtbl:
    tbl=mtbl.group(0); s=s.replace(tbl, re.sub(r'<td>[^<]*</td>(?=<td><span class="chip)','',tbl))
for a,b in {'7 days — heaviest · $15K/8d budgeted · was $125/hr':'7 days — heaviest set','D11–15 · $10K/5d budgeted · was $400/hr':'Days 11–15 (North Shore window)','$20K/6d budgeted · school closed Ch.11 6/25 — confirm who signs':'School closed Ch.11 6/25 — confirm who signs','was $145/hr · family caters!':'family caters!'}.items(): s=s.replace(a,b)
s=s.replace(' (target $10K/5d)','')
for num in ['3398323123','6038181913','6176029867','6172028648','7653877277']:
    s=re.sub(r'<a href="tel:'+num+r'">[^<]*</a>','<span style="color:var(--muted)">(on file)</span>',s)
for dash,plain in {'339-832-3123':'3398323123','603-818-1913':'6038181913','617-602-9867':'6176029867','617-202-8648':'6172028648','765-387-7277':'7653877277'}.items():
    s=s.replace(dash,'(on file)').replace(plain,'(on file)')
s=re.sub(r'href="tel:\(on file\)"','href="#"',s)
s=s.replace('⚠ OUTREACH JUL 13','⚠ OUTREACH PENDING').replace('⚠ JUL 13','⚠ PENDING')
s=s.replace('<meta name="viewport" content="width=device-width, initial-scale=1.0">','<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<meta name="robots" content="noindex,nofollow">')
s=s.replace('<title>PARANORMAL NOBODIES — Production Dashboard</title>','<title>Paranormal Nobodies — Locations, Schedule & Scripts (Producer Overview)</title>')
s=s.replace('SEASON 1 · EPISODES 102–106 · MASSACHUSETTS · 2-HUB PLAN','S1 · EPS 102–106 · MASSACHUSETTS · LOCATIONS · SCHEDULE · SCRIPTS')
open("index_plain.html","w").write(s)
print("transform ok · leaks",[n for n in ['339-832-3123','$2.0M','Hires'] if n in s] or "NONE")
