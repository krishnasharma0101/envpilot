import os
import json
import hashlib
import platform
import sys
from datetime import datetime
from . import scanner

def get_environment_details(env_name_or_path):
    """
    Gathers detailed information about a specific environment.
    """
    # Find the environment
    search_path = os.path.expanduser("~")
    all_envs = scanner.discover_environments(search_path)
    
    target_env = None
    # Check if the input is a direct path
    if os.path.isdir(env_name_or_path):
        env_path = os.path.abspath(env_name_or_path)
        target_env = next((env for env in all_envs if os.path.abspath(env['path']) == env_path), None)
    else: # Assume it's a name
        target_env = next((env for env in all_envs if env['name'] == env_name_or_path), None)

    if not target_env:
        return None, f"Environment '{env_name_or_path}' not found."

    python_executable = target_env["python_executable"]
    installed_packages = scanner.get_installed_packages(python_executable)

    details = {
        "metadata": {
            "source_host": platform.node(),
            "platform": sys.platform,
            "architecture": platform.machine(),
            "python_version": target_env["python_version"],
            "export_timestamp": datetime.utcnow().isoformat() + "Z",
        },
        "packages": installed_packages
    }
    return details, None


def export_environment(env_name, output_path):
    """
    Exports the environment's details to a JSON lock file.
    """
    details, error = get_environment_details(env_name)
    if error:
        return None, error

    # Create a hash for integrity checking
    details_str = json.dumps(details, sort_keys=True)
    hash_signature = hashlib.sha256(details_str.encode('utf-8')).hexdigest()
    
    lock_file_content = {
        "signature": hash_signature,
        "environment": details
    }
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(lock_file_content, f, indent=2)
        return output_path, None
    except IOError as e:
        return None, f"Failed to write to {output_path}: {e}"

def import_environment(lock_file_path, new_env_name):
    """
    Creates a new environment from a lock file.
    """
    try:
        with open(lock_file_path, 'r', encoding='utf-8') as f:
            lock_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        return None, f"Failed to read or parse lock file {lock_file_path}: {e}"

    # TODO: We could add a signature check here for integrity
    
    packages = lock_data.get("environment", {}).get("packages", {})
    if not packages:
        return None, "Lock file contains no packages to install."

    # Create a temporary requirements file from the lock file packages
    temp_req_path = "temp_requirements_from_lock.txt"
    with open(temp_req_path, "w", encoding='utf-8') as f:
        for package, version in packages.items():
            f.write(f"{package}=={version}\n")
    
    # Use the existing manager to create the environment
    # We need to import manager here to avoid circular dependency
    from . import manager
    env_path, error = manager.create_environment(new_env_name, temp_req_path)
    
    # Clean up the temporary file
    os.remove(temp_req_path)
    
    if error:
        return env_path, f"Environment creation from lock file failed. {error}"
        
    return env_path, None 