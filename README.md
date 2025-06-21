# envpilot 🧭

**A unified Python environment manager and synchronizer.**

`envpilot` is a command-line tool that helps you discover, manage, and synchronize Python virtual environments to promote reuse, save disk space, and streamline your development workflow across multiple machines.

---

## Core Features

-   **Discover & List:** Scans your system to find all Python environments.
-   **Intelligent Matching:** Finds the best existing environment for a new project's `requirements.txt`.
-   **Effortless Creation:** Creates new environments in your project directory by default.
-   **Direct Activation:** Instantly launches a fully activated sub-shell.
-   **Cleanup:** Identifies and removes orphaned environments.
-   **Sync & Share:** Exports and imports environment definitions via a portable lock file.

---

## Installation

Ensure you have Python 3.7+ installed. Then, install `envpilot` using pip:

```bash
pip install .
```

To set up for local development, install in editable mode:

```bash
pip install -e .
```

---

## Usage

Below are examples of the core commands. For detailed options on any command, run `envpilot <command> -h`.

### `envpilot list`
Scan and list all Python environments found on your system.

```bash
envpilot list
```
![list command output](https://i.imgur.com/example.png) <!-- Placeholder -->

### `envpilot create [NAME]`
Create a new virtual environment. By default, it creates a `venv` folder in the current directory.

```bash
# Create 'venv' in the current directory
envpilot create

# Create an environment named 'my-app-env'
envpilot create my-app-env

# Create an environment and install packages from a file
envpilot create -r requirements.txt
```

### `envpilot activate <NAME>`
Launch a new, activated shell for the specified environment.

```bash
envpilot activate my-app-env
```
This will drop you into a new shell with the environment active: `(my-app-env) PS C:\>`. Type `exit` to leave.

### `envpilot match <REQUIREMENTS_FILE>`
Find the best existing environment for a project's requirements.

```bash
envpilot match requirements.txt

# Match against a single, specific environment
envpilot match requirements.txt --env my-app-env
```
![match command output](https://i.imgur.com/example.png) <!-- Placeholder -->

### `envpilot clean`
Find and remove orphaned environments to save space.

```bash
# See which environments would be removed
envpilot clean --dry-run

# Remove them after confirming
envpilot clean
```

### `envpilot sync`
Export and import environment configurations using a lock file.

```bash
# Export 'my-app-env' to a lock file
envpilot sync export my-app-env -f my-app.lock

# Create a new environment from the lock file
envpilot sync import my-app.lock new-app-from-lock
```

---

## Contributing

Contributions are welcome! Please see the `CONTRIBUTING.md` file for details on how to get started.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details. 