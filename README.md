# Case studies

Jonathan Bayo's automation case studies, published at https://zilyn.github.io/case-studies/ from the `main` branch.

## Editing

All copy lives in `build.py` in the `PROJECTS` list. Change the text there, then run

    python build.py

which rewrites `index.html`, one page per project and `404.html`. Styles are in `assets/site.css`, the filter and theme script in `assets/site.js`. Commit the generated pages along with `build.py`; GitHub Pages serves the files as they are.

Adding a project means adding one dict to `PROJECTS` with a `slug`, a category from `CATS`, a status from `STATUS`, the copy and the pipeline nodes. Node types are `trigger`, `fetch`, `transform`, `ai`, `store` and `send`.

A featured project shows as a trading card on the front page and also needs a `card` dict: `name`, `role`, `text`, `color` (base, light, "r,g,b") and `sprite`, one of the pixel mascots in `SPRITES`. The rest are grouped into one pack per category (`PACKS`, short names in `SHORT`); clicking a pack filters the list below it.
