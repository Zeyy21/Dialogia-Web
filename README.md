# DIALOGIA Montréal 2026

A single-page conference website in French and English. The default language is French; `?lang=en` opens English. No external scripts, fonts, analytics, or application framework are required.

## Official content

The website follows the revised French and English booklets dated **10 October 2026**, the **“-2” editions supplied on 10 October 2026**. `source/fr.json` and `source/en.json` are imported directly from their respective official DOCX files. Each language preserves its document's titles, scientific rationale, programme overview, detailed schedule, 25 presentation abstracts, discussion and workshop participants, scientific committee and organising institutions. Repeated print-only labels are omitted; the attendance statement appears in the international section, and participating institutions appear in the carousel.

The second revision adds Jaume Flaquer Garcia — Loyola University / PLURIEL immediately before Raphaël Georgy in Session 1 and the Axis 1 abstracts. Both programmes use “Preaching in the Age of Artificial Intelligence: Challenges and Implications”, as supplied; his French abstract uses “La prédication à l’épreuve de l’intelligence artificielle”. The full French abstract and all four English paragraphs are included. The official cover counts remain unchanged in the supplied booklets.

Each language downloads its unchanged official Word booklet: `dist/documents/DIALOGIA-2026-FR.docx` or `dist/documents/DIALOGIA-2026-EN.docx`. `source/booklets.json` records the original filenames, public paths and SHA-256 hashes. Download URLs include a content version. Programme buttons open the matching language's on-page overview. Earlier PDFs remain in the repository as historical files and are not linked; PDF conversion products are internal QA artifacts only.

The four organising institution logos remain linked inside the menu bar. The carousel has 28 distinct institution and research-centre cards, including CPRMV, Chaire Raoul-Dandurand, IÉR, CIRRES, TRENDS Global and Université Laval. Centre Thucydide appears once despite being pictured twice in the booklet. Vechta is absent, and KPH uses the booklet's Wien/Niederösterreich name. The organiser-requested TRENDS Group name and logo remain first; TRENDS Global has its own linked card. The cover's stated total of 24 institutions is preserved as supplied.

`source/conference-info.json` contains the final cover's attendance statement (28 academics, 24 institutions, 10 countries) and the earlier organiser-supplied context: represented countries, the research initiative and launches, online participation, required registration and the 70-person venue capacity. `source/institutions.json` records bilingual institution names, countries, official websites and logo provenance. Logos retain their original artwork and colours; SVG viewports isolate UQAM, AUB and USJ from their official composite artwork without altering it. Université Laval's SVG is taken from its official website.

TRENDS Global uses its official high-resolution artwork with an SVG viewport excluding empty margins. IÉR uses the original square artwork from the GEDCIQ presentation (page 2). Chaire Raoul-Dandurand uses the organiser-supplied `CRD_fr_cmyk.png` unchanged. These three logos fill their existing logo areas while retaining their native proportions.

The carousel supports touch scrolling, previous/next buttons, and the arrow, Home and End keys when its list is focused. It has no automatic movement and respects reduced-motion preferences. The programme overview appears before the three daily schedules; the cross-cutting discussion has its own expand/collapse control. The footer reads “Designed by Zeyyad Saleh, Cofounder of Syllogos” and links to Syllogos.

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
- `source/fr.json` and `source/en.json`: passages imported from each official language edition.
- `source/booklets.json`: original booklet filenames, public paths and SHA-256 hashes.
- `source/institutions.json`: represented institutions and the sources of their logo assets.
- `source/conference-info.json`: additional organiser-supplied event information and its French translation.
- `scripts/import_booklets.py`: imports both DOCX sources and copies the unchanged originals into `dist/documents`.
- `scripts/render.py`: renders the page from source paragraphs.
- `scripts/verify.py`: checks both DOCX hashes, exact source fidelity, substantive content coverage, 25 abstracts per language, matching timings and authors, language-specific downloads, programme anchors and local assets; requires lxml.

To replace the official booklets, run:

```sh
python3 scripts/import_booklets.py --fr /path/to/revised-fr.docx --en /path/to/revised-en.docx
python3 scripts/render.py
python3 scripts/verify.py
```

Serve `dist` with a local HTTP server to preview it. Static hosting serves the same directory. For changes that do not replace the booklets, run the renderer and verifier only.

## Source inconsistencies

Each website language preserves its own official document. The following differences require an organiser decision before changing the source wording:

- **Workshop 1:** both titles specify **14 texts and videos**, but the independent evaluation refers to **9**. The French and English objectives also differ.
- **Workshop 3:** the two editions have different titles, objectives and activity descriptions. At **13 h 45**, French describes oversight and ethical principles, while English describes knowledge architecture. At **14 h 30**, French lists a roadmap; English labels governance and responsible development but retains a French description about knowledge organisation and user experience. At **15 h 30**, French lists ethical governance and English lists a general debrief.
- **19 October, Session 3:** the overview covers **14 h 00–15 h 45**, while the detailed session heading ends at **15 h 15**, followed by discussion until **15 h 45**.
- **20 October:** the introductory format paragraph places workshops in the afternoon, although Workshop 1 begins at **11 h 30** in both editions.
- **21 October:** the overview groups special activities, debrief and closing under **15 h 30–17 h 30**; the detailed programme places special activities at **17 h 00** and official closing at **17 h 30**.

These source differences are documented rather than reconciled during import. Verification checks shared times and authors while retaining language-specific wording.
