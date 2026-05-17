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

## Pricing

EPWForge runs on a credit model. **Generation costs credits; unmodified TMY downloads are free.**

| Action | Credits |
|---|---|
| Unmodified TMY for any location | 0 (free) |
| AMY year / SSP-morphed / UHI / event / smoke EPW | 1 |
| Per-model CMIP6 ensemble (~20 EPWs) | 10 |

| Plan | Monthly credits | $/mo |
|---|---|---|
| Free | 5 lifetime (one-time welcome) | $0 |
| Starter | 10 | $49 |
| Pro | 50 | $149 |
| Pro+ | 100 | $249 |

Sign up at [epwforge.com/account](https://epwforge.com/account) to get an API key + 5 welcome credits. Out-of-credits requests return a clean `402` in the component's `Status` output.

## Roadmap

- [ ] Compiled `.gha` plugin (C# Grasshopper assembly)
- [ ] Companion components: `Generate Design Day (DDY)`, `Generate Ensemble`, `Analyze Weather`, `Find Station`
- [ ] Food4Rhino + Rhino Package Manager listing
- [ ] Honeybee `Annual Simulation` integration example

## Links

- **Platform:** [epwforge.com](https://epwforge.com)
- **API docs:** [epwforge.com/api-docs](https://epwforge.com/api-docs)
- **MCP server (for AI agents):** [epwforge.com/mcp](https://epwforge.com/mcp) · `uvx epwforge-mcp`
- **Maker:** [Guzzlabs](https://guzzlabs.com)

## License

MIT
