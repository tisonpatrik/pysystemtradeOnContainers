import sys
from importlib import import_module
from pathlib import Path

# Dynamically get the package path
package_path = Path(__file__).parent
package_name = __name__

# Add all `.py` files in the current directory (except __init__.py) to the package namespace
for module_path in package_path.glob("*.py"):
    if module_path.name != "__init__.py" and module_path.suffix == ".py":
        module_name = module_path.stem
        # Import the module dynamically
        imported_module = import_module(f".{module_name}", package_name)
        # Expose the module at the package level
        sys.modules[f"{package_name}.{module_name}"] = imported_module
        sys.modules[module_name] = imported_module  # Makes `import time_series_pb2` work
