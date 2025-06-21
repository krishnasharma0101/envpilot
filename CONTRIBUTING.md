# Contributing to envpilot

First off, thank you for considering contributing to `envpilot`! Any contribution, no matter how small, is welcome and appreciated.

## How to Contribute

### Reporting Bugs
If you find a bug, please open an issue on the GitHub repository. When you report a bug, please include:
- Your operating system and Python version.
- The version of `envpilot` you are using.
- Steps to reproduce the bug.
- The full output of the command, including any errors.

### Suggesting Enhancements
If you have an idea for a new feature or an improvement, please open an issue to discuss it. This allows us to coordinate efforts and ensure the feature aligns with the project's goals.

### Submitting Pull Requests
1.  Fork the repository and create your branch from `main`.
2.  Set up your development environment:
    ```bash
    # Create a virtual environment
    python -m venv venv
    
    # Activate it
    # On Windows (PowerShell)
    . .\venv\Scripts\Activate.ps1
    # On macOS/Linux
    source venv/bin/activate
    
    # Install the project in editable mode with dev dependencies
    pip install -e .
    ```
3.  Make your changes. Ensure your code follows the existing style.
4.  (Optional, once tests are added) Make sure the test suite passes.
5.  Add a clear and concise description of your changes to the pull request.

Thank you for helping to make `envpilot` a better tool! 