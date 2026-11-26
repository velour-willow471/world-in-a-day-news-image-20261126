# The World in One Day — Thursday 26 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/c/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/velour-willow471/world-in-a-day-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/velour-willow471/world-in-a-day-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

Entry for the make.fun competition `news-image-20261126`: one image that sums
up the world's news of Thursday 26 November 2026.

## The image

A newspaper front page, drawn with code. The masthead names the day, and six
panels cover the day's leading stories:

1. **Trade** — the US proposes new tariffs on 14 partners, including China,
   the EU, Japan and India, aimed at factory overcapacity.
2. **Energy** — Houthis strike Saudi Arabia's biggest refinery, Ras Tanura;
   oil prices climb.
3. **War** — Ukraine hits a Russian airbase, damaging five jets, and says it
   struck two refineries in Samara.
4. **Disaster** — a fuel tanker fire on Cairo's ring road kills at least 31.
5. **Nuclear** — Kim Jong Un orders wider deployment of tactical nuclear
   weapons, KCNA reports.
6. **Israel** — judges urge prosecutors to drop the gravest charge in
   Netanyahu's corruption trial.

The footer adds the Bank of Korea's rate rise to 3.25%, the AI sell-off
dragging the Nasdaq toward a bear market, and the MiniMax data-access report.
Every story was verified against at least two independent reputable sources
(Reuters, CNN, AP wires via other outlets) on 26 November 2026; see
`SOURCES.md`.

## How it is built

- `draw.py` draws `entry.png` (1024×1024, deterministic — two runs write
  identical bytes) with Pillow and the DejaVu fonts.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`).

Run it locally:

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
