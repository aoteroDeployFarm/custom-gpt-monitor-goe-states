# 🧪 `scraper.py` Usage Guide

The `scraper.py` CLI tool is used to check for updates on government regulatory websites for all 50 U.S. states, supporting flexible filters, exports, and change detection.

---

## 🚀 Basic Usage

```bash
python3 app/scraper.py
````

Scrapes **all URLs across all states** defined in `config/state_urls.json`.

---

## 🏛️ Run by State

```bash
python3 app/scraper.py --state Texas
```

Checks all sites defined for the state of Texas.

---

## 🌐 Run for Specific URL

```bash
python3 app/scraper.py --state Texas --url https://example.com/regulation
```

Checks a **specific URL** and associates it with the state (used for output paths).

---

## 📁 Export Formats

You can export results in the following formats:

### JSON (default)

```bash
python3 app/scraper.py --state Alaska --export json
```

### Markdown

```bash
python3 app/scraper.py --state Alaska --export markdown
```

### CSV

```bash
python3 app/scraper.py --state Alaska --export csv
```

---

## ♻️ Only Updated Results

```bash
python3 app/scraper.py --state California --only-updated --export json
```

Skips writing or reporting unchanged pages.

---

## 🏷️ Filter by Tags

Use `--filter-tag` to limit the scrape to URLs with **specific tags**.

```bash
python3 app/scraper.py --filter-tag air
python3 app/scraper.py --filter-tag air,permits
```

---

## ❌ Exclude Tags

Skip URLs based on tags using `--exclude-tag`.

```bash
python3 app/scraper.py --exclude-tag water
python3 app/scraper.py --exclude-tag air,permits
```

---

## 🔀 Combine Filters

Example: Check all `Texas` URLs with `oil` or `gas`, but **not** `permits`:

```bash
python3 app/scraper.py --state Texas --filter-tag oil,gas --exclude-tag permits
```

---

## 📦 Output Directory Structure

Results are saved into:

```
results/
└── state/
    └── <StateName>/
        ├── json/
        ├── csv/
        ├── markdown/
        ├── diff/
        └── content/
```

Each file includes a timestamp and slug from the URL:

```
results/state/Texas/json/example_com_regulation_2025-08-17T18-55-00Z.json
```

---

## 🧠 Summary of CLI Options

| Option           | Description                                         |
| ---------------- | --------------------------------------------------- |
| `--state`        | Filter by state name (e.g. `Texas`)                 |
| `--url`          | Check a specific URL for changes                    |
| `--export`       | Export format: `json`, `csv`, or `markdown`         |
| `--only-updated` | Only export changed pages                           |
| `--filter-tag`   | Include only URLs with these tags (comma-separated) |
| `--exclude-tag`  | Exclude URLs with these tags (comma-separated)      |

---

## 🧼 Caching

* Hashes of previously scraped content are saved to `.cache/`
* Used to compare changes across runs
* Mapping of hash ➝ URL/state is stored in `mapping.json`

---

## 📥 Requirements

```bash
pip install -r requirements.txt
```

---

## 🧪 Example: Run All & Export Only Air Permits

```bash
python3 app/scraper.py --filter-tag air,permits --only-updated --export markdown
```

---

## 👨‍💻 Contribute or Extend

Feel free to edit `scraper.py` or open an issue/PR to suggest new features!

