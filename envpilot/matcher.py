import os
import sys
from packaging.requirements import Requirement
from packaging.version import Version, InvalidVersion
from . import scanner

def parse_requirements(file_path):
    """Parses a requirements.txt file into a list of Requirement objects."""
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    reqs = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            try:
                reqs.append(Requirement(line))
            except Exception:
                # Ignore invalid requirement lines for now
                pass
    return reqs

def calculate_match(required_packages, installed_packages):
    """
    Calculates how well an environment matches requirements.
    Returns: (match_percentage, missing_packages, extra_packages_count)
    """
    if not required_packages:
        return (100.0, [], len(installed_packages))

    matched_count = 0
    missing_packages_specs = []
    
    installed_map = {name.lower(): version for name, version in installed_packages.items()}
    
    for req in required_packages:
        req_name_lower = req.name.lower()
        if req_name_lower in installed_map:
            installed_version_str = installed_map[req_name_lower]
            try:
                installed_version = Version(installed_version_str)
                if req.specifier.contains(installed_version, prereleases=True):
                    matched_count += 1
                else:
                    missing_packages_specs.append(f"{req.name} (found {installed_version}, need {req.specifier})")
            except InvalidVersion:
                 # If version is not parsable (e.g., from a VCS url), we can't check specifiers.
                 # A simple check for existence is the best we can do.
                 matched_count += 1
        else:
            missing_packages_specs.append(str(req))
            
    match_percentage = (matched_count / len(required_packages)) * 100
    
    required_names = {req.name.lower() for req in required_packages}
    extra_packages_count = len(installed_map.keys() - required_names)

    return (match_percentage, missing_packages_specs, extra_packages_count)

def find_best_matches(requirements_path, env_name=None):
    """
    Finds and ranks environments based on a requirements file.
    If env_name is provided, only that environment is checked.
    """
    required_packages = parse_requirements(requirements_path)
    if not required_packages:
        return None, "Could not parse requirements file or file is empty."

    search_path = os.path.expanduser("~")
    all_environments = scanner.discover_environments(search_path)
    
    environments_to_check = []
    if env_name:
        found_env = next((env for env in all_environments if env['name'] == env_name), None)
        if not found_env:
            return None, f"Environment '{env_name}' not found."
        environments_to_check.append(found_env)
    else:
        environments_to_check = all_environments

    matches = []
    for env in environments_to_check:
        installed_packages = scanner.get_installed_packages(env["python_executable"])
        # No need to check environments with no packages installed.
        if not installed_packages and not required_packages:
            continue

        match_percentage, missing, extra = calculate_match(required_packages, installed_packages)
        
        # Scoring: higher percentage is better, fewer extra packages is a tie-breaker.
        score = match_percentage - (extra * 0.1)

        matches.append({
            "env": env,
            "match_percentage": match_percentage,
            "missing_packages": missing,
            "extra_packages_count": extra,
            "score": score,
        })
            
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches, None 