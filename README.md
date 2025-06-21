# 🚀 envpilot

**envpilot** is a smart, space-saving, cross-platform Python environment manager. It helps developers **automatically manage, match, clean, and sync** virtual environments — so you spend less time configuring and more time building.

> Think of it as your personal co-pilot for Python virtual environments.

---

## ✨ Features

- 🧭 `envpilot list`: Scan and view all virtual environments on your system.
- 🔍 `envpilot match requirements.txt`: Match existing environments to a requirements file to avoid duplicate env creation.
- ⚙️ `envpilot create <name> [--requirements=req.txt]`: Create a new environment with optional dependencies.
- 🚀 `envpilot activate <name>`: Easily activate a virtual environment.
- 🧹 `envpilot clean`: Remove unused, orphaned, or duplicate environments.
- 🔄 `envpilot sync export`: Export your environment to a lock file for sharing or syncing across devices.
- 📦 `envpilot sync import`: Recreate environments from a `.envpilot-lock.json` file.

---

## 📦 Installation

You can install directly from the GitHub repository:

```bash
pip install git+https://github.com/krishnasharma0101/envpilot.git
```

> Requires Python 3.7+

---

## 🧪 Usage

### 🗂️ List environments
```bash
envpilot list
```

### 🔍 Match requirements
```bash
envpilot match requirements.txt
```

### ⚙️ Create environment
```bash
envpilot create myenv --requirements requirements.txt
```

### 🚀 Activate environment
```bash
envpilot activate myenv
```

### 🧹 Clean up environments
```bash
envpilot clean
```

### 🔄 Export & Import
```bash
envpilot sync export    # Creates .envpilot-lock.json
envpilot sync import    # Rebuilds environment from lock
```

---

## 📁 Folder Structure

```
envpilot/
├── envpilot/                   # Core package folder
│   ├── __init__.py
│   ├── cli.py                  # Main CLI using click or argparse
│   ├── scanner.py              # Scans system for all environments
│   ├── matcher.py              # Matches envs to requirements.txt
│   ├── manager.py              # Env creation, deletion, activation
│   ├── syncer.py               # Export/import environment lock files
│   ├── cleaner.py              # Identifies unused/duplicate envs
│   ├── metadata.py             # Stores env metadata (size, timestamp, link)
│   └── utils.py                # Helpers (file ops, hashing, etc.)
├── tests/
│   ├── test_cli.py
│   ├── test_matcher.py
│   ├── test_scanner.py
│   └── test_syncer.py
├── requirements.txt
├── setup.py
├── pyproject.toml
├── README.md
└── .envpilot/                 # Internal metadata storage for environments
```

---

## 🎯 Goals

- Save disk space by avoiding redundant environments.
- Make environment reuse easy and intelligent.
- Improve cross-machine development reproducibility.
- Provide a minimal, CLI-first experience.

---

## 🧠 Future Scope

- ✅ GUI dashboard for managing environments visually
- ✅ GitHub Action for auto-matching and syncing CI environments
- ✅ AI-enhanced recommendations: Suggest required dependencies by scanning project files or a prompt
- ✅ Remote environment inspector (sync with cloud for viewing all local+remote envs)

---

## 🤝 Contributing

Pull requests are welcome! If you have feature suggestions, bug reports, or want to help build new modules, feel free to open an issue or PR.

---

## 🪪 License

MIT License — use it, build on it, and share it.

---

> Made with 💻 by [Krishna Sharma](https://github.com/krishnasharma0101)
