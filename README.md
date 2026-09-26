# DIALOGIA Montréal 2026

A single-page conference website in French and English. The default language is French; `?lang=en` opens English. No external scripts, fonts, analytics, or application framework are required.

## Official content

The source paragraphs in `source/en.json` and `source/fr.json` were extracted directly from the supplied official DOCX files. The page uses those paragraphs verbatim and includes the complete detailed programme. Abstracts remain available in the original downloadable booklets. The organiser image is the original image embedded in the booklet.

Only navigation, accessibility, download and registration labels were written for the website. The language switch selects the respective official source; it does not machine-translate conference copy.

## Registration

The bilingual Google Form is owned by `zeyyad.saleh2006@gmail.com` and is published for anyone with its link. Name, email address and attendance dates are required; affiliation is optional. Email format is validated. Google sign-in is not required, and response summaries are not shared with respondents.

[Manage the form and responses](https://docs.google.com/forms/u/1/d/1y7If-oMbaF6c-z9WNsssG_ZBPVAwJpOMRSgEnrtEdKQ/edit)

Set the verified respondent URL in `registration.json`, then run `python3 scripts/render.py`. Every registration button uses that URL. Until a working form is connected, the page clearly states that its registration link is unavailable.

## Editing and validation

- `dist/index.html`: generated bilingual page.
- `dist/styles.css`: responsive layout and visual design.
- `dist/app.js`: language switching and programme navigation.
- `scripts/render.py`: renders the page from source paragraphs.
- `scripts/verify.py`: compares every sourced passage with the official text and checks programme completeness, links and assets; requires lxml.

Serve `dist` with a local HTTP server to preview it. Static hosting serves the same directory. `python3 scripts/render.py` regenerates the page; `python3 scripts/verify.py` checks it.

## Programme discrepancies requiring an organiser decision

The website preserves each document's detailed programme. It does not reconcile the following differences:

- **20 October, Workshop 1:** English detailed programme starts at **11 h 45**; French detailed programme starts at **11 h 30**. Both programme summaries start it at **11 h 15**.
- **20 October, coffee break:** English detailed programme gives **11 h 30 – 11 h 45**; French detailed programme gives **11 h 00 – 11 h 15**, overlapping the stated Session 4 time. Both summaries give **11 h 00–11 h 15**.
- **19 October, Session 3:** the summary includes **14 h 00–15 h 45**, while the detailed session heading ends at **15 h 15**, followed by general discussion until **15 h 45**.
- The introductory format paragraph describes workshops on the afternoon of 20 October; the detailed Workshop 1 starts before noon in both documents.

Resolve these in revised official documents before changing the published wording. Original DOCX downloads are unchanged.
