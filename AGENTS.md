# Repository Guidelines

## Project Structure & Module Organization
Day-by-day teaching materials live under `DAY1`-`DAY6`; curated datasets are stored in `Front/`, `Back/`, `img/`, and `video/`, with generated media in `output/`. Production Python scripts and helpers sit in `Code/` (e.g., `find_coin.py`, `ctk_tool.py`, `tm.py`), alongside shared assets like `keras_model.h5` and `labels.txt`. When adding modules or datasets, keep them scoped to a single lab folder and note cross-folder dependencies in the README.

## Build, Test, and Development Commands
`python -m venv .venv` and `pip install -r Code/requirements.txt` prepare the workshop environment. Run demos with `python Code/find_coin.py --image img/sample.jpg` for stills or `python Code/opencamera.py` for live capture; execute from the repo root so relative paths resolve. Use `python Code/ctk_tool.py --help` to smoke-test new UI helpers, and reserve `pytest Code/tests` for automated checks you introduce.

## Coding Style & Naming Conventions
Target Python 3.10+, use PEP 8 spacing (4 spaces, <=100 characters), and keep filenames, variables, and functions in `lower_snake_case`. Wrap runnable scripts in `if __name__ == "__main__":` blocks, isolate constants in uppercase near the top, and prefer list comprehensions or helper functions over deeply nested loops for image logic.

## Testing Guidelines
Run the script you touched against representative media from `img/`, `Front/`, or the relevant `DAYx` folder; include before/after screenshots or metrics in your PR. Place automated tests in `Code/tests/` using `pytest`, naming files `test_<module>.py` and asserting measurable outputs (e.g., contour counts, classification confidences). Capture any new asset requirements in comments or docstrings so instructors can replicate sessions quickly.

## Commit & Pull Request Guidelines
Recent commits use short imperative summaries like `update` or `upload`; extend that format with the affected module (e.g., `update ctk tool`). Separate commits for code, datasets, and presentation decks to ease rollbacks. PRs should describe the teaching goal, list setup or run commands, flag new assets or models, and attach screenshots or logs for visual changes. Request instructor review whenever shared weights or day-level materials change.

## Asset & Configuration Tips
Store large binaries in the existing asset folders and avoid duplicate copies across `DAYx` directories. Keep secrets and API keys out of version control - use a local `.env` and document usage in the PR. When contributing new weights, note their training source and metrics, and prefer release attachments for files larger than a few megabytes.

