import os

# Define app directory structure
APP_NAME = "real-estate-app"
APP_DIR = os.path.join(os.getcwd(), APP_NAME)
SERVICES_DIR = os.path.join(APP_DIR, "services")
MODELS_DIR = os.path.join(APP_DIR, "models")
UTILS_DIR = os.path.join(APP_DIR, "utils")
TESTS_DIR = os.path.join(APP_DIR, "tests")

DIRECTORIES = [APP_DIR, SERVICES_DIR, MODELS_DIR, UTILS_DIR, TESTS_DIR]
SERVICE_NAMES = ["auth", "investor", "property", "event", "preapprove", "approve"]
MODEL_NAMES = [
    "user",
    "bank_account",
    "investor",
    "property",
    "event",
    "investment",
    "book_of_records",
    "notification",
    "portfolio",
]
UTILS_NAMES = ["metrics", "logging"]
FILES = {
    "__init__.py": "",
    "config.py": "",
    "database.py": "",
    "main.py": "",
}

# Create directories
for directory in DIRECTORIES:
    os.makedirs(directory, exist_ok=True)

# Create service files
for service_name in SERVICE_NAMES:
    service_file = os.path.join(SERVICES_DIR, f"{service_name}.py")
    with open(service_file, "w") as f:
        f.write(f"# {service_name.capitalize()} service code\n")

# Create model files
for model_name in MODEL_NAMES:
    model_file = os.path.join(MODELS_DIR, f"{model_name}.py")
    with open(model_file, "w") as f:
        f.write(f"# {model_name.capitalize()} model code\n")

# Create utils files
for utils_name in UTILS_NAMES:
    utils_file = os.path.join(UTILS_DIR, f"{utils_name}.py")
    with open(utils_file, "w") as f:
        f.write(f"# {utils_name.capitalize()} utility code\n")

# Create main app files
for filename, contents in FILES.items():
    filepath = os.path.join(APP_DIR, filename)
    with open(filepath, "w") as f:
        f.write(contents)

# Create test files
with open(os.path.join(TESTS_DIR, "__init__.py"), "w") as f:
    f.write("# Test initialization code\n")

# Print success message
print("App directory structure created successfully.")
