# Install — EPWForge for Grasshopper

A single Grasshopper component that fetches an EPW from [EPWForge](https://epwforge.com) for any lat/lon and saves it to disk. Pair with Ladybug's `Import EPW` / `Construct Location` exactly like you would any other weather source.

**Requirements:** Rhino 8 (Python 3 / CPython) — the script uses Python 3 stdlib only, no extra packages.

## 5-minute setup

1. **Get an API key** at [epwforge.com/account](https://epwforge.com/account) and copy the `sk_live_...` value somewhere safe.

2. **Open Grasshopper** in Rhino 8. Drop a **Python 3 Script** component on the canvas (`Maths → Script → Python 3 Script`).

3. **Add inputs** to the component (right-click each input, "Type Hint" → set the type). At minimum:

   | Input | Type Hint | Required |
   |---|---|---|
   | `Lat` | `float` | yes |
   | `Lon` | `float` | yes |
   | `ApiKey` | `str` | yes |
   | `SavePath` | `str` | yes (full path including `.epw`) |
   | `Run` | `bool` | yes |

   Optional inputs (add as you need them):

   | Input | Type Hint | Default |
   |---|---|---|
   | `Basis` | `str` | `tmy` |
   | `AmyYear` | `int` | — |
   | `Ssp` | `str` | — |
   | `Year` | `int` | — |
   | `Percentile` | `int` | 50 |
   | `Uhi` | `str` | `none` |
   | `Events` | `str` | — |
   | `EventDuration` | `int` | 14 |
   | `Intensity` | `str` | — |
   | `IntensityAuto` | `bool` | `True` |
   | `Smoke` | `bool` | `False` |
   | `SmokeIntensity` | `int` | — |
   | `SmokeDuration` | `int` | — |

4. **Add outputs:** `EpwPath`, `Filename`, `Status`, `Metadata`.

5. **Paste the script.** Open `src/EPWForge_GenerateWeatherFile.py` from this repo, copy everything, and paste it into the component's code editor. Save.

6. **Wire inputs** — Panel components are the easiest source for `ApiKey`, `SavePath`, and other string params; Number Sliders for `Lat` / `Lon` (or Ladybug's `Construct Location`).

7. **Set `Run` to `True`** to fetch. The component is gated behind `Run` so the API isn't hit every time you change another wire.

## Example wirings

**Basic TMY for any city:**
```
Lat → 40.71      ApiKey → sk_live_...      Run → True
Lon → -74.01     SavePath → C:/weather/nyc_tmy.epw
```

**Future-stressed scenario for resilience analysis:**
```
Lat → 33.45      Ssp → ssp585              Events → "heatwave,hothumid"
Lon → -112.07    Year → 2090               EventDuration → 14
Uhi → "urban"    Percentile → 90           Smoke → True
                                            SmokeIntensity → 5
```

**Honeybee / Ladybug downstream:**
- Connect `EpwPath` into Ladybug's `Import EPW`. Everything that consumes an EPW downstream (annual simulation, comfort analysis, ASHRAE design days) works unchanged.

## API key handling — please read

The `ApiKey` input is a string. **Do not save** the API key into Grasshopper files you share — anyone who opens the file gets your key. Two cleaner patterns:

- Read the key from an environment variable inside the script (edit the `ApiKey` resolution to fall back to `os.environ.get("EPWFORGE_API_KEY")`).
- Read it from a local text file outside the project, e.g., `C:/Users/you/.epwforge/key.txt`.

## Saving the component as a user object (one-click reuse)

Once configured:
- Right-click the component → **Create User Object**
- Fill in name (e.g., "EPWForge - Weather File"), category ("EPWForge"), description.
- It now appears in the Grasshopper toolbar permanently and can be dropped onto any canvas.

## Troubleshooting

- **"ERROR: EPWForge API 403"** — your API key isn't authorized for the requested feature (SSP / ensemble require Pro plan). Upgrade at [epwforge.com/pricing](https://epwforge.com/pricing).
- **"ERROR: EPWForge API 429"** — rate-limited. Wait a moment and re-trigger `Run`.
- **"ERROR: HTTP Error 401"** — API key is wrong or revoked.
- **No file appears at SavePath** — check `Status` output for the error message; the component never raises silently.

## Want a compiled .gha plugin?

This Python component is the fast-iteration path. A compiled `.gha` (proper Grasshopper plugin distributed via Food4Rhino + the Rhino Package Manager) is on the roadmap — track [github.com/guzz-labs/epwforge-grasshopper](https://github.com/guzz-labs/epwforge-grasshopper) for updates.
