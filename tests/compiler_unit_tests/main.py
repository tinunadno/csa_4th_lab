import sys
import os
import pytest


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

    pytest.main(["-v", "../../"])