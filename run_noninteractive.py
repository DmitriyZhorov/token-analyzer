"""
Non-interactive wrapper for Token-Craft skill handler.
"""
import sys
from pathlib import Path

# Add token_craft to path
sys.path.insert(0, str(Path(__file__).parent))

from skill_handler import TokenCraftHandler
import io

# Fix Windows CMD encoding issues
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Get mode from command line, default to 'full'
mode = sys.argv[1] if len(sys.argv) > 1 else 'full'

# Run analysis
handler = TokenCraftHandler()
report = handler.run(mode=mode)
print(report)
