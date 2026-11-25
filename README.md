# The World in One Day — 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/claymoreth/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/claymoreth/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the make.fun competition
[Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125).

`main.py` copies the pre-built `entry.png` (a 1024×1024 newspaper front
page summing up Wednesday 25 November 2026 — 30 stories from 7 regions:
3 heroes, 10 cards and 17 more stories, with a dotted world map) to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

`build.py` draws `entry.png` from scratch with Pillow (stdlib + PIL only,
no network, deterministic — two runs produce identical bytes).
