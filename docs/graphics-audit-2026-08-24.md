# Graphics Audit, Built for Wonder, 2026-08-24

Scope: every visual layer of the book as built from Built-for-Wonder.docx through extract_manuscript.py, build-book.py and build-gated.py: the 12 FIGURES images, the author photo, the generated SVG and HTML graphics (MARKER_BLOCKS, gen_* functions, *_HTML constants), the 611 margin icons, the DOCX-embedded media, and the deployed gated file on aowbook.netlify.app. Five independent finders (text-references, generator-coverage, assets-and-docx, rendered-pages, html-structure) each produced findings; a verifier re-checked every finding against the repo and marked it confirmed, refuted or added-by-verifier. 117 raw findings were merged into the unique issues below. The raw merged data, with every finder's evidence and the verifier's reason, is in docs/graphics-audit-findings-2026-08-24.json. No repo file was modified by the audit; all scratch output lives under the session scratchpad gfx/ folder.

Line references are to build-book.py, extract_manuscript.py, build-gated.py, manuscript-extracted.txt (ms) and Built-for-Wonder-DESIGNED.html (HTML) as of commit 386c61d.

## 1. Verdict

Not production ready. Everything that is wired up renders correctly and identically in DESIGNED, GATED, NoBrookings and the live site, but Chapter 24 (REFLEX) ships without its five DOCX-embedded images, Chapter 17 ships without the 71-row Cold Reading Toolkit, Chapter 23 ships two empty headers where the sitcom reference grids belong, and two graphics the prose promises (the Diagnostic questions and the Performance Decision Matrix) have never been written.

Unique issues after merging: 7 blockers, 16 major, 22 minor, plus about a dozen informational items (rights, inventory, parity). Two finder claims were refuted outright and roughly fifteen more were corrected in detail (section 6).

Needs new material from Chris: the real training-video URL (the QR embedded in the DOCX points at a deactivated QR.io redirect), five to eight diagnostic questions for Chapter 22, the rows of the Performance Decision Matrix for Chapter 31, nine chapter hook lines, and provenance answers for two images. Everything else, including four of the seven blockers and fourteen of the sixteen majors, is a change to build-book.py, extract_manuscript.py or build-gated.py using assets that already exist in the DOCX or in resources/.

## 2. Blockers

Definition used: the text promises a visual that is missing, a graphic is broken, or a marker leaks or silently vanishes from a page that depends on it.

### B1. Chapter 24 QR code is missing, the password renders as a header, and the QR itself is dead

Location: ms 2727 ("To help you learn: I have included a QR code to a live training...") and ms 2729 ("Password: BuiltForWonder"); HTML 5081-5082 (GATED 5236); DOCX word/media/image5.png (1638x2048 "SCAN ME" QR, rId57, anchored in DOCX paragraph 2931); build-book.py FIGURES (234-309) has no Ch24 QR entry; is_section_header (~800) accepts the two-word Title Case password line.

Evidence: HTML renders the promise paragraph and then `<h3 class="section-header sh-standard">Password: BuiltForWonder</h3>` with zero `<img>` between HTML 5081 and 5195. Build stdout has no image warning because FIGURES only fires on section headers and the QR is not in FIGURES; extract_manuscript.py reads only w:t runs so every w:drawing is dropped. The verifier decoded the QR with macOS Vision (scratchpad gfx/qr.swift): payload https://qr.link/uXLKtz. One verifier saw HTTP 200; another fetched the body and it is a QR.io page reading "Deactivated QR Code. The QR code owner needs to choose a plan to reactivate this QR code." Both are consistent: the redirect serves a 200 with a deactivation notice. Shipping image5.png as-is would print a dead code.

Fix: (1) Chris supplies the real video URL, or reactivates the QR.io plan; a static QR generated locally (python qrcode or segno, 1000px or more) removes the recurring dependency. (2) Save it as resources/metv-images/reflex-training-qr.png. (3) In build-book.py add a paragraph-anchored injection (FIGURES cannot do this; it keys on headers): when the stripped line starts with "To help you learn:" emit the paragraph, then a book-figure with the QR at about 240px, and render the following "Password:" line as the figure caption instead of an h3 (add it to a non-header exclusion). (4) Optionally emit the human-readable URL beneath the QR, or use the existing dead gen_video_embed (1358) with a VIDEO EMBED marker so web readers can click. Needs artwork: yes, a regenerated QR, but it is mechanical once the URL exists.

### B2. Chapter 24 "previous image" (two fists) is missing

Location: ms 2778 ("Have a look at the previous image and find which hand the object is in. Do not continue reading until you have done this. Go look now.") and ms 2780 ("When viewing the image that is the hand you see on the left side"); DOCX word/media/image3.png (1024x1024, two fists side by side, no watermark, rId58) in the empty paragraph directly after ms 2773 ("On the empty hand, the thumb will often rest over the knuckle...") and before ms 2775 ("The secondary tell is hand height."); HTML 5113-5127 has no `<img>`.

Evidence: only 15 `<img>` tags exist in the whole DESIGNED file and none is a hand; md5 of image3.png matches nothing in resources/. Three finders and the verifier agree on the DOCX anchor (the assets-and-docx finder's original mapping put it in the chapter intro; corrected by the verifier).

Fix: extract image3.png to resources/metv-images/reflex-two-fists.png and inject it after the ms 2773 paragraph using the same paragraph-anchored mechanism as B1, with a Figure 24.x caption naming the three tells (thumb placement, hand height, knuckle stepping). Build-only; the asset exists.

### B3. Chapter 24 "Both images above" (the two Variations fists) are missing

Location: ms 2786 ("Both images above are displaying variations of the concealing hand. In one, the index finger is stepped out independently. In the other, both the first and second fingers are stepped out."); DOCX word/media/image4.png (896x1099, rId59) and image2.png (896x1196, rId60), both inline at the end of the paragraph that ends "The confirmation is the knuckle profile." (ms 2785), i.e. immediately before ms 2786; HTML 5127-5129 (h3 Variations, one paragraph, then the orphaned sentence).

Evidence: no `<img>` within 3000 characters either side; images viewed in the scratchpad: single fists with different knuckle profiles. image2.png carries a Gemini four-point-star watermark in its bottom-right corner (see M16).

Fix: extract both to resources/metv-images/reflex-variation-index.png and reflex-variation-two-fingers.png (crop the watermark off image2 first), inject them as a two-up book-figure (flex row, each max-width 48%) after the ms 2785 paragraph so they are literally above the sentence, caption "Figure 24.x, Variations of the concealing hand: index finger stepped (left); first and second fingers stepped (right)." Build-only; assets exist. Rights: AI-generated illustration.

### B4. Chapter 17 Cold Reading Toolkit (71 rows in six Word tables) never reaches the book

Location: ms 1866-1882 describe the toolkit ("This section is the operational layer...", "How to use this toolkit in real time: observe the cue, identify the radar category, match the DISC tendency, select the line, deliver it"); in the DOCX, six w:tbl elements with columns Cue | Line | Type (16+13+10+10+9+13 = 71 data rows) sit between the "Observe. Classify. Translate. Test. Adjust." paragraph and "Cold Reading in Practice"; extract_manuscript.py line 85 iterates doc.paragraphs only, so w:tbl content is skipped; build-book.py already has the full rendering system for exactly this content (TOOLKIT_SECTION:/CRT:/TOOLKIT_NAV/CR_SUMMARY_TABLE handlers at 3352-3396, gen_crt_table 2145, gen_cr_toolkit_entry 2063, gen_toolkit_nav 1956, gen_cr_summary_table 1977) and all of it is dead.

Evidence: first cues of the six tables ("Wears well-tailored, immaculate clothing", "Straight back, purposeful stride", "Stays on the edges of the room", "Initiates conversation warmly", "Pauses carefully before speaking", "Slow, deep breath under visible stress") map to the six radar categories in order; each string has 0 hits in manuscript-extracted.txt and 0 in DESIGNED.html. HTML goes from the KEY PRINCIPLE aside straight to `<h3>Cold Reading in Practice</h3>`. Class counts crt-table 0, toolkit-nav 0. docs/10-editing-session-log.md lines 146-150 (2026-03-17) show these renderers were once live, so this is a regression. Full table dump: scratchpad gfx/docx-tables.txt.

Fix: in extract_manuscript.py walk the document body children in order (paragraph or w:tbl; previous-versions/abandoned-book-v2-pipeline-20260503/book_v2.py line 1484 already does this with qn('w:tbl')) and for each Cue | Line | Type table emit "TOOLKIT_SECTION:<radar category>" followed by one "CRT: <cue> | <type> | <context>" plus line paragraph per row, then TOOLKIT_NAV / CR_SUMMARY_TABLE, so the existing build-book.py handlers fire. Build-only; no content needed from Chris.

### B5. Chapter 23 sitcom era-by-vowel grids are dropped, leaving two empty headers

Location: ms 2631-2636 (script for multiple-word sitcom titles), headers MULTIPLE-WORD TITLES (ms 2633) and ONE-WORD TITLES (ms 2635); DOCX tables 8 and 9, each 4 rows x 6 columns (ERA / VOWEL by A E I O U: Happy Days, I Love Lucy, Golden Girls, Family Matters, Fresh Prince of Bel-Air, Full House, Big Bang Theory, Modern Family; Bewitched/Cheers, Seinfeld, Roseanne, Friends, Office). The text-references finder filed this under Ch22; the HTML header sits under id chapter-23 (PROPLESS SYSTEMS THAT ACTUALLY WORK, ms 2600), so it is Chapter 23.

Evidence: HTML has `<h3 class="section-header sh-standard">MULTIPLE-WORD TITLES</h3>` immediately followed by `<h3 class="section-header sh-standard">ONE-WORD TITLES</h3>`; "Happy Days" and "Fresh Prince" have 0 hits in the manuscript, "Golden Girls" only in the prose at ms 2625.

Fix: same extractor change as B4 (emit table rows as marker lines, e.g. "GRID: ERA / VOWEL | A | E | I | O | U") plus a small gen_vowel_grid() in build-book.py that renders a 4x6 table styled like zet3. Build-only; content exists in the DOCX.

### B6. Chapter 22 THE DIAGNOSTIC promises questions that were never written

Location: ms 2586-2589 (CLOSING TOOL / THE DIAGNOSTIC / "Run these questions against every propless routine. When a question reveals a gap, the gap tells you which section to return to." / marker CH18_DIAGNOSTIC_PANEL); build-book.py 3579-3593 unresolved-marker guard drops the token; placeholders/03_CH18_DIAGNOSTIC_PANEL.md status: "Diagnostic questions need to be written/confirmed by Chris."

Evidence: build stdout "[warn] skipped unresolved marker token: CH18_DIAGNOSTIC_PANEL"; HTML 4944-4947 renders the instruction and then the closing paragraphs with no list.

Fix: Chris writes five to eight diagnostic questions (one per section of the chapter: premise, freedom versus restriction, covert acquisition, natural language, endgame, silence). Then either paste them into the DOCX as a numbered list under THE DIAGNOSTIC, or keep the marker and add CH18_DIAGNOSTIC_PANEL to MARKER_BLOCKS (644) styled like the Ch29 checklist cards (cl-item/cl-box). Until then reword ms 2586 so it does not promise questions. Needs content from Chris.

### B7. Chapter 31 Performance Decision Matrix does not exist

Location: ms 3966-3971 (header, "This matrix maps environment type to demonstration approach to volunteer strategy. Every row represents a different neurological contract...", marker PERFORMANCE_MATRIX at 3968, then Chris Michael's Take "I played a 400-person gala using the matrix row for intimate strolling... Wrong row, wrong show."); build-book.py mentions the token only in the guard comment at 3583; no placeholders/ spec; HTML 6421-6423.

Evidence: build stdout "[warn] skipped unresolved marker token: PERFORMANCE_MATRIX"; HTML has the h3, two paragraphs and the performer-note header with nothing between; class "matrix" 0 hits; previous-versions/.../apply_audit_fixes.py line 992 carries "TODO[CONTENT GAP]: The matrix table itself is missing here". No row content exists anywhere in the repo.

Fix: Chris supplies the rows (environment type by demonstration approach by volunteer strategy; at minimum stage/keynote, corporate strolling, private dinner or close-up table, parlor, virtual). Then add PERFORMANCE_MATRIX_HTML to MARKER_BLOCKS like ZODIAC_ELEMENT_TABLE_HTML (610) with break-inside:avoid. The build side is trivial; the content is the blocker. Until then rewrite the two matrix sentences. Needs content from Chris.

Blocker summary: B2, B3, B4, B5 are build-only with assets in hand. B1 needs a URL from Chris and a regenerated QR. B6 and B7 need writing from Chris.

## 3. Major issues

### M1. Chapter 24 chin-tell photo is dropped and "The chin tell." is a plain paragraph

Location: ms 2818 ("The chin tell.") and 2819-2820 ("Draw a line from where their chin is pointed. It will aim toward the empty hand."); DOCX word/media/image6.png (896x1196, seated man with both fists forward and head turned off-axis, rId61) in the empty paragraph directly after ms 2818; HTML 5160-5169 has no `<img>`; FORCED_HEADERS has no entry for "The chin tell." or "The posture reset."

Evidence: `<p>The chin tell.</p><p>By the third phase...` in the HTML. The html-structure finder placed the image after "This is where the deepest signals emerge"; the verifier corrected the anchor to directly after "The chin tell." The image carries the Gemini watermark (M16), so it is AI-generated, not a stock portrait.

Fix: extract image6.png to resources/metv-images/reflex-chin-tell.png (crop the watermark), inject after "The chin tell." with a Figure 24.x caption, and add "The chin tell." and "The posture reset." to FORCED_HEADERS so the two tells read as sub-headers. Build-only. Rights: AI-generated illustration.

### M2. The brain-wave chart is embedded twice in Chapter 19 as Figure 19.3 and Figure 19.4

Location: FIGURES "CHAPTER 19:The Alpha Shift" (247-252) and "CHAPTER 19:Oscillations and Timing" (253-258) both src resources/metv-images/hypnosis-brain-wave-states.png (1959x1134); HTML 4379 and 4417 carry byte-identical payloads (sha a6b33e8cc612, 138,101 bytes, 184,158 chars of base64 each).

Evidence: the 19.3 alt says "alpha highlighted" but the image is identical to the plain chart; the 19.4 caption lists "beta, alpha, theta, delta" while the image has five rows including Gamma; the Oscillations section is about theta-band timing, which an alpha-highlighted chart does not illustrate. docs/10-editing-session-log.md line 188 records that the chart was deliberately re-anchored at Oscillations and Timing and the fractionation figure dropped, so the Alpha Shift entry is the stale leftover. Finders disagreed on which one to keep; the docs settle it.

Fix: delete the "CHAPTER 19:The Alpha Shift" entry (247-252), renumber the surviving caption 19.4 to 19.3, and fix its wording to name the five states shown. Build-only. Saves 179 KB of base64.

### M3. ABOUT THE AUTHOR renders three times, once as an empty photo-only page, with a stray "1"

Location: ms 65 (front matter) and ms 4661 plus 4662 (two consecutive identical lines); build-book.py 993 opens a new about section on every such line; emitter at 6403-6406 writes running header, h3 and author photo per section; HTML 2415-2419, 7190-7194 (article with header, h3, photo and no body), 7195+ (photo again plus bio). ms 67 is a bare "1" (a DOCX page number) that renders as `<p>1</p>` at HTML 2419 under the front-matter bio; ms 103 is a bare "2" rendering at HTML 2460.

Evidence: alt="Chris Michael" appears 3 times (the 327,264-byte JPEG is embedded three times, about 1.3 MB of base64); rendered p718 is a page with only the heading and the photo; parse_manuscript yields three about sections with 2, 0 and 13 paragraphs.

Fix: in the parser skip an ABOUT THE AUTHOR line that immediately follows another (or skip about sections with empty content), and skip paragraphs that are a bare integer (the part-opener branch already does this with isdigit). Also delete the duplicate paragraph and the two page-number paragraphs from the DOCX. Build-only.

### M4. The DOCX title block leaks as ten raw paragraphs ending in "FRONT MATTER"; the designed title page and author-note-front never render

Location: ms 55-64 (BUILT / FOR WONDER / subtitle / CHRIS MICHAEL / tagline / ornament / quote / attribution / FRONT MATTER); HTML 2403-2412 at the tail of the Acknowledgments; build-book.py 6237-6241 (tp_start only fires on a paragraph equal to "DECODE BEHAVIOR", which the acknowledgments never contain; ms 8 is the spaced-letter form "D E C O D E   B E H A V I O R" in the skipped pre-section block); 6260-6279 title-page and author-note-front emitters; CSS .title-page/.tp-* at about 5377.

Evidence: grep for class="title-page" and class="author-note-front" in DESIGNED = 0; rendered p10-p11 show the literal FRONT MATTER label. The generator-coverage finder's note that author-note-front "renders once as designed" is wrong.

Fix: detect the title block by "BUILT" immediately followed by "FOR WONDER" (or normalize spaced-letter lines before comparing), drop the FRONT MATTER chrome line, let the existing title-page and author-note-front sections render, then decide whether the ms 65-66 front-matter About article is still wanted alongside the condensed note that the Meta Reveal (build-book.py 3677) describes. Build-only.

### M5. Chapter 11 Volunteer Selection Matrix cards are half-empty and do not form a grid

Location: ms 1079-1091 (each cell is heading / ALL-CAPS recommendation / description); build-book.py gen_volunteer_matrix_entry 1645, trigger 3010-3016 consumes only paragraphs[i+1]; HTML around chapter-11.

Evidence: every cell renders as `<div class="vm-heading">High Confidence + High Suggestibility</div><div class="vm-rec"></div><p class="vm-body">BEST CHOICE</p>` followed by the description as a bare `<p>` outside the card; vm-rec is empty in all four; no vm-grid wrapper (0 hits), so the four cells stack vertically instead of the 2x2 confidence-by-suggestibility grid the text describes ("Map them separately"). The abandoned v2 build rendered this as matrix2x2.

Fix: when paragraphs[i+1] is ALL CAPS and paragraphs[i+2] is prose, pass rec=paragraphs[i+1], body=paragraphs[i+2] and advance by 3; wrap the four cells in a vm-grid with grid-template-columns 1fr 1fr and axis labels. Build-only.

### M6. Chapter 17 VAK Pacing Framework renders as 26 bare one-line paragraphs

Location: ms 1839-1864 (Visual / Language / see, clear, picture... / Eye movement / upward during recall / ... / Auditory / ... / Kinesthetic); build-book.py gen_modality_card 2663 and trigger 3318-3327 (_modality_triggers wants "Visual Signals", "Auditory Signals", "Kinesthetic Signals"); rendered p263-264.

Evidence: class="modality-card" 0 hits (the one string hit is the CSS rule); a run of 20 short paragraphs then 6 more under the VAK header.

Fix: extend the trigger to a bare Visual / Auditory / Kinesthetic line followed by label/value pairs, collect the pairs until the next modality or prose paragraph, join them into the "Label: value." form gen_modality_card parses (or write a small three-column renderer), and emit the cards. Build-only.

### M7. Chapter 17 Cold-Warm-Hot source rows re-render under the graphic with two stray arrows

Location: ms 1796-1809; build-book.py 3221-3225 appends COLD_WARM_HOT_HTML and then does i += 1 without consuming the COLD / arrow / WARM / arrow / HOT rows; HTML 4094-4103; rendered p257-258.

Evidence: two `<p>` containing only an arrow character at HTML 4097 and 4101; COLD and WARM become section headers while HOT becomes a plain paragraph; the graphic is followed by the same content as prose.

Fix: after appending the graphic advance i past the block, stopping at "The Four Principles of Translation". Build-only.

### M8. Chapter 9 T4 signal cards never render and the text points to a "T4 Appendix" that does not exist

Location: ms 934, 941, 949, 956 ("T4: NLP Eye Movement Direction" etc., each with THE CLAIM / THE RESEARCH / WHAT REMAINS VALID); promises at ms 480 and 525 ("documented in the T4 Appendix"); build-book.py trigger 3252 wants "SIGNAL N" lines (0 in the manuscript) and the gate at 3257 is chapter_num == 8 while the 80-Signal System is Chapter 9; gen_t4_signal_card 2642, gen_t4_table 1250; HTML 3021-3047.

Evidence: 12 generic h3s (THE CLAIM x4, THE RESEARCH x4, WHAT REMAINS VALID x4) with plain paragraphs; class t4-signal-card only in CSS; "T4 Appendix" is referenced twice in the HTML (the second split by a badge span) and no heading containing Appendix exists anywhere, including the TOC. ms 932 lists eight removed signals and only four are documented.

Fix: accept a second regex `^T4:\s*(.+)$`, drop the chapter gate, feed CLAIM / RESEARCH / VALID into gen_t4_signal_card (CSS already present), delete gen_t4_table (its hardcoded rows duplicate the manuscript). DOCX wording: change both "T4 Appendix" references to "documented under T4 Signals Removed at the end of this chapter", and either document the other four listed items or shorten the list at ms 932. Build-only plus a two-line DOCX edit.

### M9. SECTION_BADGES is keyed to the old chapter numbering: 105 of 120 badge strips never fire

Location: build-book.py SECTION_BADGES 334-466, gen_section_badge_strip 468, injection at about 3612 (badge_data = SECTION_BADGES.get(fig_key)).

Evidence: class="section-badge-strip" count 15, all under chapters 37-42 where numbering did not shift. Independently reproduced with scratchpad gfx/refute_keys.py: "CHAPTER 7:The Five Cs" is now in Chapter 8, "CHAPTER 4:The Cortisol Threshold" in Chapter 5, "CHAPTER 18:The Rainville Finding" in Chapter 19, "CHAPTER 27:The Performance Architecture Framework" in Chapter 29 (off by two for Ch27-32 keys); 21 keys name headers that no longer exist anywhere ("CHAPTER 3:1. Novelty", "CHAPTER 16:Visual Signals", "CHAPTER 31:The T1 Opener", "CHAPTER 39:Pillar One: Confidence"). docs/10 line 188 re-anchored FIGURES only. The tier/category strips the Signal Key page tells the reader to expect appear only in Part Five.

Fix: regenerate the keys from the current parser (or key by header text with a chapter-range sanity check), delete the 21 orphan keys, and add a build-time warning listing any SECTION_BADGES or FIGURES key that never matched. The same drift affects WHAT_YOU_JUST_DID (see m10). Build-only.

### M10. The four interlude chapters (7A, 21A, 27A, 37A) are not parsed as chapters

Location: ms 372-378 (7A), 2411-2417 (21A), 3526-3532 (27A), 4422-4434 (37A); the DOCX writes "CHAPTER 7A" plus the title on one line; build-book.py 891 chapter regex matches "CHAPTER n" alone and the bleed stripper at 2919-2921 then deletes the line; HTML 2779-2782, 4769, 5950, 6949; rendered p72, p352, p539, p686.

Evidence: 7A appears as a stray `<p>7A</p>` under two stacked running headers (READING THE ROOM then INTRODUCTION) directly after the Part Two opener; 21A survives as an inline section header with its number; 27A loses its number entirely; 37A gets a small "PART FIVE · INTERLUDE" section header mid-chapter. TOC toc-num list is 1-36, Intro, 37-42 with no A entries. None get openers, hook lines or badges even though the DOCX supplies hook quotes and tier badges for each. CLAUDE.md counts 37A as a chapter.

Fix: add a parser branch for `^CHAPTER (\d+A)\s*[^A-Za-z0-9]+\s*(.+)$` (and the bare "7A" + title + quote form at ms 372-374) that opens a chapter with chapter_num like "7A", add HOOK_LINES and CHAPTER_LEGEND entries for the four, emit them in gen_toc as indented sub-entries with a lighter interlude opener variant, and dedupe the back-to-back running headers at 2779-2780. Build-only. Chris should confirm the interludes are meant to read as chapters.

### M11. Ten chapter openers show an empty hook-line slot

Location: build-book.py HOOK_LINES (51) has no keys for CHAPTER 12, 26, 27, 29, 30, 31, 32, 33, 34; gen_chapter_opener 1129/1151 always emits the hook-line div and its gold rule; the Part Five "Before You Begin" opener (chapter-0) also has an empty hook and an empty part-label.

Evidence: `<div class="hook-line"></div>` count 10 in DESIGNED; KEY_READS has all 42 keys, so this is a content gap not a key drift; rendered p145 (Ch12 CHRIS MICHAEL'S TELL TABLE) shows number, title and badges with a blank between the rules. CLAUDE.md says HOOK_LINES is one per chapter. One verifier graded this minor, one major; it is listed as major because the blank slot is visible on nine production opener pages.

Fix: Chris supplies nine hook lines (or the build pulls the DOCX opener quote where one exists); gen_chapter_opener should omit the hook-line div and its rule when the string is empty; pass "PART FIVE" as the part label for chapter-0. Needs nine lines from Chris; the empty-slot suppression is build-only.

### M12. A 35 percent alpha gold is used as a text color in nine CSS rules

Location: build-book.py 3878 defines --gold-dim as rgba(201,168,76,.35); it is the text color at 4124 .ff-q, 4129 .fsig-name, 4135 .zet-el, 4144 .zet3-el, 4148 .fivec-q strong, 4153-4154 .fivec-chain, 4159 .byline-credit, 5263 .toc-part.

Evidence: rendered hi266 shows the feedback card title "01, Lip Compression" barely legible on cream; p457-458 show the zodiac element labels EARTH / AIR / WATER / FIRE as ghost text; hi89 shows the Five Cs "Context" and "Clusters" labels washed out; the TOC part labels and every routine byline credit share the problem. 21 rendered elements carry these classes.

Fix: add a solid token (for example --gold-text #8F6F2A, or reuse --gold #C9A84C which reads at bold sans sizes) and point all nine rules at it; reserve --gold-dim for rules, ornaments and borders. One edit plus rebuild. Build-only.

### M13. Photo figures have no stylesheet rule and no page-break protection

Location: build-book.py 3608-3611 (inline styles only: text-align center, margin 2em 0, caption font-size .85em color #666); no .book-figure or .figure-caption rule anywhere; print block 3896-3901 lists key-read, spotlight-box, tier-block, concept-box, h3.section-header only; the img has no width/height attributes.

Evidence: every generated graphic container (.six-area-radar, .disc-chart, .recovery-card, .tier-block, .anthem-aria-card, .principle-card, .zet3-block) carries break-inside:avoid; the 12 photo figures do not, so a caption can orphan onto the next page and the 900x1400 name chart can split. A 6x9 PDF is a real deliverable (Built-for-Wonder-DRAFT-2026-08-13.pdf is in the repo). The #666 caption color also bypasses the design tokens.

Fix: add .book-figure {break-inside:avoid; page-break-inside:avoid; margin:2em 0; text-align:center}, .book-figure img {max-width:100%; height:auto; max-height:7.2in}, .figure-caption {break-before:avoid; color:var(--dim); font-family:var(--sans)}, drop the inline styles, and emit width/height from PIL in image_data_uri so the 9 MB page does not shift while decoding. Build-only.

### M14. The gate still shows the old title and "unreleased draft" copy

Location: build-gated.py 157 (`<div class="gate-title">THE ARCHITECTURE<br>OF WONDER</div>`) and 160 ("Read the unreleased draft..."); present once in GATED and in the live capture.

Evidence: CLAUDE.md records the rename to Built for Wonder on 2026-04-08 and states display text everywhere reads Built for Wonder. This is the first screen every reader sees on a production deploy.

Fix: change the gate title to BUILT FOR / WONDER and update the description copy; keep STORAGE_KEY "aow_reader" (178) so returning readers are not re-gated. Rebuild gated and redeploy. Build-only.

### M15. The DOCX and the HTML carry disjoint image sets

Location: Built-for-Wonder.docx word/media holds six files: image1.png (a 70-byte 1x1 transparent placeholder, rId62, used at The Name Chart paragraph 3030 and ABOUT THE AUTHOR paragraph 4779 at 0.69 inch) and image2-6 (the five Ch24 visuals); none of the 12 FIGURES sources (build-book.py 235-307) is in the DOCX; [Content_Types].xml has only a png default, no jpeg or svg.

Evidence: unzip listing plus PIL; CLAUDE.md "Adding figures/photos" step 2 says to embed figures in OOXML so they are visible in Word or Google Docs, and no figure has been. Anyone reviewing the source of truth in Word sees a caption "Figure 24.1" over a blank, no author photo, and no other figures, while the site lacks the five images Word does show.

Fix: decide one direction of truth. Either run an OOXML embed pass for the 12 FIGURES files plus the author photo (add media, relationships, jpeg and svg content types, rasterize the name chart SVG to PNG for Google Docs, replace the rId62 placeholders; back up first), or record in CLAUDE.md that figures are build-only and the DOCX intentionally carries placeholders. In both cases add the five Ch24 images to FIGURES so every image has one registry with rights. Decision needed from Chris; the DOCX pass is not a build change.

### M16. Two of the five Ch24 photos carry a Gemini AI watermark

Location: DOCX word/media/image2.png (the second Variations fist) and image6.png (the chin-tell portrait), bottom-right corner; corner crops in scratchpad gfx/refuter-media/.

Evidence: PIL crops of the bottom-right 200px show the light four-point star on both; image3.png and image4.png are clean and of unknown source.

Fix: crop about 60px off the bottom (or inpaint the corner) before saving to resources/metv-images, and set rights to "AI-generated illustration" on their FIGURES entries to match the Ch13 and Ch25 convention. Build-side asset prep; no new artwork.

Major summary: all sixteen are build changes except M11 (nine hook lines from Chris, suppression is build-only) and M15 (a decision plus a DOCX embed pass).

## 4. Minor and polish

Each is fixable in build-book.py, build-gated.py or the extractor unless noted.

- m1. PERF_ARCH_FRAMEWORK_SVG (ms 3819, after the four Layer paragraphs at 3813-3818) is silently dropped by the guard at 3579-3593; placeholders/02 says "SVG needs to be designed". The prose never promises a diagram ("Four layers. Each one is required before the next"), so two verifiers graded it minor and one major. All four labels exist in the text, so a gen_perf_arch_framework() with four stacked bands (Intelligence, Architecture, Calibration, Execution) in the DISC palette can be generated and registered next to SIX_AREA_RADAR (3422) without new artwork.
- m2. CH18_IFYRE_PANEL (ms 2593) is dropped, leaving a bare "IF YOU REMEMBER NOTHING ELSE" h3 in Chapter 22 directly above the key-read card that every chapter already has. No other chapter carries that header. Either wrap the key line in a panel (reuse gen_rule_callout 1824) or suppress the header when the token follows it. placeholders/04 confirms the panel content was never written.
- m3. Chapter 20 Days of the Week (ms 2143-2149) renders as seven raw paragraphs with a literal pipe ("01 MONDAY | 6 letters"); the step-header branch at about 2417 does not accept the " | detail" suffix. Extend it to emit step-num, step-name and step-meta spans.
- m4. Chapter 21 Force Category Reference Map (ms 2387-2394): three of four headings render as h3 but "Most Dangerous If Used Badly" is a plain paragraph because is_section_header (~834) rejects lines starting with "Most " and it is not in FORCED_HEADERS. Add it, or better collect the four heading/value pairs into a 2x2 card grid.
- m5. Caption numbering: eight figures are numbered (13.1, 14.1, 14.2, 19.1 to 19.4, 24.1) and the four Chapter 25 zodiac captions are not (FIGURES 285-307). Prefix them Figure 25.1 to 25.4, or auto-prefix "Figure chapter.n" in the injector so numbering cannot drift; when the Ch24 photos land, number them in reading order and renumber the name chart.
- m6. reflex-name-chart.svg: viewBox 0 0 900 1400 but the largest y is 1055, so about a quarter of the figure box is empty above the caption (rendered p430); 177 inline font-family "Anthropic Sans" declarations plus var(--font-sans) on the root, but as an `<img>` data URI (build-book.py 3608) no page font or variable reaches it, so it falls back to Helvetica (headless Chrome renders in scratchpad gfx/chart-548.png); at the 548px column the 12px text nodes land at about 7px; the chart text contains seven em dashes. Crop the viewBox to about 900x1060, inline the SVG markup so it inherits Montserrat (or set an explicit stack), raise the smallest sizes, and replace the dashes. The "If wrong" line is not clipped (see section 6).
- m7. gen_six_area_radar emits raw ampersands in "& Posture" and "& Space" (axes list 1409-1414, emitted unescaped at 1500-1503): it is the only one of 613 inline SVGs that fails XML parsing. Browsers tolerate it; an EPUB or XHTML export would not. Wrap the label in html_module.escape (already imported at 22). The same function hard-codes font-family "sans-serif" on all 23 text nodes while the DISC chart uses "Montserrat, sans-serif"; align them.
- m8. External dependencies: the Vanishing Inc reveal logo is hot-linked from i.postimg.cc (build-gated.py 169, no onerror) while a local copy sits unused at resources/w1000-n22219JlqyT2zQoE.jpg (972x398); a curl of the postimg URL stalled at 32 KB of 42 KB after 15 seconds. Embed it as a data URI. Both editions also import Cormorant Garamond and Montserrat from Google Fonts (build-book.py 3866); decide whether the single-file book should be fully offline and, if so, subset and embed the two faces. Confirm Vanishing Inc logo usage rights.
- m9. Stray DOCX page numbers "1" (ms 67) and "2" (ms 103) render as `<p>1</p>` (HTML 2419) and `<p>2</p>` (HTML 2460). Covered by the M3 fix; listed here so it is not lost if M3 is solved DOCX-side only.
- m10. WHAT_YOU_JUST_DID (build-book.py 206-214) is keyed by chapter number and has drifted like SECTION_BADGES: the cortisol callout is injected into Chapter 4 while The Cortisol Threshold is in Chapter 5 (ms 260). The Ch8 case is arguable (the DOCX itself carries that callout in Ch8) and the Ch22 case is not drift (WYAJD_AT_START pins it deliberately). Re-key by chapter_key string like HOOK_LINES and KEY_READS.
- m11. Two short lists render as bare paragraphs: Chapter 34 BEHAVIORS THAT READ AS SAFE AND STRONG (ms 4177-4182, five separate lines, the checklist handler at about 3080 expects one dot-joined line) and the Chapter 14 five-line list at ms 1420. "BEHAVIORAL PROFILING" in checklist_heads has no manuscript trigger and can be dropped. Route consecutive short lines under a caps header through the checklist or book-list branch.
- m12. gen_context_card (2751) and gen_error_card (2758) are dead only because of case drift: the manuscript has STAGE CONTEXT, STROLLING CONTEXT (ms 485, 487) and ACTING ON A SINGLE SIGNAL, IGNORING THE BASELINE, CONFIRMATION BIAS, CULTURAL PROJECTION (ms 491-497) as ALL CAPS, while the triggers at 3164 and 3183 compare Title Case strings with a trailing period. The six blocks render as bare h3s (HTML 2972-2977). Compare case-insensitively and extend the error list to all four observer errors.
- m13. About 24 generators and constants have no trigger anywhere in the manuscript and their CSS ships unused: gen_video_embed, gen_bte_signal, gen_certainty_frame, gen_mnemonic, gen_def_card, gen_colin_cloud_card, gen_toolkit_nav, gen_cr_summary_table, gen_feedback_chart, gen_cr_toolkit_entry, gen_feedback_signals_ref, gen_crt_table, gen_cm_takeaway, gen_forces_intro, gen_glossary_entry, gen_modality_card, gen_reading_line_card, gen_context_card, gen_error_card, gen_rule_callout, gen_five_c_entry, gen_what_you_have_felt, gen_t4_table, gen_t4_signal_card, gen_concept_box, FRUIT_TO_FANG_HTML. Keep the ones the fixes above revive (toolkit family for B4, modality for M6, T4 cards for M8, context and error cards for m12, video embed for B1); FRUIT_TO_FANG_HTML, gen_feedback_chart and gen_feedback_signals_ref are superseded by blocks that fire and can be deleted. Add a build-time report of generators with zero hits so retirements are deliberate.
- m14. Five Cs grid (FIVE_CS_HTML 486-539): the final READ chain pill is white text on 8 percent white over cream and invisible (.chain-read at 5842), the Clusters pill is gold on 10 percent gold and nearly as faint, and two section-break ornaments stack back to back directly under the grid (HTML 2896, the only such case in the book). Give the pills solid backgrounds and collapse consecutive section breaks.
- m15. Back-matter About tail: the three domains (ms 4671-4673) and the ornament render as plain paragraphs (HTML 7206-7209) because the about renderer (6406-6412) wraps every line in `<p>`. Map the ornament to the section-break div and the domains to a small link list.
- m16. Tables without break protection: .tt-band (6 elements), .f2f-table (28 cells), .f2f-flow have no break-inside rule; .zet-table (CSS 4132-4136) is dead CSS with zero elements (the zodiac marker renders zet3, whose blocks are already protected). Add break-inside:avoid to tt-band and f2f-flow, delete the zet-table rule.
- m17. Page weight: 7.6 MB of the 9.0 MB single file is base64 image data and the gate cannot work until all of it downloads. Two photographs are stored as PNG (lip compression 845 KB, seven expressions 796 KB) and the four 1408x768 zodiac JPEGs are 455 to 637 KB each for a 548px column. A PIL re-encode at identical pixel size (JPEG q82 progressive) takes 4,187 KB to 1,327 KB, about 3.8 MB less base64; removing the duplicate brain-wave chart and two of the three author photos saves another 1 MB. Transcode in image_data_uri or pre-convert the files.
- m18. Print resolution: lip-compression-example.png is 843x749 (about 187 dpi in a 4.5 inch column) and seven-universal-expressions.png is a 1424x389 strip, so each face is about 78px wide on screen and the contempt versus disgust difference is hard to read on a phone. Regenerate the lip composite from the 1408x768 Gemini source at 1500px or more and consider a 4+3 layout for the seven faces. Needs re-exported artwork.
- m19. Documentation drift: the CLAUDE.md "After any edit" Step 1 snippet walks every w:p (it would spill the toolkit rows, the sitcom grids and the tier table as about 330 stray lines and collapse the QR paragraph) and is not what produces manuscript-extracted.txt; extract_manuscript.py via build_all.py is. Replace the snippet with the script call and document the marker format once B4 lands. CLAUDE.md "Two editions" lists three Brookings sections but brookings_manifest.py strips four (add preshow-failure). docs/05-production-workflow.md 173-176 and docs/03-editorial-decisions.md 115 list one figure (10.1) while FIGURES has 12 and the chapter is 14; regenerate that table from FIGURES after the rights corrections in section 5.
- m20. Pattern interrupts: four stats are configured (PATTERN_INTERRUPTS 219-233: 250 ms, 40 percent, 7 expressions, 3 signals) but only PATTERN_INTERRUPT_40PCT exists in the manuscript (ms 1312), so one interrupt renders, while the Meta Reveal (build-book.py 3755, ms 4739) says "Every eight to twelve pages, the layout changed." Add the other three markers to the DOCX at natural breaks or soften the Meta Reveal sentence. Chris decides.
- m21. Print-only layout (does not affect the deployed HTML): margin icons float outside the column with negative margins and are cut in half at the right edge on every printed page that has one (rendered hi266, p263); the Five Cs grid overflows the 6x9 text block so the fifth card is clipped (hi89); the radar category cards each land alone on a page; the dark full-bleed sections print inset because of the @page margins at 3891-3897 (the page size is already 6in by 9in, so the rendered-pages finder's suggestion to add a page size is moot). If print is a deliverable, add an @media print block for fci-grid and margin-icon and break-inside rules for the cards; otherwise document that print is unsupported.
- m22. Em dashes: the FIGURES captions and generated card titles use an em dash separator (about 37 build-generated occurrences; the other 348 in the HTML are the author's prose). Chris's standing rule bans them in public-facing copy. If the book is not exempt, switch the build-generated separators to a period or colon in FIGURES and the card title templates. Editorial call for Chris.

## 5. Inventory

### 5a. Image assets the build uses (13 files, all embedded as base64 data URIs; every one exists on disk and renders)

| File (resources/metv-images/) | Pixels | Bytes | Where it appears | Caption | Rights as configured | Notes |
|---|---|---|---|---|---|---|
| lip-compression-example.png | 843x749 | 865,537 | Ch13 Lip Compression (rendered p168) | Figure 13.1 | AI-generated illustration | PNG of a photo; low print resolution (m18) |
| seven-universal-expressions.png | 1424x389 | 815,864 | Ch14 The Seven Expressions (p180) | Figure 14.1 | Author-owned photograph | Provenance unconfirmed: matches a widely circulated third-party composite, no camera EXIF; Chris to confirm before print |
| duchenne-smile-comparison.jpg | 1408x768 | 310,404 | Ch14 The Duchenne Smile (p181) | Figure 14.2 | Author-owned photograph | Rights label is wrong: Gemini native size, EXIF BeFunky, byte-identical to resources/DUCHENNE SMILE.jpg; should read AI-generated illustration |
| hypnosis-brain-networks-shift.png | 1930x1023 | 107,144 | Ch19 What the Brain Is Doing at the Network Level (p297) | Figure 19.1 | From BFW_AllRewrites source document | Matplotlib 3.10.8 render; label is provenance, not rights; use Author-created diagram |
| hypnosis-rainville-finding.png | 1809x1059 | 126,228 | Ch19 The Rainville Finding (p299) | Figure 19.2 | From BFW_AllRewrites source document | Matplotlib; summarizes Rainville et al. 1997; use Author-created diagram, summarizing Rainville et al. 1997 (Science) |
| hypnosis-brain-wave-states.png | 1959x1134 | 138,101 | Ch19 The Alpha Shift (p301) AND Oscillations and Timing (p308) | Figure 19.3 and 19.4 | From BFW_AllRewrites source document | Same file twice (M2); five rows Delta, Theta, Alpha (highlighted), Beta, Gamma |
| reflex-name-chart.svg | viewBox 900x1400 (content to y 1055) | 55,463 | Ch24 The Name Chart (p430) | Figure 24.1 | Author-created chart | Well-formed XML, 107 text nodes; font and dead band issues (m6) |
| zodiac-fire-signs-mnemonic.jpg | 1408x768 | 466,014 | Ch25 FIRE SIGNS (p444) | unnumbered | AI-generated illustration | Gemini plus BeFunky |
| zodiac-water-signs-mnemonic.jpg | 1408x768 | 603,952 | Ch25 WATER SIGNS (p445) | unnumbered | AI-generated illustration | |
| zodiac-earth-signs-mnemonic.jpg | 1408x768 | 653,051 | Ch25 EARTH SIGNS (p446) | unnumbered | AI-generated illustration | |
| zodiac-air-signs-mnemonic.jpg | 1408x768 | 573,229 | Ch25 AIR SIGNS (p447) | unnumbered | AI-generated illustration | |
| chris-michael-author.jpg | 842x1264 | 327,264 | Front matter About (p12), back matter twice (p718, p719) | none | no rights record (injected at build-book.py 6406, outside FIGURES) | BeFunky-edited; add photographer credit; embedded three times (M3) |

Figure count check: 12 book-figure blocks in DESIGNED, GATED, NoBrookings-DESIGNED and NoBrookings-GATED; 15 img tags in DESIGNED (12 figures plus 3 author), 16 in GATED (plus the reveal logo). All FIGURES keys resolve to a real header in the right parser chapter (0 of 12 miss).

### 5b. Images embedded only in the DOCX (word/media; none reaches the build)

| File | Pixels | Anchor in the DOCX | Content | Rights | Status |
|---|---|---|---|---|---|
| image1.png (rId62, two references) | 1x1, 70 bytes | The Name Chart paragraph 3030; ABOUT THE AUTHOR paragraph 4779 | transparent placeholder at 0.69 inch | n/a | intentional placeholder; build replaces both |
| image5.png (rId57) | 1638x2048 | paragraph 2931, floating anchor in the "Read the whole chapter... Password: BuiltForWonder" block | "SCAN ME" QR to https://qr.link/uXLKtz (deactivated QR.io redirect) | n/a | missing from build (B1); code is dead |
| image3.png (rId58) | 1024x1024 | empty paragraph after ms 2773 | two closed fists side by side | unknown source, no watermark | missing from build (B2) |
| image4.png (rId59) | 896x1099 | inline at end of ms 2785 paragraph | single fist, index knuckle stepped | unknown source, no watermark | missing from build (B3) |
| image2.png (rId60) | 896x1196 | inline at end of ms 2785 paragraph | single fist, two fingers stepped | AI-generated (Gemini watermark bottom right) | missing from build (B3); crop watermark (M16) |
| image6.png (rId61) | 896x1196 | empty paragraph after ms 2818 "The chin tell." | seated man, both fists forward, chin turned | AI-generated (Gemini watermark) | missing from build (M1); crop watermark (M16) |

Extracted copies for the fix are at the scratchpad path gfx/docx-media/ (and gfx/refuter-media/word/media/ with corner crops).

### 5c. Assets on disk that nothing references

- resources/metv-images/hypnosis-fractionation-depth.png, 1646x980, 78,483 bytes, matplotlib ("Why fractionation works: each cycle goes deeper", Cycle 1-3, "Trigger word installed here"). Deliberately dropped per docs/10 line 188; the manuscript has zero mentions of fractionation, re-alerting or trigger words. Archive it.
- resources/metv-images/image_01.png to image_30.png, all 1190x1684 page renders from the METV manual export (17 are 22 KB blank pages sharing three md5s, 13 are 268 to 597 KB content pages) and image_31.png, a 64x64 icon. About 8 MB. None matches any DOCX media by md5. Move to previous-versions/ or resources/source/.
- resources/DUCHENNE SMILE.jpg (1408x768, byte-identical to the Ch14 figure), resources/Gemini_Generated_Image_j2x23fj2x23fj2x2.jpg (1408x768, the visible source of the lip compression figure), resources/BodyLanguageProjectCom-Compressed-Lips-2.jpg (500x750, watermarked third-party photo, Canon EOS-1D Mark II; correctly unused and must stay unused), resources/w1000-n22219JlqyT2zQoE.jpg (972x398, the Vanishing Inc logo the gate should embed instead of hot-linking).
- Repo-root index.html (899,480 bytes, title "The Architecture of Wonder", old T4-card era, on branch claude/book-editor) is a stale artifact and not the deploy source; the deployed file is git main:index.html, byte-identical to Built-for-Wonder-GATED.html.

### 5d. Generated graphics that render (element counts in DESIGNED; GATED and NoBrookings identical unless noted)

| Generator or block | Trigger | Count | Chapter | Status |
|---|---|---|---|---|
| tier-table (How to Read This Book legend) | front matter | 1 | front matter | good |
| gen_chapter_opener / gen_part_opener | CHAPTER n / PART n | 44 / 5 | all | good, except 10 empty hook slots (M11) and 4 missing interlude openers (M10) |
| gen_section_badge_strip | SECTION_BADGES keys | 15 | Ch37-42 only | 105 of 120 keys dead (M9) |
| margin icons (inline 18x18 SVG) | tier and category codes | 611 (609 NoBrookings) | all | good: 4 shapes, one color each (gold 178, blue 126, purple 100, red 207), all well-formed |
| gen_observation_table | "#" header at ms 526 | 1 (80 rows) | Ch9 | good |
| gen_six_area_radar plus gen_radar_category | SIX_AREA_RADAR (ms 966) | 1 plus 6 cards | Ch9 | renders; raw ampersand and font (m7) |
| DISC_HTML plus gen_disc_type_card / gen_disc_blend_card | DISC intro (ms 1015) | 1 plus 4 plus 4 | Ch10 | good |
| FIVE_CS_HTML | trigger sentence ms 440 | 1 | Ch8 | renders; READ pill invisible (m14) |
| gen_tier_card | T1 to T4 at ms 473-479 | 4 | Ch8 | good |
| gen_volunteer_card / gen_volunteer_matrix_entry | ms 1064-1091 | 7 / 4 | Ch11 | cards good; matrix broken (M5) |
| TELL_TABLE_HTML | TELL_TABLE (ms 1160) | 1 (6 tt-bands) | Ch12 | good |
| FRUIT_TO_FANG_TABLE_HTML / FRUIT_TO_FANG_FLOW | ms 1213 / 1215 | 1 (28 cells) / 1 | Ch13 | good |
| PATTERN_INTERRUPT_40PCT | ms 1312 | 1 | Ch13 | good; only one of four configured stats (m20) |
| COLD_WARM_HOT_HTML | header ms 1796 | 1 | Ch17 | renders; source rows duplicate beneath it (M7) |
| gen_principle_card | The Four Principles of Translation ms 1810 | 4 | Ch17 | good |
| gen_anthem_aria_card | ms 1830 area | 2 | Ch17 | good; deliberate pink/blue palette |
| FEEDBACK_SIGNALS_TABLE_HTML | ms 1883 | 1 (4 fsig-cards) | Ch17 | renders; titles near-invisible (M12) |
| ZODIAC_ELEMENT_TABLE_HTML | ms 2998 | 1 (3 zet3-blocks) | Ch25 | renders; element labels faint (M12) |
| gen_stage_card | 01 · PRIME to 07 · EMBED (ms 3784-3796) | 7 | Ch29 | good |
| gen_checklist_section | checklist heads | 5 | Ch29 | good; Ch34 head falls through (m11) |
| gen_recovery_card | ms 285-289 | 3 | Ch5 | good |
| gen_numbered_card | numbered heads | 15 | various | good |
| gen_warning_callout / gen_warning_header | ms 237 / 282, 3732 | 1 / 2 | Ch5, Ch28 | good |
| gen_performer_note / gen_spotlight / gen_pull_quote / gen_wyajd / gen_key_read | various | 14 / 25 / 16 / 6 / 42 | all | good; wyajd Ch4 keyed one chapter early (m10) |
| step headers (01 SHOES to 05 ENERGY) | NN NAME lines | 5 plus | Ch9 | good; Days of the Week variant unsupported (m3) |
| book-figure injection | FIGURES keys | 12 | Ch13, 14, 19, 24, 25 | renders; no CSS rule (M13) |
| reveal-logo (GATED only) | build-gated.py 169 | 1 | gate | hot-linked (m8) |

### 5e. Generators and markers with no output

No handler exists: CH18_DIAGNOSTIC_PANEL (B6), PERFORMANCE_MATRIX (B7), PERF_ARCH_FRAMEWORK_SVG (m1), CH18_IFYRE_PANEL (m2); all four are dropped by the guard at 3579-3593 and appear as [warn] lines in the build output. Handler exists but never fires: the Cold Reading Toolkit family (B4), gen_modality_card (M6), gen_t4_signal_card and gen_t4_table (M8), title-page and author-note-front (M4), gen_context_card and gen_error_card (m12), gen_video_embed (B1 option), and the rest of the m13 list. Dead CSS: .zet-table, .video-embed, .t4s-*, .crt-*, .toolkit-nav, .modality-card, .context-card, .error-card, .tp-*, .author-note-front and others listed in m13.

### 5f. Verified good (what the finders checked and found correct)

- Build reproducibility: python3 build-book.py manuscript-extracted.txt <scratch> is byte-identical to the repo DESIGNED.html with exactly four [warn] lines (the four markers above) and no image-not-found warning; manuscript-extracted.txt is current (a fresh extraction diffs to zero lines).
- Deploy parity: live aowbook.netlify.app (HTTP 200, 9,227,899 bytes) equals git main:index.html equals Built-for-Wonder-GATED.html except Netlify's automatic form rewrite on one line (+36 bytes). GATED equals DESIGNED plus one reveal-logo img and the gate ids; div and svg open/close tags balance in both. NoBrookings differs by exactly the four manifest sections (18 h3s, 4 margin icons) with all 12 figures and every designed block intact.
- All 15 img data URIs decode and open in PIL; declared mime matches sniffed format (jpeg 8, png 6, svg 1); every img has non-empty alt text; every FIGURES image sits in a book-figure with a figure-caption; zero relative or external image references in DESIGNED.
- 612 of 613 inline SVGs are well-formed XML (the radar ampersand is the one exception); no SVG lacks a viewBox; none has a fixed pixel width of 500 or more; the radar is capped at max-width 540px and the DISC chart scales to the column; the 6x9 @page text column is never exceeded.
- No marker literal leaks into any build (TELL_TABLE, ZODIAC_ELEMENT_TABLE, FRUIT_TO_FANG_*, PATTERN_INTERRUPT_40PCT, SIX_AREA_RADAR, FEEDBACK_SIGNALS_TABLE, PERF_ARCH_FRAMEWORK_SVG, PERFORMANCE_MATRIX, CR_SUMMARY_TABLE, TOOLKIT_NAV, [ITALIC], [BOLD], *PLACE HOLDER*, escaped entities); the only leaked literals are FRONT MATTER and the two page-number digits (M4, m9).
- Rendered PDF (735 pages at 6x9): cover, definitions page, contents with dotted leaders, How to Read This Book with tier badges and category icons, all five part openers with identical navy/gold treatment, chapter openers spot-checked at Ch1, 2, 3, 9, 25, all 12 figures column-aligned and legible with captions, the radar and DISC chart legible at 160 dpi, the Tell Table, Fruit to Fang table and flow, Five Cs grid, tier cards, recovery cards, the 40 percent pattern interrupt as a full dark page, the Cold-Warm-Hot graphic, the four Principle cards, both Anthem and Aria cards, the four feedback cards, the zodiac element table, the Meta Reveal opener and its 16-row design-summary table, the closing page and the back cover with its deliberate faint spot-UV text.
- Gate mechanics: fixed overlay removed 2.2 seconds after entry, #book-content toggled by class, exactly one .reader-name span personalised, Netlify Forms POST fire-and-forget, Google Fonts link present so the DISC chart's Montserrat resolves online. Caveat: the whole book is display:none until JS runs.
- Rights values as configured: 4x "From BFW_AllRewrites source document", 1x "Author-created chart", 2x "Author-owned photograph", 5x "AI-generated illustration"; corrections recommended in 5a.

## 6. Refuted and corrected claims

Nothing was discarded silently. Refuted outright:

- generator-coverage: "the IFYRE line renders as a plain orphan paragraph in Ch22". Refuted: HTML 4948-4953 shows the header followed by the styled key-read card (KEY_READS['CHAPTER 22'] at build-book.py 119), the same closer form Ch17 uses. Only the header inconsistency remains (m2).
- assets-and-docx: "the name chart's 10px 'If wrong' line runs past the 900 viewBox edge and is clipped". Refuted by a headless Chrome render at 900px: the line ends around x 790, inside the viewBox. Font, size and dead-band claims stand (m6).

Corrected in detail (claim kept, evidence or location fixed):

- generator-coverage coverage note "author-note-front renders once as designed": it never renders (0 occurrences), because tp_start looks for a literal DECODE BEHAVIOR line (M4). Its claim that the front About article "duplicates the condensed author note" is therefore also wrong.
- generator-coverage coverage note "gen_concept_box x4": the verifier's class-count script finds 0 concept-highlight hits, so gen_concept_box is dead (m13). Unresolved between the two counts; treat as dead until a rebuild proves otherwise.
- generator-coverage "gen_context_card and gen_error_card are safe to retire": they have live ALL-CAPS content in the manuscript and fail only on case (m12).
- generator-coverage WHAT_YOU_JUST_DID drift: only Ch4 is a clear miss; Ch8 matches the DOCX placement; Ch22 is pinned deliberately by WYAJD_AT_START (m10).
- rendered-pages QR finding marked fixable_in_build false and "needs a Drive ID from Chris": the QR already exists in the DOCX, so the injection is build-only; but the code itself is dead (B1), so Chris input is still needed for the URL.
- rendered-pages "printed to Letter-ish pages, add @page size 432x648pt": @page is already 6in by 9in at build-book.py 3891; the inset comes from the page margins and the print body background (m21).
- rendered-pages "em dashes in the thousands": 385 occurrences, 348 of them the author's prose, about 37 build-generated (m22).
- rendered-pages coverage note that the Ch12 opener at p145 has a hook quote: the PNG shows no quote; Ch12 is one of the ten empty hook slots (M11).
- rendered-pages 37A finding was understated: all four interludes fail the same way (M10).
- rendered-pages fsig-name finding was one instance of a nine-rule pattern (M12).
- text-references filed the sitcom grids under Ch22; they are in Ch23 (B5). Its "T4 Appendix referenced once in the HTML" is twice (M8). Its verifier note that the QR redirect is "live (HTTP 200)" is superseded by the assets-and-docx fetch of the page body, which is a QR.io deactivation notice (B1).
- text-references verifier reasons for its findings 18 through 22 (zodiac captions, short lists, dead generators, unused assets, rights) are offset by one entry in the merged data; each underlying claim is corroborated by another finder, so all five stand. Its gated-parity finding (23) was left unreviewed but is reproduced by html-structure.
- assets-and-docx hand-photo anchors were wrong (two-fists photo placed in the chapter intro, the pair placed after ms 2773); corrected to ms 2773 (two fists), ms 2785 (pair) and ms 2818 (chin tell) by the verifier and by two other finders.
- assets-and-docx "the postimg logo is the only external asset": Google Fonts is also fetched at load (m8).
- html-structure: image6 described as a third-party stock portrait; it is AI-generated with a Gemini watermark (M1, M16). Its "zet-table lacks break-inside" is moot because zet-table is dead CSS (m16). Its gated-parity counts (2 radars, 2 DISC charts, 5 pattern interrupts) were raw string counts including CSS; actual elements are 1 each (5d). Its suggestion to point Figure 19.4 at the fractionation chart is unsupported; docs/10 shows that figure was deliberately dropped (M2).
- html-structure and rendered-pages both graded PERF_ARCH_FRAMEWORK_SVG major; text-references and generator-coverage verifiers downgraded it to minor because the prose does not promise a diagram (m1). HOOK_LINES was graded minor by one verifier and major by another; listed as major (M11).

## Appendix: method and scratch files

Methods used: grep over manuscript-extracted.txt for every visual keyword and positional phrase (262 keyword hits, about 90 positional hits read in context); a body walk of word/document.xml mapping all 7 w:drawing and 9 w:tbl elements to manuscript lines; a scripted check of every FIGURES and SECTION_BADGES key against parse_manuscript output; class counts for every gen_* function and *_HTML constant in DESIGNED.html; PIL decode of every data URI; xml.etree parse of every inline SVG; md5 comparison of DOCX media against resources/; EXIF and PNG metadata reads; a headless Chrome render to a 735-page PDF with pdftotext and 109 page PNGs; curl of the live site and the QR redirect; macOS Vision decode of the QR.

Scratch files (session scratchpad, gfx/): check_promises.py, docx-tables.txt, audit.py and audit-out.txt, refute_keys.py, analyze.py and analyze.out, qr.swift, docx-media/ and refuter-media/ (extracted DOCX images and corner crops), chart-548.png and chart-900.png, render/ (book.pdf, book.txt, pages.json, page PNGs), live-index.html, rebuilt.html and scratch-build.html (byte-identical to the repo DESIGNED.html).
