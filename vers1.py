import importlib.metadata
def extract_package_names(requirements_path) -> list:
    packages_names = []
    with open(requirements_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                # Only print if '=' is missing
                if '=' not in line:
                    package_name = line
                    packages_names.append(package_name)
    return packages_names

if __name__ == "__main__":
    req_file = "requirements.txt"
    for pkg in extract_package_names(req_file):
        try:
            version = importlib.metadata.version(pkg)
            print(f"{pkg}=={version}")
        except importlib.metadata.PackageNotFoundError:
            print(f"{pkg} (not installed)")
