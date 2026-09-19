"""
AETHER Landing Builder
Builds a pixel-to-pixel static clone of the cofounder.co homepage with AETHER branding.
Pipeline: fetch SSR HTML -> download CSS -> strip scripts -> inline CSS (absolute font URLs)
-> absolutize asset URLs -> apply AETHER text map -> remap internal links -> verify.
Re-runnable: python tools/build_landing.py
"""

import re
import sys
import urllib.request

RAW_URL = "https://cofounder.co/"
OUT = "backend/static/cloned_cofounder.html"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}

ASSET_PREFIXES = ("_next", "logos", "hero", "homepage", "footer", "decor",
                  "books-covers", "build-ui-bits", "favicon", "apple-icon",
                  "icon.png", "logo-dark.svg", "logo-light.svg")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main() -> int:
    html = fetch(RAW_URL).decode("utf-8", errors="ignore")
    print(f"fetched {len(html)} bytes")

    # 1. Collect stylesheet URLs then remove ALL script tags and script preloads.
    css_urls = re.findall(r'<link rel="stylesheet" href="([^"]+)"', html)
    html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<script\b[^>]*/>", "", html)
    html = re.sub(r'<link rel="preload"[^>]*as="script"[^>]*>', "", html)
    html = re.sub(r'<link rel="preconnect"[^>]*>', "", html)
    print(f"stripped scripts, found {len(css_urls)} stylesheets")

    # 2. Download + inline CSS, rewriting relative url() refs to absolute.
    inlined = []
    for u in css_urls:
        css = fetch("https://cofounder.co" + u).decode("utf-8", errors="ignore")
        css = css.replace("url(/", "url(https://cofounder.co/")
        css = css.replace('url("/', 'url("https://cofounder.co/')
        css = css.replace("url('/", "url('https://cofounder.co/")
        inlined.append(f"<style>/* inlined: {u} */\n{css}\n</style>")
        print(f"inlined {len(css)} bytes of CSS from {u}")
    if css_urls:
        first_link = re.escape(css_urls[0])
        html = re.sub(rf'<link rel="stylesheet" href="{first_link}"[^>]*/>', "__CSS_0__", html, count=1)
        for i, u in enumerate(css_urls[1:], start=1):
            html = re.sub(rf'<link rel="stylesheet" href="{re.escape(u)}"[^>]*/>', f"__CSS_{i}__", html, count=1)
        for i, block in enumerate(inlined):
            html = html.replace(f"__CSS_{i}__", block)

    # 3. Absolutize internal asset URLs (src, href, srcSet, poster).
    def absolutize(m):
        attr, path = m.group(1), m.group(2)
        clean = path.lstrip("/")
        if clean.split("?")[0].startswith(ASSET_PREFIXES) or clean.startswith(("icon", "apple")):
            return f'{attr}="https://cofounder.co/{path.lstrip("/")}"'
        return m.group(0)

    html = re.sub(r'(srcSet|src|poster|href)="(/[^"]+)"', absolutize, html)
    html = html.replace('srcSet=\\"/', 'srcSet=\\"https://cofounder.co/')
    html = html.replace('url(\\"/decor/', 'url(\\"https://cofounder.co/decor/')
    html = html.replace('src=\\"/books-covers/', 'src=\\"https://cofounder.co/books-covers/')

    # 4. Header wordmark image -> AETHER text wordmark.
    html = re.sub(
        r'<img src="https://cofounder\.co/logo-dark\.svg"[^>]*alt="Cofounder"[^>]*/>',
        '<span style="font-family:var(--font-neoris),Georgia,serif;font-size:17px;'
        'font-weight:600;color:#262323;letter-spacing:-0.01em;line-height:1">AETHER</span>',
        html,
    )

    # 5. AETHER copy map (ordered: specific strings before generic brand swap).
    replacements = [
        ("Cofounder lets you run an entire company with AI",
         "AETHER gives your platform perfect knowledge of every builder"),
        ("Start with an AI roadmap, then hand off engineering, sales, marketing, design, finance, and ops to agents.",
         "Start with your raw user database. Hand off verification, synthesis, matchmaking, and opportunity dispatch to the context layer."),
        ("Cofounder is an agent orchestration platform designed to help you run an entire business",
         "AETHER is a cognitive context layer designed to give platforms perfect knowledge of their people"),
        ("Give Cofounder the product you built. It turns that context",
         "Give AETHER the platform you built. It turns raw users into living context"),
        ("Keep building the product. Put Cofounder to work on the company.",
         "Keep building the product. Put AETHER to work on the people."),
        ("Learn how to start a company", "Learn how context becomes intelligence"),
        ("All the tools and systems your company needs", "All the intelligence your community needs"),
        ("Run an entire company with AI agents", "Run an entire community on living context"),
        ("Cofounder launches a company with you", "AETHER verifies any builder in seconds"),
        ("Cofounder finds the right customers and gives them a reason to care",
         "AETHER assembles the optimal team with mathematical rigor"),
        ("Cofounder keeps the business moving after launch", "AETHER keeps opportunity flowing after the match"),
        ("Build across industries", "Grounded across every stack"),
        ("You stay in control, nothing ships without your approval",
         "You stay in command. Nothing ships without your verification."),
        ("Run multiple tasks in the background at the same time.",
         "Every query is audited. Every profile carries provenance."),
        ("Customize agents with apps, skills, and schedules",
         "Extend AETHER with webhooks, bots, and live web sensors"),
        ("Enrich contacts", "Enrich profiles"),
        ("Research contacts", "Research builders"),
        ("Send Outreach Emails", "Dispatch invitations"),
        ("Chapter 1 How To Start", "Chapter I How To Ground"),
        ("Chapter 2 How To Build", "Chapter II How To Synthesize"),
        ("Chapter 3 How To Sell", "Chapter III How To Match"),
        ("Chapter 4 How To Scale", "Chapter IV How To Dispatch"),
        ("How to start", "How to ground"),
        ("How to build", "How to synthesize"),
        ("How to sell", "How to match"),
        ("How to scale", "How to dispatch"),
        ("1.1 Business positioning", "1.1 Existence verification"),
        ("1.2 Brand identity", "1.2 Behavioral synthesis"),
        ("1.3 Marketing website", "1.3 Reliability index"),
        ("1.4 Launch content", "1.4 Live web grounding"),
        ("2.1 Customer research", "2.1 Graph topology"),
        ("2.2 Prospect discovery", "2.2 Complementarity engine"),
        ("2.3 Email outreach", "2.3 Squad assembly"),
        ("2.4 Marketing and Newsletters", "2.4 Synergy analysis"),
        ("3.1 LLC incorporation", "3.1 Opportunity scanning"),
        ("3.2 Product analytics", "3.2 Talent invitations"),
        ("3.3 Customer support", "3.3 Webhook ingestion"),
        ("3.4 Recurring workflows", "3.4 Audit trail"),
        ("Start in Cofounder", "Enter Command Center"),
        ("Check out the launch", "Explore Context Layer"),
        ("Run a company", "Enter Command Center"),
        ("LearnPath", "Context Layer"),
        ("Valence OS", "Matchmaker"),
        (">Start</a>", ">Context</a>"),
        (">Build</a>", ">Matchmaking</a>"),
        (">Sell</a>", ">Dispatch</a>"),
        (">Scale</a>", ">Field Guide</a>"),
        (">Pricing</a>", ">Command Center</a>"),
        ("Cofounder", "AETHER"),
        ("COFOUNDER", "AETHER"),
    ]
    for old, new in replacements:
        if old in html:
            html = html.replace(old, new)
    print("applied copy map")

    # 6. Remap remaining internal page links to the command center (assets excluded).
    def remap(m):
        path = m.group(1).lstrip("/")
        if path.split("?")[0].startswith(ASSET_PREFIXES) or path.startswith(("icon", "apple")):
            return m.group(0)
        return 'href="/command"'

    html = re.sub(r'href="(/[^"]*)"', remap, html)

    # 7. Title + meta.
    html = re.sub(r"<title>.*?</title>",
                  "<title>AETHER - Universal Context Layer &amp; Graph Matchmaker</title>", html, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*"',
                  '<meta name="description" content="AETHER is a universal cognitive context layer and autonomous graph matchmaker.">', html)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {OUT}: {len(html)} bytes")

    # 8. Verification gates.
    leftover = len(re.findall(r"Cofounder", html))
    scripts = len(re.findall(r"<script", html))
    aether = len(re.findall(r"AETHER", html))
    styles = len(re.findall(r"<style", html))
    print(f"VERIFY: leftover_cofounder={leftover} scripts={scripts} aether_mentions={aether} style_blocks={styles}")
    if leftover > 0 or scripts > 0 or len(css_urls) == 0:
        print("FAIL: verification gates tripped")
        return 1
    print("OK: landing build verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
