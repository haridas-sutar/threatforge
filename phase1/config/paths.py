from pathlib import Path

# Project root directory (phase1)
PROJECT_ROOT = Path(__file__).parent.parent

# Important directories
SCANNER_DIR = PROJECT_ROOT / "scanner"
RESULTS_DIR = PROJECT_ROOT / "results"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
CONFIG_DIR = PROJECT_ROOT / "config"

# Important files
ENHANCED_SCANNER = SCANNER_DIR / "enhanced_scanner.py"
BASIC_SCANNER = SCANNER_DIR / "basic_scanner.py"
