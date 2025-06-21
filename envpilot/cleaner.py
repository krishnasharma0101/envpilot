import os
import shutil
from . import scanner

def find_orphaned_environments(environments):
    """
    Identifies environments that are 'orphaned'.
    An environment is considered orphaned if it does not have a .project file 
    linking it to a project directory.
    """
    orphaned = []
    for env in environments:
        project_file = os.path.join(env["path"], ".project")
        if not os.path.exists(project_file):
            orphaned.append(env)
    return orphaned

def remove_environments(environments):
    """
    Removes the specified list of environment directories.
    """
    removed_paths = []
    errors = []
    for env in environments:
        try:
            shutil.rmtree(env["path"])
            removed_paths.append(env["path"])
        except OSError as e:
            errors.append(f"Could not remove {env['path']}: {e}")
    return removed_paths, errors 