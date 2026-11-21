#!/usr/bin/env python3
"""Build Bloomfield at Home into public/. Run: python3 build.py"""
import html
import json
import shutil
from datetime import date
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).parent
OUT = ROOT / "public"
SITE = yaml.safe_load((ROOT / "data/site.yaml").read_text())
PRODUCTS = {p["id"]: p for p in yaml.safe_load((ROOT / "data/products.yaml").read_text())}
CATS = {c["slug"]: c for c in SITE["categories"]}
YEAR = date.today().year
e = html.escape

CSS = """
:root{--ink:#24323b;--muted:#5b6770;--teal:#2f6f73;--teal-d:#245659;--cream:#faf6ef;--sand:#efe6d8;--line:#e2d9cb;--accent:#b5653b}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:Georgia,'Times New Roman',serif;color:var(--ink);background:var(--cream);font-size:18px;line-height:1.65}
a{color:var(--teal-d)}a:focus-visible,button:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.wrap{max-width:760px;margin:0 auto;padding:0 18px}
header.site{background:#fff;border-bottom:1px solid var(--line)}
header.site .wrap{display:flex;align-items:center;justify-content:space-between;min-height:64px;gap:12px}
.logo{font-weight:700;font-size:1.2rem;text-decoration:none;color:var(--ink);letter-spacing:.2px}
.logo span{color:var(--teal)}
nav.top a{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;font-size:.95rem;text-decoration:none;margin-left:14px}
.hero{padding:34px 0 18px}
h1{font-size:1.85rem;line-height:1.25;margin:.2em 0 .4em}
h2{font-size:1.35rem;margin:1.6em 0 .5em}
.lead{font-size:1.1rem;color:var(--muted)}
.cards{display:grid;grid-template-columns:1fr;gap:14px;margin:18px 0 30px}
.card{display:block;background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 18px;text-decoration:none;color:var(--ink)}
.card h3{margin:0 0 4px;font-size:1.1rem;color:var(--teal-d)}
.card p{margin:0;color:var(--muted);font-size:.98rem}
.meta{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;font-size:.85rem;color:var(--muted)}
.notice{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--sand);border-left:4px solid var(--accent);padding:10px 14px;border-radius:6px;font-size:.92rem;margin:16px 0}
article{background:#fff;border:1px solid var(--line);border-radius:12px;padding:6px 20px 22px;margin:18px 0 30px}
article ul,article ol{padding-left:1.2em}
.provider{border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:12px 0;background:var(--cream)}
.provider h3{margin:0 0 4px;font-size:1.05rem}
.btn{display:inline-block;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--teal);color:#fff;text-decoration:none;padding:10px 16px;border-radius:8px;margin-top:8px;font-size:.95rem;min-height:44px}
.btn:hover{background:var(--teal-d)}
.crumbs{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;font-size:.85rem;margin-top:18px}
footer.site{border-top:1px solid var(--line);background:#fff;margin-top:40px;padding:22px 0 30px;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;font-size:.88rem;color:var(--muted)}
footer.site a{margin-right:14px}
.indep{font-weight:600;color:var(--ink)}
@media(min-width:700px){h1{font-size:2.3rem}.cards{grid-template-columns:1fr 1fr}}
"""

INDEPENDENT = ("Bloomfield at Home is an independent guide site. It is not a care provider, "
               "gives general information only, and is not part of Bloomfield Care's regulated care service.")


def page(title, description, body, path, extra_head=""):
    canonical = SITE["url"] + path
    nav = "".join(f'<a href="/{c["slug"]}/">{e(c["title"].split(" - ")[0].split(",")[0])}</a>'
                  for c in SITE["categories"][:0])
    return f"""<!DOCTYPE html>
<html lang="en-GB"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}"><meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE['name'])}">
<meta name="p:domain_verify" content="ed5b08fff46b6a262476f5f0b8973de2"/>
<link rel="stylesheet" href="/style.css">{extra_head}
</head><body>
<header class="site"><div class="wrap"><a class="logo" href="/">Bloomfield <span>at Home</span></a>
<nav class="top"><a href="/guides/">Guides</a><a href="/about/">About</a></nav></div></header>
<main class="wrap">{body}</main>
<footer class="site"><div class="wrap">
<p class="indep">{INDEPENDENT}</p>
<p>Some pages contain affiliate links: if you buy through them we may earn a commission, at no extra cost to you. It never changes what we recommend. <a href="/affiliate-disclosure/">How we make money</a></p>
<p><a href="/about/">About</a><a href="/affiliate-disclosure/">Affiliate disclosure</a><a href="/privacy/">Privacy</a><a href="mailto:{SITE['email']}">Contact</a></p>
<p>&copy; {YEAR} Bloomfield at Home</p></div></footer>
</body></html>"""


def write(path, content):
    target = OUT / path.strip("/") / "index.html" if not path.endswith(".html") else OUT / path.strip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def provider_card(p):
    if p.get("affiliate_url"):
        link = (f'<a class="btn" href="{e(p["affiliate_url"])}" rel="sponsored nofollow noopener" '
                f'target="_blank">Visit {e(p["name"].split(" (")[0])} (affiliate link)</a>')
    else:
        link = (f'<a class="btn" href="{e(p["official_url"])}" rel="nofollow noopener" '
                f'target="_blank">Visit {e(p["name"].split(" (")[0])}</a>')
    return f'<div class="provider"><h3>{e(p["name"])}</h3><p>{e(p["blurb"])}</p>{link}</div>'


def load_guides():
    guides = []
    for f in sorted((ROOT / "content/guides").glob("*.md")):
        raw = f.read_text()
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm)
        meta["slug"] = f.stem
        meta["html"] = markdown.markdown(body, extensions=["extra", "sane_lists"])
        guides.append(meta)
    return guides


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "style.css").write_text(CSS)
    guides = load_guides()
    live = [g for g in guides if g.get("status", "published") == "published"]
    redirects = ["https://bloomfieldathome.co.uk/* https://bloomfieldathome.com/:splat 301!",
                 "https://www.bloomfieldathome.co.uk/* https://bloomfieldathome.com/:splat 301!",
                 "https://www.bloomfieldathome.com/* https://bloomfieldathome.com/:splat 301!"]
    urls = ["/", "/guides/", "/about/", "/affiliate-disclosure/", "/privacy/"]

    # Guides
    for g in guides:
        if g.get("status") == "archived":
            redirects.append(f"/guides/{g['slug']}/ /{g['category']}/ 301")
            continue
        cat = CATS[g["category"]]
        prods = [PRODUCTS[pid] for pid in g.get("products") or [] if pid in PRODUCTS]
        has_aff = any(p.get("affiliate_url") for p in prods)
        notice = ('<div class="notice"><strong>Ad / affiliate links:</strong> this page contains affiliate links. '
                  'If you buy through them we may earn a commission at no extra cost to you. '
                  '<a href="/affiliate-disclosure/">Find out more</a>.</div>') if has_aff else ""
        provs = ""
        if prods:
            provs = "<h2>Providers to compare</h2><p>Listed in no particular order. Always compare with the free and local options above.</p>" + "".join(provider_card(p) for p in prods)
        schema = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"],
                  "description": g["description"], "dateModified": str(g["updated"]),
                  "publisher": {"@type": "Organization", "name": SITE["name"]},
                  "mainEntityOfPage": f"{SITE['url']}/guides/{g['slug']}/"}
        body = (f'<p class="crumbs"><a href="/">Home</a> &rsaquo; <a href="/{cat["slug"]}/">{e(cat["title"])}</a></p>'
                f'{notice}<article><h1>{e(g["title"])}</h1>'
                f'<p class="meta">Updated {g["updated"].strftime("%-d %B %Y")} &middot; General information, not professional advice</p>'
                f'{g["html"]}{provs}</article>')
        head = f'<script type="application/ld+json">{json.dumps(schema)}</script>'
        write(f"/guides/{g['slug']}/", page(f"{g['title']} | {SITE['name']}", g["description"], body,
                                           f"/guides/{g['slug']}/", head))
        urls.append(f"/guides/{g['slug']}/")

    def guide_cards(items):
        return '<div class="cards">' + "".join(
            f'<a class="card" href="/guides/{g["slug"]}/"><h3>{e(g["title"])}</h3><p>{e(g["description"])}</p></a>'
            for g in items) + "</div>"

    # Categories
    for c in SITE["categories"]:
        items = [g for g in live if g["category"] == c["slug"]]
        prods = [p for p in PRODUCTS.values() if p["category"] == c["slug"]]
        has_aff = any(p.get("affiliate_url") for p in prods)
        notice = ('<div class="notice"><strong>Ad / affiliate links:</strong> some links on this page are affiliate links. '
                  '<a href="/affiliate-disclosure/">Find out more</a>.</div>') if has_aff else ""
        provs = ("<h2>Providers</h2>" + "".join(provider_card(p) for p in prods)) if prods else ""
        body = (f'<section class="hero"><h1>{e(c["title"])}</h1><p class="lead">{e(c["intro"])}</p></section>'
                f'{notice}<h2>Guides</h2>{guide_cards(items)}{provs}')
        write(f"/{c['slug']}/", page(f"{c['title']} | {SITE['name']}", c["intro"], body, f"/{c['slug']}/"))
        urls.append(f"/{c['slug']}/")

    # Home
    cat_cards = '<div class="cards">' + "".join(
        f'<a class="card" href="/{c["slug"]}/"><h3>{e(c["title"])}</h3><p>{e(c["intro"])}</p></a>'
        for c in SITE["categories"]) + "</div>"
    latest = sorted(live, key=lambda g: g["updated"], reverse=True)[:6]
    home = (f'<section class="hero"><h1>{e(SITE["tagline"])}</h1>'
            '<p class="lead">Plain-English guides for older people and the families helping them: staying safe, '
            'getting around, planning ahead and keeping bills down. We always show the free and official options first.</p></section>'
            f'<h2>Browse by topic</h2>{cat_cards}<h2>Latest guides</h2>{guide_cards(latest)}')
    write("/", page(f"{SITE['name']} - {SITE['tagline']}",
                    "Plain-English guides to personal alarms, mobility aids, stairlifts, wills, LPAs and household bills for older people and their families.",
                    home, "/"))

    write("/guides/", page(f"All guides | {SITE['name']}", "Every Bloomfield at Home guide in one place.",
                           f'<section class="hero"><h1>All guides</h1></section>{guide_cards(live)}', "/guides/"))

    about = """<section class="hero"><h1>About Bloomfield at Home</h1></section><article>
<p>Bloomfield at Home is an independent guide site run by Russell Bloomfield. It brings together plain-English information about the practical side of later life at home: alarms and home safety, mobility equipment, wills and Lasting Powers of Attorney, everyday aids and household bills.</p>
<h2>What we are not</h2>
<p>We are not a care provider and we do not give medical, legal or financial advice. Bloomfield at Home is separate from Bloomfield Care, a home care provider. Bloomfield Care's care staff do not recommend or sell products to the people they support.</p>
<p>If you are looking for home care or live-in care, you can find Bloomfield Care at <a href="https://bloomfield-care.com/">bloomfield-care.com</a>.</p>
<h2>How we choose what to include</h2>
<ul><li>We show free and official routes first, such as council assessments and gov.uk services.</li>
<li>We only list established UK providers with clear terms.</li>
<li>We do not cover insurance, funeral plans, pensions, equity release, loans or health supplements.</li>
<li>Some links earn us a commission. They are always labelled. See <a href="/affiliate-disclosure/">how we make money</a>.</li></ul>
<h2>Spotted a mistake?</h2>
<p>Rules and prices change. If something looks out of date, email <a href="mailto:hello@bloomfieldathome.co.uk">hello@bloomfieldathome.co.uk</a> and we will check it.</p></article>"""
    write("/about/", page(f"About | {SITE['name']}", "Who runs Bloomfield at Home and how we choose what to include.", about, "/about/"))

    disclosure = """<section class="hero"><h1>How we make money</h1></section><article>
<p>Bloomfield at Home is free to read. To pay for it, some of the links on this site are affiliate or referral links. If you click one and then buy something or sign up, the company may pay us a commission. You never pay more because you used our link.</p>
<ul><li>Affiliate links are marked "(affiliate link)", and pages that contain them show an "Ad / affiliate links" notice at the top.</li>
<li>Whether a company pays us does not decide whether it appears or where it is listed.</li>
<li>We always mention free and official alternatives where they exist.</li>
<li>As an Amazon Associate we earn from qualifying purchases.</li></ul>
<p>Questions? Email <a href="mailto:hello@bloomfieldathome.co.uk">hello@bloomfieldathome.co.uk</a>.</p></article>"""
    write("/affiliate-disclosure/", page(f"Affiliate disclosure | {SITE['name']}", "How Bloomfield at Home makes money and how affiliate links are labelled.", disclosure, "/affiliate-disclosure/"))

    privacy = """<section class="hero"><h1>Privacy</h1></section><article>
<p>This site does not ask you to create an account and does not use advertising or tracking cookies.</p>
<p>When you click an affiliate link, the company you visit may set its own cookies to record that you came from us. Their own privacy policy applies on their site.</p>
<p>If you email us, we use your email only to reply and do not share it.</p>
<p>Site run by Russell Bloomfield. Contact: <a href="mailto:hello@bloomfieldathome.co.uk">hello@bloomfieldathome.co.uk</a>.</p></article>"""
    write("/privacy/", page(f"Privacy | {SITE['name']}", "Privacy information for Bloomfield at Home.", privacy, "/privacy/"))

    (OUT / "404.html").write_text(page(f"Page not found | {SITE['name']}", "Page not found.",
                                       '<section class="hero"><h1>Sorry, we can\'t find that page</h1><p><a href="/guides/">See all guides</a></p></section>', "/404.html"))
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"<url><loc>{SITE['url']}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "_redirects").write_text("\n".join(redirects) + "\n")
    print(f"Built {len(live)} guides, {len(SITE['categories'])} categories, {len(urls)} URLs")


if __name__ == "__main__":
    build()
