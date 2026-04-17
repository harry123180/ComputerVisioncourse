# Repository Guidelines

## Project Structure & Module Organization
Day-by-day teaching materials live under `DAY1`-`DAY6`; each day typically owns its own `images/` or `dataset/` and `output/` sub-folder. Shared datasets live in `training_data/` (Front/Back ROI crops) and `video/` (Mediapipe demos), with generated media landing in the root `output/`. Production Python scripts and helpers sit in `tools/` (e.g., `tool04_coin_pipeline.py`, `tool06_roi_capture_advanced.py`), alongside shared assets like `model_coin_classifier.h5` and `model_labels.txt`. Camera calibration images are in `calibration_chessboard/`, course slides in `ppts/`, and onboarding screenshots in `docs/setup_guide/`. When adding modules or datasets, keep them scoped to a single lab folder and note cross-folder dependencies in the README.

## Build, Test, and Development Commands
`python -m venv .venv` and `pip install -r requirements.txt` prepare the full workshop environment (individual days also ship smaller `requirements.txt` where applicable). Run demos with `python tools/tool04_coin_pipeline.py` for coin detection or `python tools/tool01_camera_basic.py` for live capture; execute from the repo root so relative paths resolve. Use `python tools/tool06_roi_capture_advanced.py` to test UI helpers. Automated tests are not yet scaffolded — when you add one, place it under `tools/tests/` using `pytest`.

## Coding Style & Naming Conventions
Target Python 3.10+, use PEP 8 spacing (4 spaces, <=100 characters), and keep filenames, variables, and functions in `lower_snake_case`. Wrap runnable scripts in `if __name__ == "__main__":` blocks, isolate constants in uppercase near the top, and prefer list comprehensions or helper functions over deeply nested loops for image logic.

## Testing Guidelines
Run the script you touched against representative media from the relevant `DAYx/images/`, `training_data/`, or `video/` folder; include before/after screenshots or metrics in your PR. Place automated tests in `tools/tests/` using `pytest`, naming files `test_<module>.py` and asserting measurable outputs (e.g., contour counts, classification confidences). Capture any new asset requirements in comments or docstrings so instructors can replicate sessions quickly.

## Commit & Pull Request Guidelines
Recent commits use short imperative summaries like `update` or `upload`; extend that format with the affected module (e.g., `update roi capture tool`). Separate commits for code, datasets, and presentation decks to ease rollbacks. PRs should describe the teaching goal, list setup or run commands, flag new assets or models, and attach screenshots or logs for visual changes. Request instructor review whenever shared weights or day-level materials change.

## Asset & Configuration Tips
Store large binaries in the existing asset folders and avoid duplicate copies across `DAYx` directories. Keep secrets and API keys out of version control - use a local `.env` and document usage in the PR. When contributing new weights, note their training source and metrics, and prefer release attachments for files larger than a few megabytes.

