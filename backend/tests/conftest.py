import os
import sys

# component_extractor.py etc. live directly under backend/, not as an installed package —
# make sure backend/ is importable regardless of which directory pytest is invoked from.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
