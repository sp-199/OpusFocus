"""Start the OpusFocus MCP server over stdio. MCP hosts launch this file by its full path:
    OPUSFOCUS_USER=u-nino python /path/to/OpusFocus/serve.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.mcp_server import mcp  # noqa: E402

if __name__ == "__main__":
    mcp.run()
