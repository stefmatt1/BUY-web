# BUY-web

Static site for [BUY$ The Card Game](https://buythecardgame.com).

- `index.html`, `privacy.html`, and `terms.html` are the marketing and legal pages.
- `score-tracker/` is an Expo web export of the score tracker. The app expects to be served at `/score-tracker` (scripts, images, and routes use that prefix).
- `serve.py` is a small Python server for local preview. It serves the site from this folder and maps extensionless tracker routes such as `/score-tracker/game` to `score-tracker/game.html`.

## Run locally

Requires Python 3. From this folder:

```bash
python serve.py
```

Then open [http://127.0.0.1:8765/](http://127.0.0.1:8765/). The score tracker is at [http://127.0.0.1:8765/score-tracker](http://127.0.0.1:8765/score-tracker).

Opening `index.html` as a file will not load the tracker correctly, because its assets are requested from `/score-tracker/...`.
