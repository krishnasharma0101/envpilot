import os
import subprocess
import configparser
import sys

def get_folder_size(path):
    """Calculates the total size of a directory."""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except OSError:
        return 0
    return total_size

def get_python_version(python_executable):
    """Gets the Python version from a Python executable."""
    if not os.path.exists(python_executable):
        return "N/A"
    try:
        result = subprocess.run(
            [python_executable, "--version"],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return result.stdout.strip().split(" ")[-1]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        return "N/A"

def get_package_count(python_executable):
    """Gets the number of installed packages."""
    if not os.path.exists(python_executable):
        return 0
    try:
        pip_path = os.path.join(os.path.dirname(python_executable), 'pip')
        if sys.platform == "win32":
            pip_path += ".exe"

        result = subprocess.run(
            [pip_path, "list"],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        lines = result.stdout.strip().split('\n')
        return max(0, len(lines) - 2)  # Subtract header lines
    except (subprocess.CalledProcessError, FileNotFoundError):
        return 0

def get_installed_packages(python_executable):
    """Gets a dictionary of installed packages and their versions."""
    if not os.path.exists(python_executable):
        return {}
    try:
        pip_path = os.path.join(os.path.dirname(python_executable), 'pip')
        if sys.platform == "win32":
            pip_path += ".exe"

        result = subprocess.run(
            [pip_path, "list"],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        lines = result.stdout.strip().split('\n')[2:]  # Skip header
        packages = {}
        for line in lines:
            try:
                name, version = line.split()
                packages[name.lower()] = version
            except ValueError:
                # Handle cases where the line might not split into two parts
                continue
        return packages
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}

def discover_environments(search_path):
    """Discovers Python virtual environments by looking for pyvenv.cfg files."""
    environments = []
    # Limit walk depth to avoid excessively long scans in deep directories
    search_path_depth = search_path.rstrip(os.path.sep).count(os.path.sep)
    
    # More specific exclusion list to avoid skipping dot-folders like '.venv'
    excluded_dirs = {'.git', '.svn', '.hg', '$Recycle.Bin', 'node_modules', '.vscode', '.idea', '__pycache__'}

    for root, dirs, files in os.walk(search_path, topdown=True):
        # Prune search space
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        if root.count(os.path.sep) > search_path_depth + 5:
            dirs[:] = []
            continue

        if "pyvenv.cfg" in files:
            env_path = root
            
            # Heuristic to avoid detecting environments inside other environments
            if "site-packages" in env_path or ".tox" in env_path:
                dirs[:] = []
                continue

            if sys.platform == "win32":
                python_executable = os.path.join(env_path, "Scripts", "python.exe")
            else:
                python_executable = os.path.join(env_path, "bin", "python")

            if not os.path.exists(python_executable):
                dirs[:] = []
                continue

            version = get_python_version(python_executable)
            size = get_folder_size(env_path)
            package_count = get_package_count(python_executable)

            environments.append({
                "name": os.path.basename(env_path),
                "python_version": version,
                "package_count": package_count,
                "size_mb": size / (1024 * 1024),
                "path": env_path,
                "python_executable": python_executable,
            })
            
            # Don't descend further into the environment directory
            dirs[:] = []
            
    return environments

def find_environment_path(name):
    """
    Finds the path of an environment by name, checking common locations first for speed.
    """
    # 1. Check if the name is a path to an env in the current directory
    potential_path = os.path.join(os.getcwd(), name)
    if os.path.exists(os.path.join(potential_path, "pyvenv.cfg")):
        return potential_path

    # 2. Check the old default creation directory
    legacy_path = os.path.join(os.path.expanduser("~"), ".envpilot-envs", name)
    if os.path.exists(os.path.join(legacy_path, "pyvenv.cfg")):
        return legacy_path

    # 3. If not found, fall back to the slow, full scan
    all_envs = discover_environments(os.path.expanduser("~"))
    found_env = next((env for env in all_envs if env['name'] == name), None)
    
    if found_env:
        return found_env["path"]
        
    return None 