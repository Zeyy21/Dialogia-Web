# DIALOGIA Montréal 2026

A single-page conference website in French and English. The default language is French; `?lang=en` opens English. No external scripts, fonts, analytics, or application framework are required.

## Official content

The source paragraphs in `source/en.json` and `source/fr.json` are verified against the supplied official PDF booklets dated 26 September 2026. The page uses their wording verbatim and includes all substantive content: the scientific rationale, programme overview and detailed schedule, all 23 presentation abstracts in each language, workshop participants, scientific committee and organising institutions. Only the printed contents line, colour legend and a repeated heading are omitted.

The programme buttons open the appropriate PDF at page 3. Every booklet download is an unchanged copy of the supplied PDF. The four organising institution logos are linked inside the menu bar. The represented institutions carousel includes all 22 entries in the organiser's supplied list, counting UQAM and IEIM separately. Each card links to its official website.

Booklet copy remains verbatim in both languages. `source/conference-info.json` contains the additional English information supplied by the organiser, with a French translation: ten represented countries, the research initiative and launches, online participation, required registration and the 70-person venue capacity. `source/institutions.json` records bilingual institution names, countries, official websites and logo provenance. Logos retain their original artwork and colours; SVG viewports isolate UQAM, AUB and USJ from their official composite artwork without altering it.

The carousel supports touch scrolling, previous/next buttons, and the arrow, Home and End keys when its list is focused. It has no automatic movement and respects reduced-motion preferences. The footer includes the requested credit linked to Syllogos.

On phones and tablets, the compact header opens a menu with section links, organising logos and registration. Escape closes the menu and returns focus to its button. The timetable becomes labelled cards on narrow screens. Interface arrows use inline SVGs, so their appearance does not depend on device fonts.

## Registration

The bilingual Google Form is owned by `zeyyad.saleh2006@gmail.com` and is published for anyone with its link. Name, email address and attendance dates are required; affiliation is optional. Email format is validated. Google sign-in is not required, and response summaries are not shared with respondents.

[Manage the form and responses](https://docs.google.com/forms/u/1/d/1y7If-oMbaF6c-z9WNsssG_ZBPVAwJpOMRSgEnrtEdKQ/edit)

Set the verified respondent URL in `registration.json`, then run `python3 scripts/render.py`. Every registration button uses that URL. Until a working form is connected, the page clearly states that its registration link is unavailable.

## Deploy to Vercel

Import `Zeyy21/Dialogia-Web` into Vercel and leave the Root Directory at the repository root (`.`). The included `vercel.json` selects the **Other** framework preset, skips installation and building, and serves the committed `dist` directory. No environment variables are required.

The site, language switch, registration form link, images and booklet downloads are served as committed. After editing source content, CSS or JavaScript, regenerate `dist/index.html` locally and commit it before deploying. The renderer adds content versions to the CSS and JavaScript URLs so returning visitors receive the new files.

Configuration follows [Vercel’s static-site build guidance](https://vercel.com/docs/builds/configure-a-build#skip-build-step).

## Editing and validation

- `dist/index.html`: generated bilingual page.
- `dist/styles.css`: responsive layout and visual design.
- `dist/app.js`: mobile menu, language switching, programme navigation and the accessible institution carousel.
- `source/institutions.json`: represented institutions and the sources of their logo assets.
- `source/conference-info.json`: additional organiser-supplied event information and its French translation.
- `scripts/render.py`: renders the page from source paragraphs.
- `scripts/verify.py`: compares every sourced passage with the official text, checks complete substantive coverage, verifies the source text against both PDFs, and checks links and assets; requires lxml and pypdf.

Serve `dist` with a local HTTP server to preview it. Static hosting serves the same directory. `python3 scripts/render.py` regenerates the page; `python3 scripts/verify.py` checks it.

## Programme discrepancies requiring an organiser decision

The website preserves each document's detailed programme. It does not reconcile the following differences:

- **20 October, Workshop 1:** English detailed programme starts at **11 h 45**; French detailed programme starts at **11 h 30**. Both programme summaries start it at **11 h 15**.
- **20 October, coffee break:** English detailed programme gives **11 h 30 – 11 h 45**; French detailed programme gives **11 h 00 – 11 h 15**, overlapping the stated Session 4 time. Both summaries give **11 h 00–11 h 15**.
- **19 October, Session 3:** the summary includes **14 h 00–15 h 45**, while the detailed session heading ends at **15 h 15**, followed by general discussion until **15 h 45**.
- The introductory format paragraph describes workshops on the afternoon of 20 October; the detailed Workshop 1 starts before noon in both documents.

Resolve these in revised official documents before changing the published wording. The PDF downloads preserve the supplied originals.
