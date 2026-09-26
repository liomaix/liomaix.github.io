# liomaix.github.io

Static site, no build step needed by GitHub Pages.

- Content lives in `build.py` (publications, talks, news, equations). Edit it, then run `python3 build.py` to regenerate the HTML pages.
- Topics: `cyber` (violet), `climate` (green), `micro` for market microstructure (copper). Tag a publication or news item with them to colour it and make it filterable; a filter button only appears once a topic has at least one item on the page.
- Equations are LaTeX, rendered by KaTeX. In HTML, write `\lt` and `\gt` instead of `<` and `>`.
- Keep `profile_.jpg` (4:3, e.g. 2000x1500) and the `files/` folder (CV and slides) at the repository root.
- The hero photo and text scale with the window width (see the `.hero` rules in `style.css`).
