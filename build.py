#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generuje statickou jednostránku Nemoinspekt (index.html) z reálného obsahu."""
import os, re

ROOT = os.path.expanduser("~/workspace/nemoinspekt-web")

# ---------------------------------------------------------------- DATA
LEADERSHIP = [
    ("tomas-zima", "Ing. Tomáš Zima", "Ředitel společnosti · Hlavní inspektor · Předseda ZK AIN"),
    ("jan-brezina", "Ing. Jan Březina", "Hlavní inspektor · Revizor zakázek · ČKAIT"),
]

INSPECTORS = [
    ("marie-vyskocilova", "Ing. arch. Marie Vyskočilová", "Manažerka segmentu bytových domů", "Praha"),
    ("klara-kolovratova", "Ing. arch. Klára Kolovratová", "Inspektor · ČKA", "Praha"),
    ("stanislav-barta", "Stanislav Bárta", "Inspektor · ČKAIT", "Praha"),
    ("libor-pistelak", "Libor Pištělák", "Inspektor · ČKAIT", "Praha"),
    ("michal-panek", "Ing. Michal Pánek", "Inspektor · ČKAIT · Koordinátor BOZP", "Praha"),
    ("kamila-sindelarova", "Ing. arch. Kamila Šindelářová", "Inspektor · ČKA", "Praha"),
    ("vaclav-cerny", "Ing. Václav Černý", "Inspektor", "Praha"),
    ("jana-noskova", "Ing. arch. MgA Jana Nosková", "Inspektor", "Praha"),
    ("vaclav-tomasek", "Václav Tomášek", "Inspektor", "Praha"),
    ("jiri-lukes", "Ing. arch. Jiří Lukeš", "Inspektor · ČKA", "Středočeský"),
    ("milan-cermak", "Ing. Milan Čermák", "Inspektor · ČKAIT · Odhadce", "Středočeský"),
    ("jan-jelinek", "Ing. Jan Jelínek", "Inspektor · ČKAIT", "Jihočeský"),
    ("milos-patera", "Ing. Miloš Patera", "Inspektor · ČKAIT · Soudní znalec", "Karlovarský"),
    ("michal-huml", "Ing. Michal Huml", "Inspektor", "Plzeňský"),
    ("kurt-postupka", "Ing. Kurt Postupka, DiS", "Inspektor · ČKAIT", "Ústecký"),
    ("pavel-sulc", "Ing. Pavel Šulc", "Inspektor", "Liberecký"),
    ("martina-hepnerova", "Ing. Martina Hepnerová", "Inspektor · ČKAIT", "Královéhradecký"),
    ("lubos-svatos", "Ing. Luboš Svatoš", "Inspektor · ČKAIT", "Pardubický"),
    ("antonin-ruzicka", "Ing. Antonín Růžička", "Inspektor · Jihomoravský kraj, Slovensko", "Jihomoravský"),
    ("martin-zaoral", "Ing. Martin Zaoral", "Inspektor · ČKAIT", "Jihomoravský"),
    ("eva-uhlirova", "Ing. Eva Uhlířová", "Inspektor", "Jihomoravský"),
    ("petr-goldmann", "Ing. Petr Goldmann", "Inspektor", "Jihomoravský"),
    ("michal-baumann", "Ing. Michal Baumann", "Inspektor", "Jihomoravský"),
    ("zuzana-hrabanova", "Ing. arch. Zuzana Hrabaňová", "Inspektor · ČKA", "Vysočina"),
    ("jaromira-svestkova", "Ing. Jaromíra Švestková", "Inspektor · Třebíč, Jihlava, Žďár n. S.", "Vysočina"),
    ("pavel-svoboda", "Ing. Pavel Svoboda", "Inspektor · ČKAIT", "Olomoucký"),
    ("martin-cablik", "Ing. arch. Martin Čablík", "Inspektor · ČKA", "Moravskoslezský"),
    ("antonin-zavada", "Ing. arch. Bc. Antonín Závada, MBA", "Inspektor · Autorizovaný architekt", "Zlínský"),
]

CERTS = ["ČKAIT", "ČKA", "Soudní znalec", "Odhadce", "Koordinátor BOZP", "Autorizovaný architekt"]

AUDIENCE = [
    ("house-inspection", "Inspekce před koupí", "Byt, dům i pozemek prověříme dřív, než podepíšete. Zjistíte skutečný technický stav a reálné náklady na opravy.", "#kontakt"),
    ("novostavba", "Přejímka novostavby", "Převezměte byt nebo dům bez vad. Sepíšeme protokol o vadách a nedodělcích, který obstojí u developera.", "#kontakt"),
    ("apartment", "Technický audit pro SVJ", "Komplexní posouzení stavu bytového domu jako podklad pro plán oprav a rozhodování shromáždění.", "#kontakt"),
]

PRO_SERVICES = [
    ("Inspekce pro realitní makléře", "Profesionální zpráva z inspekce posílí důvěru kupujícího a zrychlí prodej."),
    ("Služby pro developery", "Přejímky od stavby, kontroly před klientskými přejímkami a technický dozor."),
    ("Technické due diligence", "Důkladné posouzení technického stavu nemovitosti před akvizicí."),
    ("Stavební dozor a poradenství", "Prověříme pozemek, pomůžeme vybrat zhotovitele a ohlídáme průběh stavby."),
]

CHECKS = [
    "Dispozice a výměry, pozemek",
    "Základy, nosné i nenosné konstrukce, střecha",
    "Exteriér a fasáda, hydroizolace a tepelná izolace",
    "Vnitřní instalace — voda, plyn, elektro, vytápění",
    "Interiéry, povrchy, zařizovací předměty",
    "Vstupní i interiérové dveře a okna",
    "Sklepy, garáže a společné prostory",
    "Požární bezpečnost a vlhkostní problémy",
]

PROCESS = [
    ("01", "Poptáte a domluvíme termín", "Reakce do 15 minut · termín standardně do 48 hodin",
     "Odešlete formulář, napište na info@nemoinspekt.cz nebo zavolejte. Vybereme inspektora ve vašem regionu a navrhneme termín, který vám sedí."),
    ("02", "Provedeme inspekci", "Byt 1–2 hodiny, dům 2–3 hodiny",
     "Inspektor přijede, detailně prohlédne nemovitost a hlavní zjištění vám sdělí hned po kontrole na místě."),
    ("03", "Obdržíte zprávu", "Standardně do 3 pracovních dní, expres do 24 hodin",
     "Detailní zpráva přijde mailem v PDF. Před odesláním ji reviduje hlavní inspektor — kontrola 4 očí."),
]

FAQ = [
    ("Co je inspekce nemovitostí a co všechno zahrnuje?",
     "Je to podrobný vizuální průzkum technického stavu nemovitosti. Prověříme konstrukce, střechu, fasádu a izolace, vnitřní instalace (voda, plyn, elektro, vytápění), okna a dveře, povrchy, sklepy i společné prostory. Výstupem je přehledná PDF zpráva se zjištěnými závadami a odhadem nákladů na opravy."),
    ("Kolik stojí inspekce nemovitosti?",
     "Cena se odvíjí od typu a velikosti nemovitosti a rozsahu prohlídky. Ozvěte se nám a nezávazně vám ji spočítáme — proti uchráněným statisícům na skrytých vadách jde o zlomek hodnoty."),
    ("Jak rychle můžete provést inspekci?",
     "Termín nabízíme standardně do 48 hodin, zprávu dodáme do 3 pracovních dní. Když vám hoří termín, zvládneme inspekci i zprávu v expresním režimu do 24 hodin."),
    ("Jsou vaši inspektoři certifikovaní?",
     "Ano. Náš tým tvoří inženýři a architekti autorizovaní u ČKAIT a ČKA, mezi nimi soudní znalci a odhadci. Každou zprávu navíc reviduje hlavní inspektor."),
    ("Vyplatí se inspekce i u novostavby?",
     "Rozhodně. I u nových staveb běžně nacházíme desítky vad a nedodělků. Protokol z přejímky vám pomůže vymoci jejich odstranění po developerovi včas a zdarma."),
]

# ---------------------------------------------------------------- HELPERS
def chips(role):
    found = [c for c in CERTS if c in role]
    return "".join('<span class="chip">%s</span>' % c for c in found)

def role_clean(role):
    # odeber certifikace z popisné role, nech hlavní titul
    parts = [p.strip() for p in role.split("·")]
    keep = [p for p in parts if p not in CERTS]
    return " · ".join(keep) if keep else parts[0]

def member_card(photo, name, role, region, delay):
    return f'''<article class="member reveal" style="transition-delay:{delay}ms" data-region="{region}">
  <div class="member-photo"><img src="assets/team/{photo}.webp" alt="{name}" loading="lazy" width="300" height="300"></div>
  <div class="member-meta">
    <span class="member-region">{region}</span>
    <h4>{name}</h4>
    <p>{role_clean(role)}</p>
    <div class="chips">{chips(role)}</div>
  </div>
</article>'''

# leadership cards (větší)
lead_html = ""
for i, (p, n, r) in enumerate(LEADERSHIP):
    lead_html += f'''<article class="lead-card reveal" style="transition-delay:{i*90}ms">
  <div class="lead-photo"><img src="assets/team/{p}.webp" alt="{n}" loading="lazy" width="320" height="320"></div>
  <div class="lead-meta"><span class="member-region">Vedení</span><h4>{n}</h4><p>{r}</p></div>
</article>'''

team_html = "".join(member_card(p, n, r, reg, (i % 4) * 70) for i, (p, n, r, reg) in enumerate(INSPECTORS))

regions = []
for _, _, _, reg in INSPECTORS:
    if reg not in regions:
        regions.append(reg)
filter_html = '<button class="filter-btn active" data-filter="all">Všechny kraje</button>' + \
    "".join(f'<button class="filter-btn" data-filter="{r}">{r}</button>' for r in regions)

audience_html = ""
for i, (icon, title, desc, href) in enumerate(AUDIENCE):
    audience_html += f'''<a class="route reveal" href="{href}" style="transition-delay:{i*90}ms">
  <div class="route-icon"><img src="assets/icons/audience-routes/{icon}.svg" alt="" width="40" height="40"></div>
  <h3>{title}</h3>
  <p>{desc}</p>
  <span class="route-link">Více <svg viewBox="0 0 24 24" class="arr"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>
</a>'''

pro_html = ""
for i, (title, desc) in enumerate(PRO_SERVICES):
    pro_html += f'''<div class="pro reveal" style="transition-delay:{i*70}ms">
  <h4>{title}</h4><p>{desc}</p>
  <a href="#kontakt" class="pro-link">Více <svg viewBox="0 0 24 24" class="arr"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
</div>'''

checks_html = "".join(
    f'''<li class="reveal" style="transition-delay:{i*50}ms"><svg viewBox="0 0 24 24" class="ck"><path d="M20 6L9 17l-5-5"/></svg>{c}</li>'''
    for i, c in enumerate(CHECKS))

process_html = ""
for i, (num, title, meta, desc) in enumerate(PROCESS):
    process_html += f'''<div class="step reveal" style="transition-delay:{i*120}ms">
  <div class="step-num"><span>{num}</span></div>
  <div class="step-body"><h3>{title}</h3><span class="step-meta">{meta}</span><p>{desc}</p></div>
</div>'''

faq_html = ""
for i, (q, a) in enumerate(FAQ):
    faq_html += f'''<div class="faq-item reveal">
  <button class="faq-q" aria-expanded="false"><span>{q}</span><svg viewBox="0 0 24 24" class="faq-ico"><path d="M12 5v14M5 12h14"/></svg></button>
  <div class="faq-a"><p>{a}</p></div>
</div>'''

# ---------------------------------------------------------------- TEMPLATE
HTML = open(os.path.join(ROOT, "template.html"), encoding="utf-8").read()
for token, val in {
    "{{LEAD}}": lead_html, "{{TEAM}}": team_html, "{{FILTERS}}": filter_html,
    "{{AUDIENCE}}": audience_html, "{{PRO}}": pro_html, "{{CHECKS}}": checks_html,
    "{{PROCESS}}": process_html, "{{FAQ}}": faq_html,
}.items():
    HTML = HTML.replace(token, val)

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("index.html zapsáno (%d B)" % len(HTML))
