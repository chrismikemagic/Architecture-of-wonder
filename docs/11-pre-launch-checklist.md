# Pre-Launch Checklist

> Items to review and complete before the book is considered production-ready. Add to this list throughout the project. Clear items only when they have been tested in the built HTML.

---

## Design & Formatting

- [ ] **Section badge review** — Verify tier and observation category assignments in `SECTION_BADGES` are accurate across all chapters. Add any missing sections that deserve a badge. Confirm none are misfiled (e.g. T1 assigned to field-tested patterns). Approximately 120 badges currently placed; do a chapter-by-chapter pass.

- [ ] **Chapter opener legend accuracy** — Spot-check `CHAPTER_LEGEND` mappings against actual chapter content. Confirm tiers and categories shown on each opener reflect what is inside.

- [ ] **Pattern interrupt placement** — Read through the full HTML and confirm no pattern interrupts appear mid-card-sequence or in awkward positions. The `_is_card_trigger` guard handles most cases but edge cases may exist.

- [ ] **Priming image system** — Four full-bleed priming images to be commissioned and inserted at:
  1. Early (Chs 2–3): Surveillance — dominant face/eye with direct gaze
  2. Early-mid (Chs 13–14): Convergence — crowd with shared attention
  3. Mid (before Ch10): Split-Signal Portrait — face with quietly incompatible emotional cues
  4. Late (before Ch11 or Ch31): The Missing Center — group reacting to something not shown
  Once images are finalized, add to `FIGURES` dict and update Meta Reveal copy to name them and explain why each was chosen.

- [ ] **"How to Read This Book" section** — Add explanation of the tier badge system (T1–T4) and observation category icons (BP, CR, VS, AM) so readers understand what the inline badges mean before they encounter them.

---

## Content

- [ ] **Chapters with missing hook lines** — Several chapters marked "(needs hook)" in `docs/07-chapter-map.md`. Review `HOOK_LINES` dict and fill any gaps.

- [ ] **Chapters with missing key reads** — Several chapters marked "(needs key read)" in chapter map. Review `KEY_READS` dict and fill any gaps.

- [ ] **Meta Reveal accuracy pass** — Walk through the Meta Reveal section and confirm every technique it names is still present in the book. The checklist in `docs/08-meta-reveal-checklist.md` tracks this; sync after any structural changes.

- [ ] **T4 signal appendix** — Confirm T4 signal cards appear correctly in both Ch7 inline and the appendix. Verify disclaimer language is present before each.

---

## Production

- [ ] **Image rights audit** — Confirm all entries in `FIGURES` dict have an accurate `rights` field. No unlicensed images in the final build.

- [ ] **Build clean on both scripts** — Run `python build-book.py && python build-gated.py` from clean state and confirm no errors or warnings.

- [ ] **Gated version access test** — Test the gate overlay: confirm it blocks content, localStorage persistence works, and the unlock flow is correct.

---

## Notes

- Add items here as they come up during editing sessions.
- Do not remove items until they have been tested in the built HTML, not just edited in source.
