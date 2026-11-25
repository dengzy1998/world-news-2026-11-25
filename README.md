# The World Today — Wednesday 25 November 2026

One image summing up 25 November 2026's world news: 52 sourced stories
across 6 regions — 3 illustrated leads, 12 grid cards, 37 one-liners — plus
a UTC timeline, a numbered schematic map, and a DATE CHECK box listing
older stories deliberately left out.

Entry for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125).

## How it is built

`render_poster.py` draws `entry.png` (1024×1024, Pillow, deterministic)
from the story ledger in `../stories.md`. `main.py` (standard library only)
copies that finished image to `$MAKEFUN_OUTPUT_DIR/entry.png`, so both
grading runs produce byte-identical output.

## Sources

AP, Reuters, South China Morning Post, Yeni Safak, OneTurn, MyKhel,
Arab News, ProCappers — see `../stories.md` for the per-story ledger.
