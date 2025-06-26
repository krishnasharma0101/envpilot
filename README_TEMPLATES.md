

### **Summary**

This pull request introduces a new **environment template** feature to EnvPilot, allowing users to quickly create Python virtual environments pre-configured with sets of dependencies using simple CLI commands. Templates are defined as YAML files and can include common stacks (such as data science, web development, etc.), making environment setup faster and more reproducible.

### **Feature Details**

- **Environment templates** are YAML files stored in the `templates/` directory.
- Each template specifies a list of Python packages and dependencies.
- The CLI can list available templates and create new environments based on a selected template.
- This feature improves developer productivity and ensures consistent, repeatable setups for common use cases.

### **How to Use**

#### **1. List Available Templates**

```sh
python -m envpilot.cli list-templates
```
This command displays all available environment templates.

#### **2. Create an Environment from a Template**

```sh
python -m envpilot.cli create  --template 
```
- Replace `` with your desired environment name.
- Replace `` with the template you want to use (e.g., `datascience`, `web`, etc.).

**Example:**
```sh
python -m envpilot.cli create myenv --template datascience
```

This will:
- Create a new virtual environment named `myenv`.
- Install all dependencies listed in the `datascience` template (e.g., numpy, pandas, matplotlib, scikit-learn, jupyter).

#### **3. Activate the Environment**

On Windows:
```sh
.\myenv\Scripts\activate
```
On macOS/Linux:
```sh
source myenv/bin/activate
```

### **Why This Is Useful**

- **Fast onboarding:** New contributors or team members can set up their development environment with a single command.
- **Reproducibility:** Ensures everyone uses the same package versions and dependencies.
- **Extensibility:** New templates can be added easily for different stacks or projects.

### **Additional Notes**

- Documentation has been updated in the README to reflect these new commands.
- The feature is backwards compatible; existing CLI commands are unchanged.
- Users can add their own custom templates by creating new YAML files in the `templates/` directory.

