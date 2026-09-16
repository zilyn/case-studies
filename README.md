# Case studies

Jonathan Bayo's automation case studies, published at https://zilyn.github.io/case-studies/ from the `main` branch.

## Editing

All copy lives in `build.py` in the `PROJECTS` list. Change the text there, then run

    python build.py

which rewrites `index.html`, one page per project and `404.html`. Styles are in `assets/site.css`, the filter and theme script in `assets/site.js`. Commit the generated pages along with `build.py`; GitHub Pages serves the files as they are.

Adding a project means adding one dict to `PROJECTS` with a `slug`, a category from `CATS`, a status from `STATUS`, the copy and the pipeline nodes. Node types are `trigger`, `fetch`, `transform`, `ai`, `store` and `send`.
