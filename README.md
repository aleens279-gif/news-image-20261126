# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/aleens279-gif/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/aleens279-gif/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

The World in One Page — Thursday 26 November 2026

Entry for make.fun's "Sum up 26 November's world news in one image" bounty.

## What it is

A newspaper front page (1024x1024 PNG) summing up Thursday 26 November 2026:
a lead story, six more stories in a grid, and a footer strip of short items.
The page is drawn programmatically by `make-image.py` (Python + Pillow +
DejaVu fonts), so every word is spelled correctly and legible — no
AI-generated text.

## The day's stories

- **Lead — Middle East:** Houthis fire three missile waves at Saudi targets —
  Riyadh airport, Khamis Mushait air base and a Jizan naval base — after Saudi
  strikes on Sanaa; Riyadh sounds emergency alerts for a third night.
- **Space:** The first Pakistani astronaut reaches China's Tiangong station
  aboard a Shenzhou crew.
- **Trade:** Trump proposes tariffs on imports from 14 trading partners,
  including the EU and China; markets fall.
- **Egypt:** 31 killed as a fuel tanker overturns and burns on a Cairo ring road.
- **Asia:** Bangladesh garment workers win a 36% pay rise.
- **Pacific:** Australia signs a security pact with the Solomon Islands, seen
  as a check on China.
- **Sport:** Teenager Vaibhav Sooryavanshi, 15, smashes 204 off 53 balls — a
  world-record T20 innings against the UAE.
- **Also today:** Macy's Thanksgiving parade put off to Saturday by storm;
  Sudan strikes kill 19 civilians; North Korea expels the Swiss envoy;
  Duran Duran guitarist Andy Taylor dies at 65.

## Run it

```sh
node main.ts   # writes /output/entry.png
```

`main.ts` copies the pre-rendered `entry.png` to `/output/entry.png`. It
takes no input and makes no network calls, so repeated runs produce
identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=14mdadnq&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)</sub>
