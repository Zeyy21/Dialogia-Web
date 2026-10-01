# DIALOGIA Montréal 2026

A single-page conference website in French and English. The default language is French; `?lang=en` opens English. No external scripts, fonts, analytics, or application framework are required.

## Official content

The website follows the final French print booklet supplied on 1 October 2026, `DIALOGIA_Montreal_2026_Livret_FR_FINAL_IMPRESSION.pdf` (16 pages). `source/fr.json` preserves its scientific rationale, programme overview, detailed schedule, all 24 presentation abstracts, discussion and workshop participants, scientific committee and organising institutions. The repeated cover, printed contents line, colour legend and repeated heading are not duplicated on the page. The cover's attendance statement appears in the international section, and the participating institutions appear in the existing carousel.

`source/en.json` retains the previously supplied English text where it still agrees with the final French edition, with translations of the additions and corrections. No final English PDF was supplied. Both language versions link to the unchanged final French PDF, with French labels on English download links. Programme buttons open its overview on page 4. PDF URLs include a content version so returning visitors receive the final edition. The earlier English PDF remains in the repository for reference and is no longer linked from the website.

The four organising institution logos remain linked inside the menu bar. The carousel has 27 distinct institution and research-centre cards from the final booklet's visual roster, including logos embedded as images: Chaire Raoul-Dandurand, IÉR, CIRRES, TRENDS Global and Université Laval. Centre Thucydide appears once despite being pictured twice in the booklet. Vechta, absent from the final booklet, has been removed, and KPH now uses the booklet's Wien/Niederösterreich name. The organiser-requested TRENDS Group name and logo remain first; TRENDS Global has its own linked card. The cover's stated total of 24 institutions is preserved as supplied.

`source/conference-info.json` contains the final cover's attendance statement (28 academics, 24 institutions, 10 countries) and the earlier organiser-supplied context: represented countries, the research initiative and launches, online participation, required registration and the 70-person venue capacity. `source/institutions.json` records bilingual institution names, countries, official websites and logo provenance. Logos retain their original artwork and colours; SVG viewports isolate UQAM, AUB and USJ from their official composite artwork without altering it. Université Laval's SVG is taken from its official website.

TRENDS Global uses its official high-resolution artwork with an SVG viewport excluding empty margins. IÉR uses the original square artwork from the GEDCIQ presentation (page 2). Chaire Raoul-Dandurand uses the organiser-supplied `CRD_fr_cmyk.png` unchanged. These three logos fill their existing logo areas while retaining their native proportions.

The final update adds Gilles Bibeau's opening address, Lyse Langlois's title and full abstract, the cross-session discussion participants and discussants, and Sultan Al Hosani in the workshop roster. It also applies the final schedule, Wasim Salman spelling, Wael Saleh affiliation and abstract corrections.

The carousel supports touch scrolling, previous/next buttons, and the arrow, Home and End keys when its list is focused. It has no automatic movement and respects reduced-motion preferences. The programme overview appears before the three daily schedules. The footer reads “Designed by Zeyyad Saleh, Cofounder of Syllogos” and links to Syllogos.

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
- `scripts/verify.py`: checks every displayed source passage, complete French PDF coverage, 24 abstracts in each language, matching bilingual timings and authors, final booklet links, and local assets; requires lxml and pypdf.

Serve `dist` with a local HTTP server to preview it. Static hosting serves the same directory. `python3 scripts/render.py` regenerates the page; `python3 scripts/verify.py` checks it.

## Programme discrepancies requiring an organiser decision

The website preserves the final French document's wording and timing in both languages:

- **20 October:** the final booklet resolves the previous timing differences. Session 4 is **9 h 00–11 h 15**, including discussion at **11 h 00–11 h 15**; coffee is **11 h 15–11 h 30**; Workshop 1 starts at **11 h 30**.
- **19 October, Session 3:** the summary includes **14 h 00–15 h 45**, while the detailed session heading ends at **15 h 15**, followed by general discussion until **15 h 45**.
- The introductory format paragraph describes workshops on the afternoon of 20 October; the detailed Workshop 1 starts before noon in both documents.

The remaining differences are preserved from the final booklet; they have not been silently reconciled. The French PDF download is an unchanged copy of the supplied final document.
