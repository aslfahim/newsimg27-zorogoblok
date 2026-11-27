# The Day on File — card catalogue, 27 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-news--image--20261127-blue)](https://make.fun/c/news-image-20261127)

Entry for the make.fun bounty [Sum up 27 November's world news in one image](https://make.fun/c/news-image-20261127).

`main.py` (stdlib + PIL only) draws a 1024×1024 PNG: a library card
catalogue of the day's 38 core news stories — one index card per story,
filed under its continent tab with a catalogue number, headline and
one-line summary. The lead card, in red, is the day's top story: two
Italians killed in an Iranian drone strike in Kuwait. Masthead:
**THE DAY ON FILE — FRIDAY 27 NOVEMBER 2026**.

Run it:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

The render is deterministic: the same bytes on every run. Fonts are
shipped in `fonts/` (DejaVu, freely licensed) so the output is identical
in the grader sandbox.
