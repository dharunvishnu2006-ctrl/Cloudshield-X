# 🛡️ CloudShield X — Server Log Security Analyzer

> Enterprise-grade CSPM platform built from scratch in Python.
> v1.0 shipped in 3 days. v1.1 closed the audit: 80/80 steps built,
> 3 real bugs fixed.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![pytest](https://img.shields.io/badge/pytest-21%20tests-yellow)
![bandit](https://img.shields.io/badge/bandit-clean-brightgreen)

## 🚀 Live Demo
**[Try it live →](https://cloudshield-x-v1-4rdy68whxptnf6whzzrdrd.streamlit.app)**

## 📖 The Honest Story

v1.0 shipped in 3 days — 5 features, 5 tests, deployed.
But its range was 80 roadmap steps and it used 25.

I audited my own work, found that, and closed it in v1.1.
The audit also found 3 real bugs:

| # | Bug | Fix |
|---|-----|-----|
| 1 | `split()` broke on quoted fields | Compiled regex with named groups |
| 2 | Memory-only — restart lost everything | SQLite persistence |
| 3 | `print()` instead of logging | Structured JSON logging + run_id |

## ✨ Features — v1.1 (80/80 steps)

**Foundation (v1.0):**
- Log File Reader — File I/O, error handling
- Suspicious IP Detector — threshold-based counting
- Alert System — testable, typed alerts
- CSV Report Generator — Pandas DataFrame
- Streamlit Dashboard — upload, scan, download

**Completion (v1.1):**
- Pydantic validation — bad data rejected at parse boundary
- Regex parser — handles real Apache/nginx logs
- SQLite database — history survives restart
- OOP detector hierarchy — polymorphic, extensible
- NumPy/Pandas analytics — p95 data-driven threshold
- Plotly + Seaborn charts — interactive dashboard
- Threat intel feeds — external reputation API
- Flask alert API — `GET /alerts`, `GET /health`
- Pre-commit hooks — black, flake8, mypy, bandit clean
- LLM summaries — verified, never fabricated

## 📊 Results (measured, not guessed)

- Parser: split() vs regex — disagreed on real log lines
- Tests: 5 (v1.0) → 21 (v1.1)
- Steps: 25 (v1.0) → 80/80 (v1.1)
- Security: 0 bandit findings

## 🏗️ Architecture
Log File → Reader (generator) → Parser (regex) → Validator (Pydantic)
↓
Detectors (polymorphic)
↓
SQLite Store → Flask API
↓
Streamlit Dashboard

## 🔧 Tech Stack

Python 3.14 · Pydantic · NumPy · Pandas · Matplotlib · Seaborn ·
Plotly · SQLite · Flask · Streamlit · pytest · black · flake8 ·
mypy · bandit · pre-commit

## 💻 How to Run

```bash
git clone https://github.com/dharunvishnu2006-ctrl/Cloudshield-X.git
cd Cloudshield-X
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 🧪 Tests

```bash
python -m pytest tests/ -v
# 21 tests — all passing
```

## 🗺️ Roadmap

<!-- VERSIONS_TABLE_START -->
| Version | Status | Steps | Tests | Description |
|---------|--------|-------|-------|-------------|
| **v1.0** | ✅ Shipped | 1-80 | 5 | Foundation — 3-day sprint |
| **v1.1** | ✅ Shipped | 1-80 | 25 | Completion — all 80 steps built |
| **v2** | 🔜 Planned | 81-153 | — | Threat Intelligence — DSA + SQL |
| **v3** | 🔜 Planned | 154-240 | — | Statistics Engine — Maths + ML start |
| **v4** | 🔜 Planned | 241-373 | — | ML, FastAPI, Docker |
| **v5** | 🔜 Planned | 374-500 | — | Deep Learning, GenAI Agents |
| **v6** | 🔜 Planned | 501-600 | — | MLOps, Kubernetes, Monitoring |
<!-- VERSIONS_TABLE_END -->

[View Architecture](docs/architecture.png) · [View Evolution Map](docs/evolution.png) · [Decision Records](docs/adr/)

## 👤 Author

**J. Dharun Vishnu**
[GitHub](https://github.com/dharunvishnu2006-ctrl)