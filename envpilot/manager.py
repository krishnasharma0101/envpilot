import os
import subprocess
import sys
import venv
from . import scanner

def create_environment(name, requirements_path=None, base_path=None, dependencies=None):
    """
    Creates a new virtual environment and optionally installs packages from requirements.txt
    and/or a list of dependencies (e.g., from a template).
    """
    # Default to the current working directory if no base_path is provided
    if base_path:
        os.makedirs(base_path, exist_ok=True)
        env_path = os.path.join(base_path, name)
    else:
        env_path = os.path.join(os.getcwd(), name)

    if os.path.exists(env_path):
        return None, f"An environment already exists at '{env_path}'."

    try:
        # 1. Create the virtual environment
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(env_path)

        # 2. Determine pip executable path
        if sys.platform == "win32":
            pip_executable = os.path.join(env_path, "Scripts", "pip.exe")
        else:
            pip_executable = os.path.join(env_path, "bin", "pip")

        # 3. Install packages from requirements.txt if provided
        if requirements_path:
            subprocess.run(
                [pip_executable, "install", "-r", requirements_path],
                check=True,
                capture_output=True,
                text=True
            )

        # 4. Install dependencies from template if provided
        if dependencies:
            subprocess.run(
                [pip_executable, "install"] + dependencies,
                check=True,
                capture_output=True,
                text=True
            )

        return env_path, None
    except subprocess.CalledProcessError as e:
        # If installation fails, still return the created env path but with an error
        error_message = f"Environment created but package installation failed: {e.stderr}"
        return env_path, error_message
    except Exception as e:
        return None, f"Failed to create environment: {e}"

def launch_shell(name):
    """
    Launches a new sub-shell with the specified environment activated.
    """
    env_path = scanner.find_environment_path(name)

    if not env_path:
        return f"Environment '{name}' not found."

    try:
        if sys.platform == "win32":
            # For Windows, launch PowerShell with the activation script
            script_path = os.path.join(env_path, "Scripts", "Activate.ps1")
            if not os.path.exists(script_path):
                return f"Activation script not found at {script_path}"
            
            print(f"Launching activated shell for '{name}'. Type 'exit' to leave.")
            subprocess.run(
                ["powershell", "-NoExit", "-Command", f"& '{script_path}'"],
                check=True
            )
        else:
            # For Unix-like systems (Linux, macOS)
            shell = os.environ.get("SHELL", "/bin/bash")
            script_path = os.path.join(env_path, "bin", "activate")
            if not os.path.exists(script_path):
                return f"Activation script not found at {script_path}"
            
            print(f"Launching activated shell for '{name}'. Type 'exit' to leave.")
            # We use execve to replace the current process with the new shell
            # This is a common way to give the user a fully interactive sub-shell
            os.execve(shell, [shell, "--rcfile", script_path], os.environ)

    except Exception as e:
        return f"Failed to launch shell: {e}"
    
    return None  # Should not be reached on success for Unix
