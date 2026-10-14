# Instructions for continuing the illustrated collection

The user wants source-specific explanations for a general reader, with the existing research topics first. Use the model to read each manuscript and author its explanation. The build scripts format authored material; they do not generate explanations from titles or abstracts.

The previous failure was generic boxes that did not teach the mathematics. Every figure must therefore show an actual mathematical object or a checked example: coefficients, incidence entries, geometric constraints, probability mass, explicit state changes, or quantitatively labeled growth. A process diagram is useful only if its relationships carry specific mathematical information. Include captions that explain how to read each diagram and what conclusion it supports.

For each new paper:

1. Pin a source commit, read the actual manuscript, preserve its PDF, source, citation, license, and file hashes. Do not infer the proof from the abstract. Inspect the manuscript's build instructions and any applicable repository instructions.
2. Author a route from familiar definitions to the paper's mechanism. Explain quantifiers, normalization, assumptions, and the scope of the theorem before interpreting its implications. Include worked examples and source section/page anchors. Preserve attribution to earlier work.
3. Label each diagram as an original object, a teaching example, or an asymptotic expression. Never label a toy as a counterexample, benchmark, or verified instance of a large construction. Never invent an unspecified constant or threshold. Do not replace a paper's claim with a later conditional community result.
4. Check finite arithmetic and combinatorics exactly where possible. Avoid tests that merely assert copied constants. Keep these checks distinct from verification of the full theorem or a Lean formalization.
5. Build a readable guide and an expanded edition containing the complete original. This batch puts the guide first and appends unchanged original pages; do not describe it as annotations interleaved with the original proof. Maintain source page numbers and bookmarks.
6. Render and inspect every new guide page and diagram. Confirm the appended pages render identically to the source. Check captions, missing glyphs, clipping, links, source hashes, and archive contents.
7. Embed core diagrams in the paper README. Update the catalogue only when the actual guide, figures, and expanded edition are present. Confirm GitHub commits, file blobs, and rendered README image references after upload.

All source edits, builds, caches, previews, downloads, and logs must stay on the mounted writable external SSD under `/Volumes/SP AI 01_16/CodexWorkspaces`. Never silently fall back to Documents, Desktop, or iCloud Drive. Do not change unrelated research repositories or their claims as part of creating a reading edition.

The publication is independent and not an official OpenAI release. The source collection itself warns that results are at different verification stages. Explain a source claim faithfully without presenting the reading edition as an independent validation.
