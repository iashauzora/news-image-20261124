# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/iashauzora/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/iashauzora/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world's news of Tuesday 24 November 2026: a newspaper front page, "THE WORLD IN A DAY", rendered with PIL. The lead story is Nvidia's board unanimously reinstating Jensen Huang as CEO; alongside it, leaked data puts Russia's war death toll near 700,000, the Pentagon has yet to approve 60 Patriot interceptors already allocated to Ukraine, SpaceX and Tesla entrust five directors with a potential $3.5 trillion merger, South Korea scrambles jets as Russian warplanes enter its air zone, and Malaysia tells data centres to cut off US-blacklisted firms. Every story was reported on 24 November 2026 by at least two independent sources — full citations in `design/sources.md`, and the page itself is drawn by `design/render.py`.

## Run it

```sh
node main.ts
```

`main.ts` validates `entry.png` (PNG/JPEG by magic bytes, at most 1024x1024, at most 1 MiB) and copies it, byte for byte, to `/output/entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=sy4xfh92&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
