"""Generates the static pages of liomaix.github.io.
Edit the content below, then run:  python3 build.py
Equations use LaTeX between \\[ ... \\] (display) or \\( ... \\) (inline); KaTeX renders them in the browser.
Topics: "cyber", "climate", "micro" (each has its own colour)."""
import os

OUT = "."
PAGES = [("about.html", "About"), ("research.html", "Research"), ("publications.html", "Publications"),
         ("talks.html", "Talks"), ("teaching.html", "Teaching"), ("cv.html", "CV")]
TOPIC_NAMES = {"cyber": "Cyber Risk", "climate": "Climate Transition Risk", "micro": "Market Microstructure"}
DESC = ("Lionel Sopgoui, postdoctoral researcher in mathematical and actuarial finance at ENSAE Paris "
        "and Institut Louis Bachelier, working on cyber risk, climate transition risk and market microstructure.")
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#1b8a8f"/>'
        '<path d="M5 24 L11 21 L11 14 L17 12 L21 13 L21 6 L27 5" stroke="#fff" stroke-width="2.4" fill="none" '
        'stroke-linecap="round" stroke-linejoin="round"/><path d="M11 21 L11 14 M21 13 L21 6" stroke="#e5a53a" '
        'stroke-width="2.6" stroke-linecap="round"/></svg>')
FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' "
           "rx='7' fill='%231b8a8f'/><path d='M5 24 L11 21 L11 14 L17 12 L21 13 L21 6 L27 5' stroke='white' "
           "stroke-width='2.4' fill='none' stroke-linecap='round' stroke-linejoin='round'/></svg>")
KATEX = r"""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}],throwOnError:false})"></script>
"""


def head(title, current, math=False):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in PAGES)
    full = "Lionel Sopgoui" if current == "index.html" else f"{title} | Lionel Sopgoui"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#0b2433">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://liomaix.github.io/profile_.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
{KATEX if math else ""}<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">{LOGO}Lionel Sopgoui</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
  </div>
</header>
"""


FOOT = """<footer class="site-footer">
  <div class="wrap">
    <nav aria-label="Elsewhere">
      <a href="https://www.ensae.fr/">ENSAE Paris</a>
      <a href="https://www.institutlouisbachelier.org/">Institut Louis Bachelier</a>
      <a href="https://scholar.google.com/citations?user=rdoDR00AAAAJ&hl=en">Google Scholar</a>
      <a href="https://github.com/liomaix">GitHub</a>
      <a href="https://uk.linkedin.com/in/lionel-sopgoui">LinkedIn</a>
      <a href="mailto:maixent.sopgoui@outlook.com">maixent.sopgoui@outlook.com</a>
    </nav>
    <span>© 2026 Lionel Sopgoui</span>
  </div>
</footer>
<script src="main.js"></script>
</body>
</html>
"""


def page_head(title, lede):
    return f"""<div class="band page-head">
  <svg class="paths" data-n="5" aria-hidden="true"></svg>
  <div class="wrap"><h1>{title}</h1><p>{lede}</p></div>
</div>
"""


def write(name, title, body, math=False):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(head(title, name, math) + body + FOOT)


def chips(topics):
    return "".join(f'<span class="chip t-{t}">{TOPIC_NAMES[t]}</span>' for t in topics)


def entry(title, url, meta, topics=(), status=None, extra=""):
    cls = f"t-{topics[0]}" if topics else "t-none"
    st = f'<span class="status">{status}</span>' if status else ""
    t = f'<a href="{url}">{title}</a>' if url else title
    ch = f'<span class="chips">{chips(topics)}</span>' if topics else ""
    return (f'<li class="{cls}" data-topics="{" ".join(topics) or "other"}"><span class="entry-title">{t}{st}</span>'
            f'<span class="meta">{meta}</span>{extra}{ch}</li>')


def filters(*lists):
    """Filter buttons, only for topics that appear in the given lists of entries."""
    html = "".join("".join(x) for x in lists)
    b = '<button type="button" class="t-none" data-f="all" aria-pressed="true">All</button>'
    b += "".join(f'<button type="button" class="t-{k}" data-f="{k}" aria-pressed="false">{v}</button>'
                 for k, v in TOPIC_NAMES.items() if f'class="chip t-{k}"' in html)
    return f'<div class="filters" role="group" aria-label="Filter by topic">{b}</div>'


# ---------------------------------------------------------------- equations
EQ = {
    "hawkes": r"""\begin{aligned}d\widehat H_t = (\varpi\widehat z_t-\rho\widehat H_t)d t + \bar\sigma\,d W_t
       - \sum_{\tau_i \leq t} \kappa_i H_{\tau_i^-} S(H_{\tau_i^-}, \upsilon_{\tau_i})\end{aligned}""",
    "sir": r"\mathrm{d}I_t=(\beta S_t-\gamma)\,I_t\,\mathrm{d}t+\sigma I_t\,\mathrm{d}W_t",
    "gpd": r"\mathbb{P}(X-u\gt x\mid X\gt u)\approx\Big(1+\frac{\xi x}{\sigma}\Big)^{-1/\xi}",
    "firm": r"V_t=\mathbb{E}_t\!\left[\int_t^{\infty}e^{-r(s-t)}\,\Pi_s(\delta_s)\,\mathrm{d}s\right]",
    "option": r"u(p)=\sup_{\tau}\,\mathbb{E}_p\big[e^{-r\tau}(P_\tau-K)^+\big]",
    "loss": r"L_T=\sum_{i=1}^{n}\mathrm{EAD}_i\,\mathrm{LGD}_i\,\mathbf{1}_{\{\tau_i\le T\}}",
    "rp": r"r_t=S_t-q_t\,\gamma\,\sigma^2\,(T-t)",
    "fill": r"\lambda^{\pm}(\delta)=A\,e^{-k\,\delta}",
    "lgd": r"\mathrm{LGD}_i=\Big(1-\frac{C^i_{\tau_i}}{\mathrm{EAD}_i}\Big)^{+}",
    "lgd_qf": r"\mathrm{LGD}^n_t=(1-\gamma)\,\mathbb{E}\Big[\Big(1-(1-k)\,e^{-ra}\frac{C^n_{t+a}}{\mathrm{EAD}^n_t}\Big)^{+}\,\Big|\,V^n_t\lt D^n_t,\,\mathcal{G}_t\Big]",
    "profit": r"\pi^i_t=e^{-\gamma(T_t-T_0)}\nu^i_tK^i_t-(\omega^i_t+r^i_t)K^i_t-\tfrac{\chi}{2}\tfrac{(I^i_t)^2}{\bar K_{t-1}}-\big(y^i_tK^i_t-E^{i,\mathrm{target}}_t\big)\delta_t",
    "damage": r"\bar c^{\,i}_t=\big(\omega^i_t+r^i_t+y^i_t\,\delta_t\big)\,e^{\gamma(T_t-T_0)}",
    "sir17": r"\frac{\mathrm{d}I_{k,t}}{\mathrm{d}t}=-\gamma_{k,t}I_{k,t}+Y_t\sum_{j=k}^{K}jS_{j,t}\,b_{jk,t}",
    "force": r"Y_t=\frac{1}{N_0}\sum_{k=1}^{K}\beta_{k,t}\,kI_{k,t}",
    "mfg_obj": r"J_d(H_0,z)=\mathbb{E}^{\mathbb{Q}}\Big[U_d\Big(L^\star_T-L_T-\int_0^T\big(c_1Az_t+\tfrac{c_2}{2}(Az_t)^2+A\pi_t\big)\,\mathrm{d}t\Big)\Big]",
}


def eq(key, caption):
    return f'<div class="eq">\\[{EQ[key]}\\]<small>{caption}</small></div>'


# ---------------------------------------------------------------- publications
ME = "<strong>L. Sopgoui</strong>"
PREPRINTS = [
    entry("Climate-vulnerable firms, credit supply, and cascading failures: an agent-based model",
          "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6879501",
          f"{ME}. SSRN 6879501, 2026. Submitted to <em>Economic Modelling</em>.", ("climate",), "Preprint"),
    entry("Modeling the impact of climate transition on real estate prices", "https://arxiv.org/abs/2408.02339",
          f"{ME}. arXiv:2408.02339, 2024. Submitted to <em>Journal of Climate Finance</em>.", ("climate",), "Preprint"),
]
JOURNAL = [
    entry("A stochastic SIR model for cyber contagion: application to granular growth of firms and to insurance portfolio",
          "https://doi.org/10.1080/03461238.2026.2734133",
          f"C. Hillairet, O. Lopez, {ME}. <em>Scandinavian Actuarial Journal</em>, 1–34, 2026.", ("cyber",)),
    entry("Impact of the carbon price on credit portfolio’s loss with stochastic collateral",
          "https://doi.org/10.1080/14697688.2025.2577121",
          f"{ME}. <em>Quantitative Finance</em>, 1–30, 2025.", ("climate",)),
    entry("Propagation of a carbon price in a credit portfolio through macroeconomic factors",
          "https://epubs.siam.org/doi/10.1137/24M1655718",
          f"G. Bouveret, J.-F. Chassagneux, S. Ibbou, A. Jacquier, {ME}. <em>SIAM Journal on Financial Mathematics</em>, 16(2):545–605, 2025.",
          ("climate",)),
]
THESIS = [entry("Pricing and hedging of transition risk in credit portfolio", "https://hal.science/tel-04882729v1",
                f"{ME}. PhD thesis, Université Paris Cité, 2024.", ("climate",))]
OTHER = [entry("Les essais de Paukémil, l’intrus universel",
               "https://www.bod.fr/librairie/les-essais-de-paukemil-lionel-sopgoui-9782322274079",
               f"{ME}. <em>Books on Demand</em>, 2021. Essays, in French.")]


# ---------------------------------------------------------------- talks
def topics_of(title):
    t = title.lower()
    out = []
    if "cyber" in t: out.append("cyber")
    if "climate" in t or "carbon" in t: out.append("climate")
    if any(k in t for k in ("microstructure", "order book", "market making", "execution", "liquidity")): out.append("micro")
    return tuple(out)


def talk(name, url, dates, title, place, slides=None, cancelled=False):
    tp = topics_of(title)
    s = f' · <a href="files/{slides}">Slides</a>' if slides else ""
    li = entry(name, url, f"{dates} · {place}{s}", tp, "Not held" if cancelled else None,
               extra=f'<span class="meta"><em>{title}</em></span>')
    return li.replace('<li class="', '<li class="cancelled ', 1) if cancelled else li


CYB = "A stochastic SIR model for cyber contagion: from granular growth of firms to insurance portfolio"
TALKS = {
    "Upcoming": [
        talk("Mathematical Advances on Emerging Risks 2026", "https://thomaspeyrat.github.io/Merida_2026.github.io/index.html",
             "3–6 November 2026", "A major–minor MFG with common jumps and impulse control for optimal cybersecurity investment",
             "Mexico City, Mexico"),
    ],
    "2026": [
        talk("7th European Actuarial Journal Conference", "https://www.eaj2026istanbul.org/", "9–11 September", CYB,
             "Istanbul, Turkey", "7th_EAJ_Conference_Sopgoui.pdf"),
        talk("CEMRACS 2026", "https://cemracs2026.math.cnrs.fr/en/", "20 July – 14 August",
             "Dynamic top-down model for financial loss distribution under climate, credit and market risks "
             "(with D. Bastide, S. Crépey, S. Pavarana, R. Timeus)", "CIRM, Marseille, France"),
        talk("XIII Bachelier World Congress", "https://eventi.unibo.it/bachelier", "29 June – 3 July", CYB, "Bologna, Italy"),
        talk("Scandinavian Actuarial Conference 2026", "https://sites.google.com/view/sac2026/", "15–16 June", CYB,
             "Stockholm University, Sweden"),
        talk("Financial Risks International Forum 2026", "https://www.risks-forum.org/", "30–31 March", CYB,
             "Palais Brongniart, Paris, France"),
        talk("XXVII Workshop on Quantitative Finance", "https://qfw2026.unibg.it/", "30–31 March", CYB, "Bergamo, Italy"),
    ],
    "2025": [
        talk("Quantitative Methods in Finance 2025", "https://qmf2025.exordo.com", "16–19 November",
             "Impact of the carbon price on credit portfolio’s loss with stochastic collateral",
             "University of Technology Sydney, Australia", "QFM_Sydney_2025.pdf"),
        talk("Séminaire Actuariat &amp; Finance (IRA-ISFA-ENSAE-CNAM-ISUP)",
             "https://gains.univ-lemans.fr/fr/actualites/agenda-2025/novembre/e-seminaire-actuariat-finance.html", "21 November",
             "A stochastic SIRS model for cyber contagion: application to firms’ growth and insurance portfolios",
             "Institut du Risque &amp; de l’Assurance, Le Mans, France"),
        talk("SIAM Conference on Financial Mathematics and Engineering (FM25)",
             "https://www.siam.org/conferences-events/past-event-archive/fm25", "15–18 July",
             "Modeling the impact of climate transition on real estate prices", "Miami, Florida, USA"),
        talk("EconophysiX seminar", "https://www.econophysix.com/news", "8 April",
             "A top-down and a bottom-up approach for financial fragility under climate change",
             "Capital Fund Management, Paris, France", "CFM_2025.pdf"),
        talk("UCLA Financial and Actuarial Mathematics Seminar",
             "https://secure.math.ucla.edu/seminars/display.php?&amp;id=838987", "20 February",
             "Pricing and hedging of climate transition risk in credit portfolio", "UCLA (online)", "UCLA_2025.pdf"),
        talk("London–Oxford–Warwick Financial Mathematics Workshop",
             "https://sites.google.com/view/london-oxford-warwick-workshop/", "9–10 January",
             "Modeling the impact of climate transition on real estate prices", "University of Oxford, England"),
    ],
    "2024": [
        talk("9th Green Finance Research Advances", "https://green-finance-research-advances-2024.org/", "9–10 December",
             "Impact of climate transition on credit-portfolio loss with stochastic collateral", "Banque de France, Paris, France"),
        talk("Groupe de Travail – Risques Climatiques", "https://www.lpsm.paris/seminaires/gtfinanceprobanumeriques/index",
             "17 October", "Modeling the impact of climate transition on real estate prices", "CACIB, Montrouge, France"),
        talk("12th Bachelier World Congress", "https://eventos.fgv.br/bachelier-2024", "8–12 July",
             "Propagation of carbon taxes in credit portfolio through macroeconomic factors", "FGV EMAp, Rio de Janeiro, Brazil"),
        talk("XXV Workshop on Quantitative Finance", "https://eventi.unibo.it/qfw2024", "11–13 April",
             "Impact of climate transition on credit-portfolio loss with stochastic collateral", "Università di Bologna, Italy"),
        talk("Séminaire Bachelier", "http://www.bachelier-paris.fr/programme/", "9 February",
             "Impact of climate transition on loss given default with stochastic collaterals",
             "Institut Henri Poincaré, Paris, France"),
    ],
    "2023": [
        talk("8th Green Finance Research Advances", "https://indico.cern.ch/event/1286716/", "13–14 December",
             "Propagation of carbon taxes in credit portfolio through macroeconomic factors", "Banque de France, Paris, France"),
        talk("European Summer School in Financial Mathematics",
             "https://www.tudelft.nl/en/events/2023/eemcs/diam/finance-summer-school-2023", "4–8 September",
             "Propagation of carbon taxes in credit portfolio through macroeconomic factors", "TU Delft, The Netherlands"),
        talk("London/Oxford/Warwick Financial Mathematics Workshop",
             "https://www.kcl.ac.uk/events/londonoxfordwarwick-financial-mathematics-workshop-1", "12–13 July",
             "Diffusion of carbon price in credit portfolio through macroeconomic factors", "King’s College London, England",
             "Oxford_London_Warwick_2023.pdf"),
        talk("MathRisk Conference on Numerical Methods in Finance", "https://mathrisk2023.sciencesconf.org/", "14–16 June",
             "Propagation of carbon tax in credit portfolio through macroeconomic factors", "University of Udine, Italy",
             cancelled=True),
        talk("SIAM Conference on Financial Mathematics and Engineering (FM23)",
             "https://www.siam.org/conferences/cm/conference/fm23", "6–9 June",
             "Propagation of carbon tax in credit portfolio through macroeconomic factors", "Philadelphia, Pennsylvania, USA",
             cancelled=True),
        talk("Groupe de travail des thésards du LPSM", "https://www.lpsm.paris/seminaires/gtt/index", "30 May",
             "Propagation of carbon tax in credit portfolio through macroeconomic factors", "Sorbonne Université, Paris, France"),
        talk("Quantitative Finance Workshop 2023", "https://qfw2023.unicas.it/", "20–22 March",
             "Diffusion of carbon price in credit portfolio through macroeconomic factors", "Università di Cassino, Gaeta, Italy"),
    ],
    "2022": [
        talk("London–Paris Bachelier Workshop (6th edition)", "http://www.bachelier-paris.fr/london-paris-bachelier-workshop/",
             "15–16 September", "Diffusion of carbon price in a credit portfolio through macroeconomic factors",
             "Institut Henri Poincaré, Paris, France"),
    ],
}

# ---------------------------------------------------------------- news
NEWS = [
    ("Nov 2026", "cyber", 'Upcoming talk at <a href="https://thomaspeyrat.github.io/Merida_2026.github.io/index.html">Mathematical Advances on Emerging Risks 2026</a> in Mexico City, on a major–minor mean-field game for optimal cybersecurity investment.'),
    ("Sep 2026", "cyber", 'Our paper with Caroline Hillairet and Olivier Lopez, <a href="https://doi.org/10.1080/03461238.2026.2734133">A stochastic SIR model for cyber contagion</a>, is published in the <em>Scandinavian Actuarial Journal</em>.'),
    ("Sep 2026", "cyber", 'Presented our cyber-contagion SIR model at the <a href="https://www.eaj2026istanbul.org/">7th European Actuarial Journal Conference</a> in Istanbul (<a href="files/7th_EAJ_Conference_Sopgoui.pdf">slides</a>).'),
    ("Jul 2026", "climate", 'Joined <a href="https://cemracs2026.math.cnrs.fr/en/">CEMRACS 2026</a> at CIRM Marseille to build a dynamic top-down model for losses under climate, credit and market risks.'),
    ("Mar 2026", "cyber", 'New preprint with Caroline Hillairet and Olivier Lopez: <a href="https://hal.science/hal-05555552v1">A stochastic SIR model for cyber contagion</a>.'),
    ("2026", "climate", 'New preprint: <a href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6879501">Climate-vulnerable firms, credit supply, and cascading failures: an agent-based model</a>.'),
    ("2025", "climate", 'Published in <em>Quantitative Finance</em>: <a href="https://doi.org/10.1080/14697688.2025.2577121">Impact of the carbon price on credit portfolio’s loss with stochastic collateral</a>.'),
]

ICON = {
    "research": '<path d="M4 26 L10 22 L10 15 L16 13 L21 14 L21 7 L28 5"/><path d="M4 28 H28"/>',
    "publications": '<path d="M8 4 H20 L25 9 V28 H8 Z"/><path d="M20 4 V9 H25"/><path d="M12 15 H21 M12 19 H21 M12 23 H18"/>',
    "talks": '<rect x="4" y="5" width="24" height="16" rx="1.5"/><path d="M16 21 V27 M11 27 H21"/><path d="M8 16 L13 12 L17 14 L23 9"/>',
    "teaching": '<path d="M3 11 L16 5 L29 11 L16 17 Z"/><path d="M8 13.5 V21 C11 24 21 24 24 21 V13.5"/><path d="M29 11 V19"/>',
    "cv": '<rect x="6" y="4" width="20" height="24" rx="1.5"/><circle cx="16" cy="12" r="3.2"/><path d="M11 21 C12 17.5 20 17.5 21 21"/>',
    "about": '<circle cx="16" cy="11" r="5"/><path d="M6 27 C7 20 25 20 26 27"/>',
}


def tile(href, key, label, text, t):
    return (f'<a class="tile t-{t}" href="{href}"><span class="ic"><svg viewBox="0 0 32 32" aria-hidden="true">{ICON[key]}</svg></span>'
            f'<strong>{label}</strong><span>{text}</span></a>')


# ---------------------------------------------------------------- pages
def build():
    news = "".join(f'<li class="t-{t}"><time>{d}</time><div>{txt}</div></li>' for d, t, txt in NEWS)
    home = f"""<div class="band hero">
  <svg class="paths" data-n="9" data-animate="true" aria-hidden="true"></svg>
  <div class="wrap">
    <div>
      <h1>Lionel Sopgoui</h1>
      <p class="role">Postdoctoral researcher in mathematical and actuarial finance</p>
      <p class="affil">ENSAE Paris and Institut Louis Bachelier<br>Paris, France</p>
      <div class="links">
        <a class="primary" href="files/CV_Lionel_Sopgoui.pdf">CV (PDF)</a>
        <a href="https://scholar.google.com/citations?user=rdoDR00AAAAJ&hl=en">Google Scholar</a>
        <a href="https://github.com/liomaix">GitHub</a>
        <a href="https://uk.linkedin.com/in/lionel-sopgoui">LinkedIn</a>
        <a href="https://twitter.com/liomaix">X</a>
        <a href="mailto:maixent.sopgoui@outlook.com">Email</a>
      </div>
      <div class="eq-card">\\[{EQ["hawkes"]}\\]<p><b>Cybersecurity level dynamics:</b> mean-reverting diffusion with a downward jump at each cyber incident.</p></div>
    </div>
    <div class="portrait-frame"><img class="portrait" src="profile_.jpg" alt="Portrait of Lionel Sopgoui" width="2000" height="1500" fetchpriority="high"></div>
  </div>
</div>
<main id="main" class="wrap">
  <section>
    <h2>Research</h2>
    <p class="lede">I build stochastic models that follow shocks from firms to the banks and insurers exposed to them: cyber epidemics through insurance portfolios, carbon prices and warming through credit portfolios, and order flow through prices.</p>
    <div class="topics">
      <div class="topic t-cyber"><h3>Cyber Risk</h3><p>How attacks spread between firms, and what they cost insurers and defenders.</p>{eq("force", "Force of infection of the cyber epidemic")}</div>
      <div class="topic t-climate"><h3>Climate Risk</h3><p>How the carbon price and global warming reach firms, collateral and banks.</p>{eq("damage", "Effective cost per unit of output: raised by warming and by the carbon price")}</div>
      <div class="topic t-micro"><h3>Market Microstructure</h3><p>How order flow, liquidity and trading strategies shape prices in limit order books.</p>{eq("rp", "Market maker’s reservation price")}</div>
    </div>
    <p class="more"><a href="research.html">Research themes and ongoing work</a></p>
  </section>

  <section>
    <h2>News</h2>
    <ul class="news">{news}</ul>
  </section>

  <section>
    <h2>Recent publications</h2>
    <ul class="entries">{"".join(PREPRINTS[:2] + JOURNAL)}</ul>
    <p class="more"><a href="publications.html">All publications</a></p>
  </section>

  <section>
    <h2>Explore</h2>
    <div class="tiles">
      {tile("research.html", "research", "Research", "Themes, ongoing work and projects", "none")}
      {tile("publications.html", "publications", "Publications", "Preprints, articles and thesis", "cyber")}
      {tile("talks.html", "talks", "Talks", "Conferences and seminars since 2022", "climate")}
      {tile("teaching.html", "teaching", "Teaching", "Financial mathematics at ENSAE", "micro")}
      {tile("cv.html", "cv", "CV", "Education and full résumé", "cyber")}
      {tile("about.html", "about", "About", "Background and life outside research", "climate")}
    </div>
  </section>
</main>
"""
    write("index.html", "Home", home, math=True)

    write("about.html", "About", page_head("About", "Mathematician working where probability meets risk management.") + """<main id="main" class="wrap">
   <section class="prose">
    <h2>Background</h2>
    <p>I am a postdoctoral researcher in mathematical and actuarial finance at <a href="https://www.ensae.fr/">ENSAE Paris</a> (CREST) and the <a href="https://www.institutlouisbachelier.org/">Institut Louis Bachelier</a>, working with <a href="https://sites.google.com/site/carolinehillairet">Prof. Caroline Hillairet</a> and <a href="https://sites.google.com/view/sitepersonneldolivierlopez/home">Prof. Olivier Lopez</a> on cyber risk for finance and insurance. We model cyber epidemics with stochastic multi-group SIR dynamics coupled to a granular model of firm growth, and translate them into firms’ revenue losses and the aggregate exceedance probability of a cyber-insurance portfolio. We also study optimal cybersecurity investment as a major–minor mean-field game, in which firms defend against a ransomware group that chooses when and how hard to strike. This work is part of the CyFi project, with the startup Citalid and the support of Bpifrance.</p>
    <p>I completed a PhD in mathematical finance at <a href="https://www.lpsm.paris/">Université Paris Cité</a>, with research visits at <a href="https://www.imperial.ac.uk/mathematical-finance/">Imperial College London</a>, funded by a CIFRE grant with the Risk division of BPCE S.A. My thesis, <em>Pricing and hedging of transition risk in credit portfolio</em>, followed a carbon price from a multisectoral economy to firm values, default probabilities, collateral and the losses of a bank’s credit portfolio. I was co-advised by <a href="https://chssgnx.github.io">Jean-François Chassagneux</a>, <a href="https://jackantoinejacquie.wixsite.com/jacquier">Antoine (Jack) Jacquier</a> and <a href="https://www.linkedin.com/in/smail-ibbou-31a73b5/">Smail Ibbou</a>.</p>
    <p>I continue to work on climate risk. With agent-based models of heterogeneous firms and a bank, I study how physical and transition risk combine and how credit rationing turns them into cascading failures.</p>
  </section>
  <section class="prose">
    <h2>Outside research</h2>
    <ul class="plain">
      <li>Regular runner and tennis player.</li>
      <li>Writer and philosopher; author of <a href="https://www.bod.fr/librairie/les-essais-de-paukemil-lionel-sopgoui-9782322274079"><em>Les essais de Paukémil, l’intrus universel</em></a>.</li>
      <li>Fan of basketball (Golden State Warriors), tennis (Novak Djokovic) and cycling.</li>
      <li>Traveler.</li>
    </ul>
  </section>
  <section class="prose">
    <h2>Contact</h2>
    <p>Email: <a href="mailto:sopgoui@lpsm.paris">sopgoui@lpsm.paris</a></p>
  </section>
</main>
""")

    write("research.html", "Research", page_head("Research", "Stochastic models for emerging risks, the climate transition and financial markets.") + f"""<main id="main" class="wrap">
  <section>
    <h2>Themes</h2>
    <div class="topics rows">
      <div class="topic row wide t-cyber"><div><h3>Cyber Risk</h3><p>Stochastic multi-group SIR models coupled with granular firm growth to measure the impact of cyber epidemics on firms and insurance portfolios, and major–minor mean-field games in which firms choose their cybersecurity investment against a strategic ransomware group.</p></div>
        <div class="eqs">{eq("sir17", "Infected firms of size k (Scandinavian Actuarial Journal, 2026)")}{eq("mfg_obj", "Defender’s objective in the major–minor mean-field game (ongoing work)")}</div></div>
      <div class="topic row wide t-climate"><div><h3>Climate Transition Risk</h3><p>How a carbon price and global warming propagate to firm values, collateral, credit losses and bank equity, from closed-form credit models to agent-based economies with cascading failures.</p></div>
        <div class="eqs">{eq("lgd_qf", "Loss given default with stochastic collateral (Quantitative Finance, 2025)")}{eq("profit", "Firm profit under physical and transition risk (agent-based model, 2026)")}</div></div>
      <div class="topic row t-micro"><div><h3>Market Microstructure</h3><p>Price formation and liquidity in limit order books, market making and optimal execution, and statistical and learning-based trading strategies.</p></div>
        <div class="eqs">{eq("rp", "Reservation price of an inventory-averse market maker")}{eq("fill", "Execution intensity of a quote at distance δ")}</div></div>
    </div>
  </section>
  <section>
    <h2>Ongoing work</h2>
    <ul class="entries">
      {entry("Real estate pricing under transition risk: a real option approach", None, "With Jean-François Chassagneux.", ("climate",))}
      {entry("A major–minor MFG with common jumps and impulse control for optimal cybersecurity investment", None, "With Caroline Hillairet.", ("cyber",))}
    </ul>
  </section>
  <section class="prose">
    <h2>Applied projects</h2>
    <ul class="plain">
      <li><strong>Trading algorithms on stocks and cryptocurrencies.</strong> Statistical-arbitrage strategies implemented in Python and deployed through the Interactive Brokers and Binance APIs.</li>
      <li><strong>Deep and reinforcement learning for option pricing and hedging.</strong> Estimating Black–Scholes option values and hedging strategies with modern learning methods.</li>
      <li><strong>Economic conditions and stock-market performance.</strong> Regression analyses linking the S&amp;P 500 to inflation, unemployment and interest rates.</li>
      <li><strong>Machine learning on DAX and EURO STOXX futures.</strong> Statistical inference and learning-based trading strategies.</li>
    </ul>
  </section>
</main>
""", math=True)

    write("publications.html", "Publications", page_head("Publications", 'Preprints, journal articles and thesis. See also <a href=https://scholar.google.com/citations?user=rdoDR00AAAAJ&hl=en">Google Scholar</a>.') + f"""<main id="main" class="wrap">
  {filters(PREPRINTS, JOURNAL, THESIS, OTHER)}
  <section><h2>Preprints</h2><ul class="entries">{"".join(PREPRINTS)}</ul></section>
  <section><h2>Journal articles</h2><ul class="entries">{"".join(JOURNAL)}</ul></section>
  <section><h2>Thesis</h2><ul class="entries">{"".join(THESIS)}</ul></section>
  <section><h2>Other writing</h2><ul class="entries">{"".join(OTHER)}</ul></section>
</main>
""")

    talks = "".join(f'<section><h2>{y}</h2><ul class="entries">{"".join(items)}</ul></section>' for y, items in TALKS.items())
    write("talks.html", "Talks", page_head("Talks", "Conference presentations and invited seminars. Slides are linked where available.")
          + f'<main id="main" class="wrap">{filters(*TALKS.values())}{talks}</main>\n')

    write("teaching.html", "Teaching", page_head("Teaching", "Courses I have taught as a teaching assistant.") + f"""<main id="main" class="wrap">
  <section>
    <h2>ENSAE Paris</h2>
    <ul class="entries">
      {entry("Financial mathematics", None, 'First-year master’s students, <a href="https://www.ensae.fr/">ENSAE Paris</a>.', (), extra='<p style="margin:.6rem 0 0">Introduction to financial derivatives, valuation in financial markets, pricing by trees, stochastic calculus and the Black–Scholes model.</p>')}
    </ul>
  </section>
</main>
""")

    def edu(when, t, title, where, more=""):
        return (f'<li class="t-{t}"><span class="when">{when}</span><div class="body"><span class="entry-title">{title}</span>'
                f'<span class="meta">{where}</span>{more}</div></li>')

    write("cv.html", "CV", page_head("CV", "Education and training. The full résumé is available as a PDF.") + f"""<main id="main" class="wrap">
  <a class="cv-download" href="files/CV_Lionel_Sopgoui.pdf">Download CV (PDF)</a>
  <section>
    <h2>Education</h2>
    <ul class="edu">
      {edu("Sep 2021 – Nov 2024", "cyber", "PhD in Mathematical Finance", '<a href="https://u-paris.fr/">Université Paris Cité</a> and Imperial College London · Paris, France', '<p style="margin:.5rem 0 0">Thesis: <em>Pricing and hedging of transition risk in credit portfolio</em>. Advisors: Jean-François Chassagneux, Antoine (Jack) Jacquier and Smail Ibbou.</p>')}
      {edu("Sep 2019 – Dec 2020", "climate", "MSc in Financial Mathematics: Statistics and Finance", '<a href="http://www.master-statistique-finance.com/IP_Paris/">École Polytechnique and ENSAE Paris</a> · Palaiseau, France', '<p style="margin:.5rem 0 0">Thesis: <em>Machine learning for finance</em>.</p>')}
      {edu("Sep 2017 – Dec 2020", "micro", "Engineering degree in statistical modelling and applications", '<a href="https://www.telecom-sudparis.eu/">Télécom SudParis</a> · Évry, France', '<p style="margin:.5rem 0 0">Thesis: <em>Machine learning for finance</em>.</p>')}
      {edu("Sep 2012 – Jul 2015", "none", "BSc in Mathematics and Computer Science", '<a href="https://polytechnique.cm/">National Advanced School of Engineering</a> · Yaoundé, Cameroon')}
    </ul>
  </section>
</main>
""")


if __name__ == "__main__":
    build()
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print("Built", len(PAGES) + 1, "pages")
