import sys
import os
import pytest

@pytest.fixture(scope="session", autouse=True)
def adjust_sys_path():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    print(f"Adjusted sys.path: {sys.path}")
