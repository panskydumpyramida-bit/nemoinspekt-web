#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generuje statickou jednostránku Nemoinspekt (index.html) z reálného obsahu."""
import os, re

ROOT = os.path.expanduser("~/workspace/nemoinspekt-web")

# ---------------------------------------------------------------- DATA
LEADERSHIP = [
    ("jan-vales", "Ing. Jan Valeš", "Jednatel společnosti"),
    ("tomas-zima", "Ing. Tomáš Zima", "Ředitel společnosti · Hlavní inspektor · Předseda ZK AIN"),
    ("jan-brezina", "Ing. Jan Březina", "Hlavní inspektor · Revizor zakázek · ČKAIT"),
]

REVIEWS = [
    ("Pomůže vám rozhodovat se hlavou. Zachránila mě před koupí nádherného domu, který vůbec nebyl v tak dobrém stavu, jak bylo prezentováno.", "Alžběta Trusinová", "Starší nemovitost · inspekce před koupí"),
    ("Díky závěrečné zprávě máme důkladné zhodnocení stavebně-technického stavu domu. Lépe plánujeme a řídíme opravy v souladu s dlouhodobým plánem.", "Eva Širůčková", "Bytový dům · BD Zenklova, Praha"),
    ("Pan architekt z Nemoinspekt ušetřil našemu SVJ 500 000 Kč. Střecha, u které nám všichni tvrdili, že dorazila na konec životnosti, měla jen špatně udělanou okapnici.", "Marek Wiesner", "Bytový dům · audit pro SVJ"),
    ("Inspektorka se nenechala od zástupců developera odbýt a trvala na zaznamenání i nejmenších drobností. Při předávce jsem cítil, že nejsem ta slabší strana.", "Tomáš Koller", "Novostavba · přejímka novostavby v Praze"),
    ("Inspekce stála 10–15 tisíc. Na základě jejích zjištění se nám podařilo srazit cenu o 1,2 milionu. Dobrá investice.", "Tomáš Novella", "Starší nemovitost · inspekce před koupí"),
    ("We do not speak Czech and were looking for English-speaking professionals. Both Eliška at reception and inspector Kamila were helpful and professional. Highly recommend.", "Tuhin Khan", "Starší nemovitost · house inspection · English service"),
]

# kraj -> (zkratka, sloupec, řádek) pro dlaždicovou mapu ČR
MAP_POS = {
    "Ústecký": ("ULK", 3, 1), "Liberecký": ("LBK", 4, 1), "Královéhradecký": ("HKK", 5, 1),
    "Karlovarský": ("KVK", 1, 2), "Praha": ("PHA", 3, 2), "Pardubický": ("PAK", 5, 2),
    "Olomoucký": ("OLK", 6, 2), "Moravskoslezský": ("MSK", 7, 2),
    "Plzeňský": ("PLK", 1, 3), "Středočeský": ("STČ", 2, 3), "Vysočina": ("VYS", 4, 3), "Zlínský": ("ZLK", 6, 3),
    "Jihočeský": ("JHČ", 2, 4), "Jihomoravský": ("JHM", 4, 4),
}

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

# počty inspektorů na kraj
counts = {}
for _, _, _, reg in INSPECTORS:
    counts[reg] = counts.get(reg, 0) + 1

star = '<svg viewBox="0 0 24 24"><path d="M12 2l3 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.9 21l1.2-6.8-5-4.9 6.9-1z"/></svg>'

# --- reálná geografická SVG mapa ČR (z prototypu), kraje obarvené dle počtu inspektorů ---
def _norm(r):
    return r.replace("Kraj Vysočina", "Vysočina").replace(" kraj", "").strip()
_svg = open(os.path.join(ROOT, "assets", "cz-map.svg"), encoding="utf-8").read()
_svg = re.sub(r"-?\d+\.\d{2,}", lambda m: f"{float(m.group()):.1f}", _svg)  # zaokrouhli souřadnice
_maxc = max(counts.values())
def _path(m):
    a = m.group(1)
    dm = re.search(r'\sd="([^"]*)"', a)
    if not dm:
        return m.group(0)
    d = 'd="' + dm.group(1) + '"'
    rm = re.search(r'data-region="([^"]+)"', a)
    if not rm:
        return f'<path class="map-bg" {d}/>'
    region = rm.group(1); short = _norm(region); n = counts.get(short, 0)
    shade = 0.16 + 0.52 * (n - 1) / max(1, _maxc - 1)
    return (f'<path class="map-region" data-filter="{short}" data-count="{n}" data-name="{region}" '
            f'fill="rgba(139,177,77,{shade:.2f})" {d}/>')
map_svg = re.sub(r"<path\b([^>]*?)/?>", _path, _svg)
map_html = map_svg + ('<div class="map-info" id="mapInfo"><b>14 krajů ČR</b>'
                      '<span>Najeďte na kraj nebo klikněte pro výběr</span></div>')

# --- Oponentura: transparentní srovnání 3 verzí (kritérium: starý / rebuild / naše, 0–5) ---
OP_COLS = ["Starý web", "Komerční rebuild", "Naše verze"]
OPONENTURA = [
    ("Moderní design", 2, 4, 5),
    ("Úplnost webu (podstránky)", 5, 5, 2),
    ("Ceník + kalkulačka", 4, 5, 0),
    ("Tým + mapa inspektorů", 1, 4, 5),
    ("Recenze / sociální důkaz", 4, 4, 3),
    ("Blog & SEO obsah", 4, 5, 1),
    ("Animace & interaktivita", 1, 3, 5),
    ("Branding / nové logo", 1, 5, 5),
    ("Rebrand intro video", 0, 0, 5),
    ("EN verze", 3, 4, 0),
]
OP_AWARDS = [
    ("Nejúplnější produkční web", "Komerční rebuild"),
    ("Nejlepší motion &amp; rebrand launch", "Naše verze"),
    ("Unikátní TV reference (ČT, Receptář)", "Starý web"),
]

def _dots(n):
    return '<span class="op-dots">' + "".join(
        ('<i class="on"></i>' if i < n else '<i></i>') for i in range(5)) + "</span>"

_totals = [0, 0, 0]
_oprows = ""
for crit, *sc in OPONENTURA:
    mx = max(sc)
    for i, s in enumerate(sc):
        _totals[i] += s
    cells = "".join(
        f'<td class="op-score{" op-win" if s == mx and s > 0 else ""}">{_dots(s)}</td>'
        for s in sc)
    _oprows += f"<tr><th>{crit}</th>{cells}</tr>"
_max_total = max(_totals)
_tcells = "".join(
    f'<td class="op-total{" op-win" if _totals[i] == _max_total else ""}">{_totals[i]}<span>/50</span></td>'
    for i in range(3))
_oprows += f'<tr class="op-totalrow"><th>Celkem</th>{_tcells}</tr>'

_awards = "".join(
    f'<div class="op-award"><span class="op-medal"></span><div><b>{w}</b><span>{title}</span></div></div>'
    for title, w in OP_AWARDS)

oponentura_html = f'''<div class="op-intro">
  <span class="eyebrow">Oponentura</span>
  <h3>Srovnání tří verzí webu Nemoinspekt</h3>
  <p>Transparentní pohled na to, kde každá verze stojí. Tahle „naše" verze vznikla jako <b>oponentura a proof-of-concept</b> motion vrstvy a rebrandu — ne jako náhrada produkčního webu.</p>
</div>
<div class="op-table-wrap"><table class="op-table">
  <thead><tr><th>Kritérium</th><th>Starý web<span>nemoinspekt.cz</span></th><th>Komerční rebuild<span>dodavatel</span></th><th class="op-ours">Naše verze<span>tento web</span></th></tr></thead>
  <tbody>{_oprows}</tbody>
</table></div>
<div class="op-awards">{_awards}</div>
<p class="op-verdict"><b>Pořadí:</b> 1. Komerční rebuild &middot; 2. Naše verze &middot; 3. Starý web. Rebuild vede <b>úplností</b> (ceník, kalkulačka, blog, EN, 7 stránek služeb). Naše verze přidává <b>motion design, mapu na homepage a rebrand video</b> — ideální jako kampaňová launch stránka k rebrandu.</p>'''

# --- Slabiny rebuildu + konkurence + příležitosti (deep-research, 06/2026) ---
OP_GAPS = [
    ("Pojištění odpovědnosti se neukazuje", "Rebuild ho nikde neuvádí. Konkurent <b>Inspekce Lukeš</b> jím vědomě buduje důvěru („pojištění profesní odpovědnosti je naprostá samozřejmost&ldquo;)."),
    ("Žádná online rezervace termínu", "Jen poptávkový formulář. Nemá ji ale <b>nikdo</b> na českém trhu → největší šance se odlišit (zahraniční laťka: HomeInspections.com — vybrat inspektora, datum, potvrdit, zpráva do 24 h)."),
    ("Vzorová zpráva jen k prohlédnutí", "Varianty Standard/Premium k náhledu, ale <b>ne ke stažení v PDF</b>. Stejně na tom je i konkurence."),
    ("Slabší &bdquo;tvrdé&ldquo; certifikační důkazy", "Zmiňuje ČKAIT/ČKA, ale <b>Ensan</b> ukazuje konkrétní <b>čísla certifikátů</b> (AIN č.&nbsp;00063, TÜV, ČSOS č.&nbsp;014) — silnější důkaz."),
    ("Chybí případové studie a live chat", "Jen textové recenze + WhatsApp. Případovky („ušetřili jsme 1,2&nbsp;mil.&ldquo;) a chat jsou napříč trhem slabé."),
]
OP_COMPETITORS = [
    ("Nemoinspekt", "kalkulačka, od ~5 000 Kč", "AIN · ČKAIT · ČKA · 30+ inspektorů + mapa", "ne (poptávka)", True),
    ("NEMOPAS (sk. DEK)", "byt od 9 000 · dům od 11 000 Kč", "AIN · garant znalce DEKPROJEKT", "ne", False),
    ("Inspekce Lukeš", "byt od 11 990 · dům od 14 990 Kč", "ČKAIT · pojištění odpovědnosti", "ne", False),
    ("Ensan", "od 1 500 / 2 900 / 3 900 Kč", "AIN č.00063 · TÜV · ČSOS č.014", "ne", False),
]
OP_OPPS = [
    "Plně online <b>rezervace termínu</b> (vybrat inspektora → datum → potvrzení) — v ČR to nemá nikdo, vede k odlišení.",
    "<b>Stažitelná vzorová zpráva v PDF</b> přímo u CTA / ceníku.",
    "<b>Pojištění odpovědnosti</b> + certifikační <b>loga a čísla</b> (AIN, ČKAIT, ČKA) jako viditelné badges.",
    "<b>Případové studie</b> s konkrétní uchráněnou částkou + <b>live chat</b>.",
    "Jasný <b>příslib rychlosti</b> (zpráva do 24–72 h) jako konkurenční výhoda.",
]

_gaps = "".join(f"<li><b>{g}</b><span>{d}</span></li>" for g, d in OP_GAPS)
_comp = ""
for firma, ceny, duvera, rez, ours in OP_COMPETITORS:
    cls = ' class="op-ours-row"' if ours else ""
    _comp += f"<tr{cls}><th>{firma}</th><td>{ceny}</td><td>{duvera}</td><td class='op-c'>{rez}</td></tr>"
_opps = "".join(f"<li>{o}</li>" for o in OP_OPPS)

oponentura_html += f'''
<div class="op-section">
  <h4>Slabiny komerčního rebuildu</h4>
  <ul class="op-gaps">{_gaps}</ul>
</div>
<div class="op-section">
  <h4>Konkurence na českém trhu</h4>
  <p class="op-note">Nemoinspekt je jednou ze 4 dominantních firem (dle ČTK: NEMOPAS, Bytecheck, Nemoinspekt, Home Experts) sdružených v <b>AIN</b> — Asociaci inspektorů nemovitostí (~80–120 certifikovaných inspektorů, ~80&nbsp;% trhu).</p>
  <div class="op-table-wrap"><table class="op-table op-comp">
    <thead><tr><th>Firma</th><th>Orientační ceny</th><th>Klíčová důvěra</th><th>Online rezervace</th></tr></thead>
    <tbody>{_comp}</tbody>
  </table></div>
</div>
<div class="op-section">
  <h4>Příležitosti — kde může web vést trh</h4>
  <ol class="op-opps">{_opps}</ol>
</div>
<p class="op-source"><b>Metodika:</b> konkurenční data z deep-research (5 úhlů, 20 zdrojů, 89 tvrzení → 18 ověřeno adversariální verifikací 3 hlasy, 7 vyvráceno). Ceny jsou orientační „od&ldquo;, ověřeno 06/2026. Zdroje: ain.cz, nemopas.cz, inspekcelukes.cz, ensan.cz, ASHI Standard of Practice, HomeInspections.com.</p>'''

# recenze
reviews_html = ""
for i, (quote, author, meta) in enumerate(REVIEWS):
    reviews_html += (f'<div class="review-card">'
                     f'<div class="stars">{star*5}</div>'
                     f'<blockquote>„{quote}"</blockquote>'
                     f'<div class="who">{author}<span>{meta}</span></div></div>')

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
    "{{MAP}}": map_html, "{{REVIEWS}}": reviews_html, "{{OPONENTURA}}": oponentura_html,
}.items():
    HTML = HTML.replace(token, val)

with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(HTML)
print("index.html zapsáno (%d B)" % len(HTML))
