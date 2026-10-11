# DIALOGIA Montréal 2026

A single-page conference website in French and English. The default language is French; `?lang=en` opens English. No external scripts, fonts, analytics, or application framework are required.

## Official content

The website text was imported from the revised French and English DOCX booklets dated **10 October 2026** (the **“-2” editions**), then updated with the organiser’s corrections supplied on **11 October 2026**. `source/fr.json` and `source/en.json` contain the current website text. `source/programme-corrections.json` records the authorised replacements so verification can still check the rest of each source against its original DOCX. Each language preserves its document's titles, scientific rationale, programme overview, detailed schedule, 25 presentation abstracts, discussion and workshop participants, scientific committee and organising institutions. Repeated print-only labels are omitted; the attendance statement appears in the international section, and participating institutions appear in the carousel.

The second revision adds Jaume Flaquer Garcia — Loyola University / PLURIEL immediately before Raphaël Georgy in Session 1 and the Axis 1 abstracts. Both programmes use “Preaching in the Age of Artificial Intelligence: Challenges and Implications”, as supplied; his French abstract uses “La prédication à l’épreuve de l’intelligence artificielle”. The full French abstract and all four English paragraphs are included. The official cover counts remain unchanged in the supplied booklets.

Each language downloads its unchanged final PDF booklet supplied on **11 October 2026**: `dist/documents/DIALOGIA-2026-FR.pdf` or `dist/documents/DIALOGIA-2026-EN.pdf`. `source/booklets.json` records the original PDF filenames, public paths and SHA-256 hashes; its `text_source` entries retain the DOCX provenance used to verify the website text. Download URLs include a content version. Programme buttons open the matching language’s on-page overview. Earlier DOCX files remain in the repository for source verification and are not linked.

The four organising institution logos remain linked inside the menu bar. The carousel has 29 distinct institution and research-centre cards, including CPRMV, Chaire Raoul-Dandurand, IÉR, CIRRES, TRENDS Global, Université Laval and Loyola University (Spain). Loyola uses the organiser-supplied JPEG unchanged and links to its official website. Centre Thucydide appears once despite being pictured twice in the booklet. Vechta is absent, and KPH uses the booklet's Wien/Niederösterreich name. The organiser-requested TRENDS Group name and logo remain first; TRENDS Global has its own linked card. The cover's stated total of 24 institutions is preserved as supplied.

`source/conference-info.json` contains the final cover's attendance statement (28 academics, 24 institutions, 10 countries) and the earlier organiser-supplied context: represented countries, the research initiative and launches, online participation, required registration and the 70-person venue capacity. `source/institutions.json` records bilingual institution names, countries, official websites and logo provenance. Logos retain their original artwork and colours; SVG viewports isolate UQAM, AUB and USJ from their official composite artwork without altering it. Université Laval's SVG is taken from its official website.

TRENDS Global uses its official high-resolution artwork with an SVG viewport excluding empty margins. IÉR uses the original square artwork from the GEDCIQ presentation (page 2). Chaire Raoul-Dandurand uses the organiser-supplied `CRD_fr_cmyk.png` unchanged. These three logos fill their existing logo areas while retaining their native proportions.

The carousel supports touch scrolling, previous/next buttons, and the arrow, Home and End keys when its list is focused. It has no automatic movement and respects reduced-motion preferences. The programme overview appears before the three daily schedules; the cross-cutting discussion has its own expand/collapse control. The footer reads “Designed by Zeyyad Saleh, Cofounder of Syllogos” and links to Syllogos.

The **Speakers & participants / Intervenants et participants** gallery appears immediately before the international institutions section. Its navy background, large colour portraits, serif names and unboxed captions distinguish people from institution logo cards. It reuses the carousel's touch, button and keyboard controls, with no automatic movement. The compact navigation includes a link to the gallery. Portraits remain scrollable without JavaScript, and all profiles appear in print.

`source/speakers.json` records 30 distinct portrait/name pairs extracted from the organiser-supplied `Montreal_2026_Speakers_11-10-2026.docx`, in first-appearance order. Repeated appearances merge roles and affiliations into one profile. It includes French and English captions, the source document hash, embedded media paths and hashes, source paragraph references, and public portrait hashes. The embedded portraits are resized to 550 pixels wide and compressed as WebP, retaining their colour and proportions (about 1 MB in total), and loaded lazily. The document's cover states 32 named contributors, but only 30 distinct portrait/name pairs are present; no missing people are inferred and the official booklet's programme and attendance totals are unchanged.

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
- `source/booklets.json`: final PDF filenames, public paths and SHA-256 hashes, plus retained DOCX text-source provenance.
- `source/programme-corrections.json`: organiser-authorised website text replacements dated 11 October 2026.
- `source/institutions.json`: represented institutions and the sources of their logo assets.
- `source/speakers.json`: portrait/name matches, bilingual affiliations and roles, and source provenance.
- `dist/assets/speakers/`: optimised portraits extracted from the supplied speaker document.
- `source/conference-info.json`: additional organiser-supplied event information and its French translation.
- `scripts/import_booklets.py`: replaces PDF downloads without changing the curated website text, or imports DOCX sources and copies unchanged originals into `dist/documents`.
- `scripts/render.py`: renders the page from source paragraphs.
- `scripts/verify.py`: checks PDF and DOCX hashes, exact source fidelity with the recorded organiser corrections, substantive content coverage, 25 abstracts per language, matching timings and authors, language-specific PDF downloads, programme anchors, all 30 speaker profiles and portrait hashes, and local assets; requires lxml.

To replace the official booklets, run:

```sh
python3 scripts/import_booklets.py --fr /path/to/final-fr.pdf --en /path/to/final-en.pdf
python3 scripts/render.py
python3 scripts/verify.py
```

Serve `dist` with a local HTTP server to preview it. Static hosting serves the same directory. For changes that do not replace the booklets, run the renderer and verifier only. PDF replacement preserves the language JSONs and their text-source provenance. A future DOCX import requires reviewing and updating the recorded programme corrections before validation.

## Source inconsistencies

Each website language preserves its own official document. The following differences require an organiser decision before changing the source wording:

- **Workshop 1:** the organiser’s 11 October correction changes both titles from **14** to **9 texts and videos**. The three facilitators remain Zeyyad Saleh, Wael Saleh and Eissa Ali AlMannaei. The French and English objectives still differ.
- **Workshop 3:** the organiser’s 11 October correction replaces the **14 h 30** and **15 h 30** entries in each language. The final PDFs confirm distinct governance descriptions: English covers knowledge organisation and user experience; French covers ethical governance and responsible development. The French PDF’s governance paragraph is printed in English; the website translates it into French. Both website languages include the expanded final synthesis and roadmap at **15 h 30**, after the **15 h 15** coffee break. Earlier workshop titles, objectives and the **13 h 45** descriptions retain their language-specific wording.
- **19 October, Session 3:** the overview covers **14 h 00–15 h 45**, while the detailed session heading ends at **15 h 15**, followed by discussion until **15 h 45**.
- **20 October:** the introductory format paragraph places workshops in the afternoon, although Workshop 1 begins at **11 h 30** in both editions.
- **21 October:** the overview groups special activities, debrief and closing under **15 h 30–17 h 30**; the detailed programme places special activities at **17 h 00** and official closing at **17 h 30**.

Remaining source differences are documented rather than reconciled during import. Verification checks shared times and authors while retaining language-specific wording and the explicitly recorded organiser corrections.
