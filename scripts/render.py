"""Render the bilingual page from paragraphs verified against the official PDFs.

Conference text is selected by paragraph index, never rewritten. data-source
attributes let verify.py compare every displayed passage against its source.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
registration = json.loads((ROOT / 'registration.json').read_text())['url']
if registration and not registration.startswith('https://'):
    raise ValueError('Registration must use an HTTPS URL')

UI = {
 'fr': dict(skip='Aller au contenu', nav='Navigation principale', register="S’inscrire", registration='Inscription', programme='Programme', rationale='Argument', practical='Informations pratiques', download='Télécharger le livret', booklet='Livret officiel', full='Lire la suite', top='Retour en haut', pending="Le lien d’inscription n’est pas encore disponible.", days='Programme détaillé', lang='Choisir la langue', doclang='Français', other='English', overview='Consulter le programme'),
 'en': dict(skip='Skip to content', nav='Main navigation', register='Register', registration='Registration', programme='Program', rationale='Rationale', practical='Practical information', download='Download the booklet', booklet='Official booklet', full='Read more', top='Back to top', pending='The registration link is not available yet.', days='Detailed program', lang='Choose language', doclang='English', other='Français', overview='View the program'),
}

UI['fr'].update(abstracts='Résumés des communications', show='Afficher', hide='Réduire', program_pdf='Programme (PDF)', official_site='Site officiel')
UI['en'].update(abstracts='Presentation abstracts', show='Expand', hide='Collapse', program_pdf='Program (PDF)', official_site='Official website')

ORGANIZERS = [
 ('TRENDS Group', 'https://trendsgroup.org/', '35 125 805 310'),
 ('PLURIEL', 'https://pluriel.fuce.eu/', '910 125 520 310'),
 ('Université de Montréal', 'https://www.umontreal.ca/', '1520 125 575 310'),
 ('UQAM', 'https://uqam.ca/', '2210 125 530 310'),
]

ABSTRACT_AXES = {
 'en': [(229,253,[231,235,239,242,247]),(253,284,[255,264,267,270,273,278]),(284,306,[286,289,294,298,303]),(306,334,[308,312,315,318,321,326,329])],
 'fr': [(229,253,[231,235,239,242,247]),(253,283,[255,264,267,270,273,278]),(283,305,[285,288,293,297,302]),(305,332,[307,311,314,317,320,324,327])],
}

def page(lang):
 p = json.loads((ROOT / 'source' / f'{lang}.json').read_text())
 ui = UI[lang]
 def s(i, tag='p', cls=''):
  return f'<{tag} data-source="{lang}:{i}" class="{cls}">{escape(p[i])}</{tag}>'
 def anchor(key): return f'{key}-{lang}'
 def toggle():
  return f'<span class="toggle-control"><span class="when-closed">{ui["show"]}</span><span class="when-open">{ui["hide"]}</span><span class="plus" aria-hidden="true"></span></span>'
 def program_button(cls='button button-program', short=False):
  return f'<a class="{cls}" data-program-pdf href="{download}#page=3" target="_blank" rel="noopener noreferrer">{ui["program_pdf"] if short else ui["overview"]}<span aria-hidden="true">↗</span></a>'
 def register(cls='button'):
  href = registration or '#' + anchor('registration')
  external = ' target="_blank" rel="noopener noreferrer"' if registration else ''
  return f'<a class="{cls}" data-registration href="{escape(href, quote=True)}"{external}>{ui["register"]}<span aria-hidden="true">↗</span></a>'
 def session(start, stop):
  return f'<details class="session" id="session-{start}-{lang}"><summary><span>'+s(start,'span','session-label')+s(start+1,'span','session-title')+'</span>'+toggle()+'</summary><div class="session-body">'+''.join(s(i,'p','speaker' if '—' in p[i] and i<184 else '') for i in range(start+2,stop))+'</div></details>'
 def day(start,stop,num):
  sessions = {111:126,126:143,143:158,165:186,186:196,198:207,207:229}
  content=[]
  i=start+2
  while i<stop:
   if i in sessions:
    end=min(sessions[i],stop)
    content.append(session(i,end)); i=end
   else:
    content.append(s(i,'p','schedule-note')); i+=1
  return f'<details class="day" id="day-{num}-{lang}"><summary><span class="day-number" aria-hidden="true">{num}</span><span class="day-heading">{s(start,"span","day-title")}{s(start+1,"span","day-subtitle")}</span>{toggle()}</summary><div class="day-body">'+''.join(content)+'</div></details>'
 def overview():
  tables=[]
  for start,end in [(41,69),(69,88),(88,107)]:
   rows=''.join('<tr>'+''.join(s(i,'td') for i in range(row,row+3))+'</tr>' for row in range(start+4,end,3))
   tables.append('<table>'+s(start,'caption')+'<thead><tr>'+''.join(s(i,'th') for i in range(start+1,start+4))+'</tr></thead><tbody>'+rows+'</tbody></table>')
  return f'<details class="overview-details" id="overview-{lang}"><summary>{s(34,"span","day-title")}{toggle()}</summary><div class="overview-body">{s(35,"p","overview-description")}'+''.join(tables)+'</div></details>'
 def abstracts():
  axes=[]
  for axis,(start,end,authors) in enumerate(ABSTRACT_AXES[lang],1):
   papers=[]
   for number,author in enumerate(authors):
    stop=authors[number+1] if number+1<len(authors) else end
    papers.append(f'<details class="paper" id="paper-{axis}-{number}-{lang}"><summary><span>{s(author,"span","paper-author")}{s(author+1,"span","paper-title")}</span>{toggle()}</summary><div class="paper-body">'+''.join(s(i) for i in range(author+2,stop))+'</div></details>')
   axes.append(f'<details class="abstract-axis" id="abstract-axis-{axis}-{lang}"><summary><span>{s(start,"span","session-label")}{s(start+1,"span","session-title")}</span>{toggle()}</summary><div class="papers">'+''.join(papers)+'</div></details>')
  return ''.join(axes)
 def logos():
  links=[]
  for number,(name,url,box) in enumerate(ORGANIZERS):
   x,y,width,height=box.split()
   clip=f'logo-clip-{number}-{lang}'
   links.append(f'<a class="organizer-link" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{escape(name)} — {ui["official_site"]}" title="{escape(name)} — {ui["official_site"]}"><svg viewBox="{box}" aria-hidden="true" focusable="false"><defs><clipPath id="{clip}"><rect x="{x}" y="{y}" width="{width}" height="{height}"/></clipPath></defs><image href="/assets/organizing-institutions.png" width="2804" height="561" clip-path="url(#{clip})"/></svg><span class="logo-external" aria-hidden="true">↗</span></a>')
  return ''.join(links)
 institution = 348 if lang=='en' else 346
 committee = 342 if lang=='en' else 340
 workshops = 334 if lang=='en' else 332
 download=f'/documents/DIALOGIA-2026-{lang.upper()}.pdf'
 opposite='en' if lang=='fr' else 'fr'
 return f'''<div data-language="{lang}">
 <a class="skip-link" href="#{anchor('main')}">{ui['skip']}</a>
 <header class="header" id="{anchor('top')}"><div class="shell header-inner">
  <a class="wordmark" href="#{anchor('top')}" aria-label="DIALOGIA 2026">DIALOGIA<span>MONTRÉAL 2026</span></a>
  <nav aria-label="{ui['nav']}" class="main-nav"><a href="#{anchor('program')}">{ui['programme']}</a><a href="#{anchor('abstracts')}">{ui['abstracts']}</a></nav>
  <div class="header-actions"><div class="language-switch" aria-label="{ui['lang']}"><a href="?lang=fr" data-set-language="fr" lang="fr" aria-label="Français" {'aria-current="true"' if lang=='fr' else ''}>FR</a><span aria-hidden="true">/</span><a href="?lang=en" data-set-language="en" lang="en" aria-label="English" {'aria-current="true"' if lang=='en' else ''}>EN</a></div><div class="header-buttons">{program_button('button button-small button-program',True)}{register('button button-small')}</div></div>
 </div></header>
 <section class="institutions" aria-label="{escape(p[institution])}"><div class="shell"><div class="organizers-row">{logos()}</div>{s(institution,'p','eyebrow')}</div></section>
 <main id="{anchor('main')}">
  <section class="hero"><div class="shell">
   {s(0,'p','eyebrow hero-eyebrow')}
   <div class="hero-grid"><div class="hero-main"><h1>{s(1,'span')}{s(2,'span','title-second')}</h1>{s(3,'p','hero-subtitle')}<div class="hero-actions">{program_button()}{register()}</div></div>
    <aside class="hero-information">{s(4,'p','event-date')}<div class="venue">{s(5)}{s(6)}</div><a class="booklet-link" href="{download}" download><span>{ui['booklet']}<small>{ui['doclang']} · PDF</small></span><span aria-hidden="true">↓</span></a></aside>
   </div>
   <div class="day-overview">{''.join(f'<a href="#day-{n}-{lang}" data-open-day="day-{n}-{lang}">{s(i,"span","overview-date")}{s(i+1,"span","overview-label")}<span class="overview-arrow" aria-hidden="true">↘</span></a>' for i,n in [(10,19),(12,20),(14,21)])}</div>
  </div></section>
  <section class="section rationale shell" id="{anchor('rationale')}"><div class="section-rail">{s(16,'p','eyebrow')}<span class="section-number" aria-hidden="true">01</span></div><div class="section-content">{s(18,'h2')}{s(19,'p','body-copy')}<details class="rationale-more" id="rationale-more-{lang}"><summary>{ui['full']}{toggle()}</summary><div>{s(20)}{s(21)}{s(22,'h3','eyebrow')}{s(23)}</div></details>
  <div class="axes">{s(24,'h3','eyebrow')}<div class="axes-grid">{''.join(f'<div class="axis">{s(i,"span","axis-number")}{s(i+1,"h4")}</div>' for i in [25,27,29,31])}</div></div></div></section>
  <section class="program-section" id="{anchor('program')}"><div class="section shell"><div class="section-rail"><p class="eyebrow">{ui['programme']}</p><span class="section-number" aria-hidden="true">02</span></div><div class="section-content"><div class="section-heading"><h2>{ui['days']}</h2><a class="download-link" href="{download}" download>{ui['download']}<span aria-hidden="true">↓</span></a></div>{s(8,'h3','eyebrow format-label')}{s(9,'p','program-intro')}<div class="schedule">{day(107,163,19)}{day(163,196,20)}{day(196,229,21)}</div>{overview()}<details class="workshop-details" id="workshop-details-{lang}"><summary>{s(workshops,'span','day-title')}{toggle()}</summary><div class="workshop-body">{s(workshops+1)}{s(workshops+2,'h3')}{s(workshops+3)}{s(workshops+4,'h3')}{''.join(s(i) for i in range(workshops+5,committee))}</div></details></div></div></section>
  <section class="section abstracts-section shell" id="{anchor('abstracts')}"><div class="section-rail"><p class="eyebrow">{ui['abstracts']}</p><span class="section-number" aria-hidden="true">03</span></div><div class="section-content"><h2>{ui['abstracts']}</h2><div class="abstracts-list">{abstracts()}</div></div></section>
  <section class="section practical shell" id="{anchor('practical')}"><div class="section-rail">{s(33,'p','eyebrow')}<span class="section-number" aria-hidden="true">04</span></div><div class="section-content practical-grid"><div><h2>{ui['practical']}</h2>{s(4,'p','practical-date')}{s(5)}{s(6)}<a class="download-link" href="{download}" download>{ui['booklet']} — {ui['doclang']}<span aria-hidden="true">↓</span></a></div><div class="registration-panel" id="{anchor('registration')}"><h3>{ui['registration']}</h3>{s(0,'p','registration-description')}{register()}<p class="registration-status" {'hidden' if registration else ''}>{ui['pending']}</p></div></div></section>
 </main>
 <footer class="footer"><div class="shell"><div class="footer-grid"><div class="wordmark">DIALOGIA<span>MONTRÉAL 2026</span></div><div>{s(committee,'h2','eyebrow')}<div class="committee-names">{''.join(s(i,'span') for i in range(committee+1,committee+6))}</div></div><div>{s(institution,'h2','eyebrow')}{''.join(s(i,'p','institution-name') for i in range(institution+1,len(p)))}</div></div><div class="footer-bottom"><a href="{download}" download>{ui['booklet']} · {ui['doclang']}<span aria-hidden="true">↗</span></a><a href="?lang={opposite}" data-set-language="{opposite}" lang="{opposite}">{ui['other']}</a><a href="#{anchor('top')}">{ui['top']} ↑</a></div></div></footer>
 </div>'''

html='''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>DIALOGIA Montréal 2026 — Colloque scientifique</title>
<meta name="description" content="Dialogue interreligieux « assisté par » et « en dialogue avec » l’IA. 19–21 OCTOBRE 2026 · UNIVERSITÉ DE MONTRÉAL">
<meta name="theme-color" content="#142f44"><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' rx='3' fill='%23142f44'/%3E%3Ctext x='8' y='30' font-family='Georgia,serif' font-size='30' fill='white'%3ED%3C/text%3E%3C/svg%3E">
<script>try{document.documentElement.lang=new URLSearchParams(location.search).get('lang')==='en'?'en':'fr'}catch(e){}</script>
<link rel="stylesheet" href="/styles.css"><script src="/app.js" defer></script></head><body>
'''+page('fr')+page('en')+'</body></html>'
(ROOT/'dist/index.html').write_text(html)
print('Rendered both languages directly from the official source paragraphs.')
