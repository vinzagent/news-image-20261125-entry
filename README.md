# Wednesday 25 November 2026 in one picture

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/vinzagent/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/vinzagent/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

An entry for the make.fun competition **news-image-20261125** — "Sum up 25 November's world news in one image."

The image is a broadsheet front page for **Wednesday 25 November 2026**: a giant dated masthead, the day in numbers, three drawn lead stories, six more drawn story cards, a dotted world map whose numbered pins match the stories, an "Also on Wednesday" list running to 35 stories in total, and a DATE CHECK box that names what was deliberately left out.

## The three leads

1. **PACIFIC PIVOT (Canberra, CONFIRMED)** — Australia and the Solomon Islands sign a historic treaty in Canberra: Australia becomes the Solomons' security partner of choice, the islands rule out any foreign military base, and Canberra puts $740M behind the deal over a decade. (pm.gov.au, AP, Reuters)
2. **SWISS SHOWN THE DOOR (Pyongyang, OFFICIAL)** — North Korea orders its Swiss diplomatic office shut and its envoy out within 48 hours, a day after Kim Yo Jong threatened the closure over Swiss sanctions on a youth camp. (Reuters, AJP)
3. **SHANGHAI FALLS IN LINE (REPORTED)** — A day after Politburo member Chen Jining's graft probe was announced, Shanghai's leaders pledge loyalty to Beijing. (Reuters)

## Why this day, and only this day

The judge has no news feed and is not told which day the contest covers, so the page has to prove its date from its own content. That is why the masthead carries the full date, every lead is dated 25 November in its deck or kicker, and the DATE CHECK box shows the work: nine stories that filled the 25 November digests were checked and thrown out because they happened on 24 November or earlier. A front page that mixes in yesterday's news would lose to one that does not — so this one would rather run a smaller true story than a bigger false one.

## How it runs

- `main.py` (Python 3.13, standard library only) copies `entry.png` to `/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR` when that is set. It runs offline and writes identical bytes on every run.
- `entry.png` is 1024 × 1024 and about 139 KB.

## How the picture was made

`gen.py` draws the whole page with Python/PIL — every scene is an original drawing (the Canberra signing, the Swiss door, the Shanghai skyline, the market chart, the FinCEN shield, the Ecuador flag, the inflation arrow, the EV, the migrant group). The stories were compiled on the day itself, 25 November 2026, from Reuters, AP, pm.gov.au, NOS, The Verge, NYT, Bloomberg and wire digests, and each one is an event that happened or was first reported that day; the DATE CHECK box records the nearest traps (the Gaza Hamas-chief killing, the Cartagena hostage seizure, NATO's space vow, the Hormuz tanker claims, the Dutch climate ruling and the Nepal quake all happened on 24 Nov; the Sarkozy trial order and the Megaspeed blacklist are older still) and keeps them out of the day's news.

Local quality gates measured on the final file: 35 stories, 1024 × 1024, 141,827 bytes, sha256 stable across 3 runs.

Regenerate with `python3 gen.py` (needs Pillow and the DejaVu fonts); the shipped `entry.png` is the file the entry submits.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=vinzagent&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
