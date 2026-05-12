# epwforge-grasshopper

> Grasshopper / Rhino integration for [EPWForge](https://epwforge.com). Fetch climate-stressed EPW weather files for any global location directly inside your Ladybug / Honeybee canvas.

**What it does:** drop a Python component on the Grasshopper canvas, wire `Lat` / `Lon` / `ApiKey` / `SavePath`, optionally configure SSP / UHI / events / smoke, and you get a valid `.epw` written to disk plus a `Path` output ready to pipe into Ladybug's `Import EPW`.

**Status:** Python 3 script for Rhino 8. Single-file, no extra packages. Compiled `.gha` plugin in the roadmap.

## What you can do with it

| Goal | Wire-up |
|---|---|
| Generate a TMYx for any city worldwide | `Lat`, `Lon`, `ApiKey`, `SavePath`, `Run=True` |
| Actual Meteorological Year for a specific year | + `Basis="amy"`, `AmyYear=2023` |
| Future-climate stressed file (CMIP6 morphing) | + `Ssp="ssp245"`, `Year=2050` |
| Layer urban heat island | + `Uhi="urban"` |
| Inject extreme events (heat wave, cold snap, etc.) | + `Events="heatwave,hothumid"` |
| Compound events (auto-blend) | `Events="heatwave,hothumid"` blends humidity into heat; `Events="coldsnap,coldwindy"` does the same for wind |
| Wildfire smoke overlay | + `Smoke=True`, `SmokeIntensity=5` |
| Worst-case design scenario | All of the above in one call |

## Quick install

See [INSTALL.md](INSTALL.md) for full step-by-step. The 30-second version:

1. Get an API key at [epwforge.com/account](https://epwforge.com/account).
2. Drop a Python 3 Script component in Grasshopper.
3. Add inputs (`Lat`, `Lon`, `ApiKey`, `SavePath`, `Run`, ...).
4. Paste [`src/EPWForge_GenerateWeatherFile.py`](src/EPWForge_GenerateWeatherFile.py) into it.
5. Wire and set `Run=True`.

## Tier requirements

- **Free** — `find_station`-equivalent (n/a in this component)
- **Starter** — TMYx / AMY generation, UHI, events, smoke (no SSP)
- **Pro** — SSP future-climate morphing, ensembles

Tier enforcement is server-side; an unauthorized request returns a clean error in the `Status` output.

## Roadmap

- [ ] Compiled `.gha` plugin (C# Grasshopper assembly)
- [ ] Companion components: `Generate Design Day (DDY)`, `Generate Ensemble`, `Find Nearest Grid Cell`
- [ ] Food4Rhino + Rhino Package Manager listing
- [ ] Honeybee `Annual Simulation` integration example

## Links

- **Platform:** [epwforge.com](https://epwforge.com)
- **API docs:** [epwforge.com/docs](https://epwforge.com/docs)
- **Python client:** `pip install epwforge` (forthcoming)
- **MCP server (for AI agents):** `pip install epwforge-mcp` ([PyPI](https://pypi.org/project/epwforge-mcp/))
- **Maker:** [Guzzlabs](https://guzzlabs.com)

## License

MIT
