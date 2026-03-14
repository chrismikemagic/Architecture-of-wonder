# The Architecture of Wonder — Book Project

## Your Editing Document

**`Architecture-of-Wonder.docx`** — This is your master content document. Edit this file for all content changes. It contains the complete manuscript including:
- All 41 chapters across 8 parts
- Introduction, Glossary, T4 Appendix, About the Author
- The Meta Reveal chapter (the "standing ovation" moment)
- Expanded Five Cs framework (Context, Clusters, Congruence, Consistency, Culture)

## Project Structure

```
Architecture-of-Wonder.docx          <-- EDIT THIS (your working manuscript)
Architecture-of-Wonder-DESIGNED.html  <-- Generated output (don't edit directly)
build-book.py                         <-- Converts manuscript to designed HTML
manuscript-extracted.txt              <-- Text extracted from DOCX (used by build script)

design-reference/                     <-- Design specs and mockups
  design-specification.md             <-- Complete design bible
  designer-implementation-guide.md    <-- Page-by-page production guide
  chapter-template.md                 <-- Hook lines + key reads for all chapters
  meta-reveal-chapter.md              <-- Meta Reveal full text
  Expanded-Observation-List.md        <-- Extended observation list
  graphics/                           <-- SVG mockups and diagrams

resources/                            <-- Reference materials (B2B deck, profiling guide, etc.)
previous-versions/                    <-- Earlier drafts
backups/                              <-- DOCX backups
```

## How to Generate the Designed Book

1. Edit `Architecture-of-Wonder.docx` with your content changes
2. Run `python3 build-book.py` to generate the designed HTML
3. Open `Architecture-of-Wonder-DESIGNED.html` in a browser
4. Print to PDF for the final formatted version
