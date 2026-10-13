# Flight Telemetry Analyzer

Upload flight CSV logs, inspect altitude, airspeed, battery and vertical-speed plots, flag configurable threshold violations and export results.

## Quick start

Python 3.12 recommended. Run commands inside this repository.

```sh
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Validation

```sh
python -m unittest discover -v
```

## Model and limitations

Required CSV columns: `time_s`, `altitude_m`, `airspeed_ms`, `battery_pct`. Time must strictly increase; values must be finite. Battery is 0–100 percent. Vertical speed uses a numerical gradient on actual sample timestamps. The built-in flight is synthetic. Thresholds are user-defined and are not regulatory limits.

## Repository structure

- `core.py`: numerical/data processing functions
- `app.py`: interactive Streamlit interface
- `test_core.py`: checks for model behavior and invalid input

## Development

Built with AI assistance. Model assumptions and validation are documented so the implementation can be reviewed and extended.
