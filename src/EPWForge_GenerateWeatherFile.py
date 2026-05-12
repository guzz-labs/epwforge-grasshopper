"""EPWForge — Generate Weather File (Grasshopper component, Rhino 8 CPython 3)

Drop this code into a Grasshopper Python 3 component to fetch a climate-stressed
EPW from EPWForge for any lat/lon. Pair with Ladybug's "Construct Location" /
"Import EPW" upstream/downstream as you would any Ladybug weather source.

INPUTS (rename each input in Grasshopper to match):
    Lat              (float, required)   — latitude, decimal degrees
    Lon              (float, required)   — longitude, decimal degrees
    ApiKey           (str,   required)   — sk_live_... key from epwforge.com/account
    SavePath         (str,   required)   — full path for the .epw to be written
    Run              (bool,  required)   — set True to fetch (component is gated to avoid surprise downloads)

    Basis            (str,   default "tmy")    — "tmy" or "amy"
    AmyYear          (int,   optional)         — year for AMY basis
    Ssp              (str,   optional)         — "ssp126" | "ssp245" | "ssp370" | "ssp585"
    Year             (int,   optional)         — 2030 | 2050 | 2070 | 2090
    Percentile       (int,   default 50)       — 5,10,25,50,75,90,95
    Uhi              (str,   default "none")   — "none" | "suburban" | "urban" | "dense_urban"
    Events           (str,   optional)         — CSV: "heatwave,hothumid"
    EventDuration    (int,   default 14)       — 3..30 days
    Intensity        (str,   optional)         — CSV: "heatwave:8,hothumid:7"
    IntensityAuto    (bool,  default True)     — AR6 ensemble auto-fill under SSP
    Smoke            (bool,  default False)    — wildfire smoke overlay
    SmokeIntensity   (int,   optional)         — 1..10 → peak AOD 0.1..6.0
    SmokeDuration    (int,   optional)         — 3..30 days

OUTPUTS:
    EpwPath          — absolute path to the saved EPW
    Filename         — server-suggested filename
    Status           — human-readable summary
    Metadata         — full JSON response for downstream parsing

NOTES:
    * Auth and file output happen client-side; this component does NOT save the
      API key into the Grasshopper file. Wire it from a Panel that you keep
      out of shared scripts, or set it via a Honeybee/Ladybug secrets workflow.
    * Tier gating: SSP / ensemble features require an EPWForge Pro plan;
      free-tier keys will surface a 403 error in Status.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


BASE_URL_ENV = "EPWFORGE_BASE_URL"
DEFAULT_BASE_URL = "https://epwforge.com"
TIMEOUT_SECONDS = 60


# --- gh component glue ------------------------------------------------------
# Inputs come in as module-level names matching the Grasshopper input names.
# Provide defaults for the optional ones so the component degrades cleanly
# when a wire isn't connected.
def _opt(name, default=None):
    v = globals().get(name)
    return default if v is None else v


def _build_query():
    qs = {
        "lat": float(Lat),
        "lon": float(Lon),
        "basis": _opt("Basis", "tmy"),
        "percentile": int(_opt("Percentile", 50)),
        "uhi": _opt("Uhi", "none"),
        "event_duration": int(_opt("EventDuration", 14)),
        "intensity_auto": "true" if _opt("IntensityAuto", True) else "false",
        "format": "json",
    }
    if _opt("AmyYear") is not None:
        qs["amy_year"] = int(AmyYear)
    if _opt("Ssp"):
        qs["ssp"] = Ssp
    if _opt("Year") is not None:
        qs["year"] = int(Year)
    if _opt("Events"):
        qs["events"] = Events
    if _opt("Intensity"):
        qs["intensity"] = Intensity
    if _opt("Smoke"):
        qs["smoke"] = "true"
    if _opt("SmokeIntensity") is not None:
        qs["smoke_intensity"] = int(SmokeIntensity)
    if _opt("SmokeDuration") is not None:
        qs["smoke_duration"] = int(SmokeDuration)
    return qs


def _fetch(api_key, qs):
    base = os.environ.get(BASE_URL_ENV, DEFAULT_BASE_URL).rstrip("/")
    url = base + "/api/epwforge?" + urllib.parse.urlencode(qs)
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + api_key,
        "User-Agent": "epwforge-grasshopper",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # Surface the API's structured error rather than the generic urllib message.
        try:
            body = e.read().decode("utf-8", errors="replace")
            msg = json.loads(body).get("error", body)
        except Exception:
            msg = "HTTP " + str(e.code)
        raise RuntimeError("EPWForge API " + str(e.code) + ": " + str(msg))


def _save(epw_b64, path):
    import base64
    data = base64.b64decode(epw_b64)
    out = os.path.expanduser(path)
    parent = os.path.dirname(out)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with open(out, "wb") as f:
        f.write(data)
    return out, len(data)


# --- main flow --------------------------------------------------------------
EpwPath = ""
Filename = ""
Status = ""
Metadata = None

if not Run:
    Status = "Idle — set Run=True to fetch."
elif not ApiKey or not str(ApiKey).startswith("sk_"):
    Status = "ERROR: ApiKey is missing or not a sk_live_... key. Get one at https://epwforge.com/account."
elif Lat is None or Lon is None:
    Status = "ERROR: Lat and Lon are required."
elif not SavePath:
    Status = "ERROR: SavePath is required (full path including .epw filename)."
else:
    try:
        qs = _build_query()
        data = _fetch(str(ApiKey), qs)
        b64 = data.get("epw_base64")
        if not b64:
            raise RuntimeError("Response missing epw_base64 field.")
        path, n = _save(b64, str(SavePath))
        EpwPath = path
        Filename = data.get("filename", os.path.basename(path))
        Metadata = json.dumps({k: v for k, v in data.items() if k != "epw_base64"}, indent=2)
        Status = "OK  " + str(n) + " bytes written to " + path
    except Exception as e:
        Status = "ERROR: " + str(e)
