# Odds-processing and Discord prototype

Historical Python experiments for collecting odds, calculating expected-value examples and forwarding results to Discord. The repository contains source and a container recipe; it does not establish that an AWS deployment is currently running or that an observed opportunity can be executed profitably.

## Source map

- `main.py`, `game_id_scraper.py`: provider-specific collection experiments.
- `EVCalculator.py`: arithmetic helpers.
- `discord_main.py`: Discord integration.
- `Starter.py`: process orchestration.
- `conf.py`: request templates; copied browser cookies/session identifiers have been removed.

## Configuration and verification

Use Python 3.12 with `pip install -r requirements.txt`. Supply your own `DISCORD_BOT_TOKEN`. Optional browser/session configuration is JSON supplied via the names in `.env.example`, never copied into source. Values must be objects; malformed values fail without echoing their content. Current provider contracts/terms and account permissions must be reviewed before running the collector. No provider access is needed for:

```sh
python -m unittest discover -s tests -v
```

The container can be built with `docker build -f docker_test.dockerfile .`; running it is intentionally not part of offline CI because collection and messaging have external side effects. The checks validate safe configuration and absence of credential literals, not trading performance or live API compatibility.

## Attribution and status

Retain the original Git author history and any upstream attribution when reusing the work. Historical README screenshots pointed to external contributor material; they are not claimed as this repository's verified live deployment evidence. See [SECURITY.md](SECURITY.md) before reusing historical credentials or cookies.
