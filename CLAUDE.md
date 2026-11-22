# Bloomfield at Home — project rules

Owner: Russell Bloomfield, personally (NOT Bloomfield Care Ltd). Domain bloomfieldathome.com (primary, chosen 21 Nov 2026) and .co.uk (redirects to .com), registered to Russell personally at Namecheap, DNS on Cloudflare. GitHub BloomfieldatHome/bloomfield-at-home, hosting on Cloudflare Pages (project bloomfield-at-home, connected to the BloomfieldatHome GitHub; deploys on every push to main). The old Netlify site has auto publishing off and is kept only as a fallback.

## What this site is
An independent guide site for older people and families helping someone live well at home: home safety and alarms, stairlifts and mobility, wills and LPAs, everyday aids and wellbeing, and household bills/utilities. It earns from clearly labelled affiliate and referral links.

## Non-negotiables
1. **Not a care provider.** Every page carries the footer line saying the site is independent, not a care provider and not part of Bloomfield Care's regulated service. Never imply CQC registration, care expertise of the site, or that Bloomfield Care staff recommend these products.
2. **Disclosure.** Any page with an affiliate link shows the "Ad / affiliate links" notice at the bottom of the page content (Russell's decision, 22 Nov 2026, after being told UK ad rules expect upfront disclosure) (and Amazon's "As an Amazon Associate..." line where Amazon links appear). Buttons are NOT individually labelled "(affiliate link)" (Russell's decision, 22 Nov 2026). Links use rel="sponsored nofollow noopener".
3. **No regulated financial promotions.** No life insurance, over-50s plans, funeral plans, pensions, equity release, loans or investments. Wills and LPAs are fine.
4. **No medicines, supplements or health claims.** Pharmacy and foot-care retailers (e.g. Express Chemist, Algeos) are allowed, but only link to NON-medicine products: daily living aids, incontinence, mobility/bathroom aids, home monitors (BP monitors, thermometers), footwear, insoles, foot-care tools. Never link to prescription medicines (illegal to advertise to the public), over-the-counter medicines or supplements. Product copy is factual (what it is, who it suits) - never 'relieves', 'treats', 'cures' or similar. Always point to the GP, pharmacist, NHS podiatrist, OT or physio where relevant. (Agreed with Russell 21 Nov 2026.)
5. **Always show the free/official route** alongside any paid option (council OT assessment, gov.uk LPA, council lifeline alarms, Priority Services Register, etc.).
6. **Facts that change** (fees, grant limits, prices, programme rates) are checked before publishing and dated, or left out.
7. **Human approval.** New articles and Pinterest pins are drafted, then published only after Russell approves the weekly batch.
8. Archive, never delete published articles (set `status: archived` in front matter; the build keeps a 301 to the category page).
9. Mobile-first: design and check at 375px first.
10. British English, plain language, no jargon, no emojis, no "gesture of goodwill".

11. **Never name Russell (or any person) as the owner on public pages.** Contact is hello@ only. (Russell, 21 Nov 2026.)

## How the site is built
- `content/guides/*.md` — articles with YAML front matter (title, description, category, updated, status).
- `data/site.yaml` — categories and site settings. `data/products.yaml` — product/provider cards; `affiliate_url` empty means show the plain official link with no affiliate label.
- `python3 build.py` renders everything into `public/` (committed). Cloudflare Pages serves `public/` with no build step (output directory `public`).
- Always run `python3 build.py` and commit `public/` with content changes.

## Repository is PUBLIC (since 21 Nov 2026)
Made public so Netlify's free plan accepts pushes from the BloomfieldCare GitHub login. Never commit secrets, API keys, affiliate account IDs beyond what appears in public links, commission rates, earnings, or anything about Bloomfield Care clients or staff.

## Pinterest pins (style agreed by Russell, 21 Nov 2026)
- Bloomfield palette: navy #1D2B3A, maroon #7C2D37, cream #FAF7F2, soft pink #E8C4C8, sand #F1E8E3. Site uses the same palette.
- Pins are 1000x1500: navy header band (category kicker + "FREE PLAIN-ENGLISH GUIDE"), serif headline, short subline, maroon rule, a simple flat illustration in a sand rounded panel, navy footer "bloomfieldathome.com".
- Illustrations are simple flat shapes drawn in code (no photos, no AI images, no Bloomfield Care client photos). Generator: tools/pins/make.py (text layout from pins.json) then tools/pins/illus.py (one drawing function per pin; add new ones as needed). Run from a scratch copy of tools/pins.
- Posting: approved pin images go in pins/ (copied to public/pins/) AND get an entry in data/pins.yaml (img, guide slug, title, desc, date). The build writes https://bloomfieldathome.com/pins.xml, which Pinterest auto-publish reads and posts from. Only add approved pins. Never remove entries (they're the posting history).
