"""Rebuild the genre catalog and serve the dashboard."""

import os
import subprocess
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

print("Rebuilding genre catalog...")
subprocess.run([sys.executable, "build_catalog.py"], check=True)

port = 8765
print(f"\nServing dashboard at http://localhost:{port}")
print("Press Ctrl+C to stop.\n")
webbrowser.open(f"http://localhost:{port}")
HTTPServer(("", port), SimpleHTTPRequestHandler).serve_forever()
