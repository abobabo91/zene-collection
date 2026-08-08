"""Újraépíti és kiszolgálja a dashboardot.

Http kell hozzá, nem elég a file:// - az idővonal `fetch()`-csel tölti be a
`genre_catalog.json`-t, amit a böngésző file:// alól CORS miatt megtagad.

    python serve.py            # 8766, böngésző nyílik
    python serve.py --no-build # a begyűjtés kihagyásával
"""

import os
import subprocess
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8766                      # a genre_timeline saját serve.py-ja a 8765-öt használja

if "--no-build" not in sys.argv:
    print("Dashboardok begyűjtése...")
    subprocess.run([sys.executable, os.path.join(HERE, "build.py")], check=True)

os.chdir(HERE)
print(f"\nhttp://localhost:{PORT}\nCtrl+C a leállításhoz.\n")
webbrowser.open(f"http://localhost:{PORT}")
HTTPServer(("", PORT), SimpleHTTPRequestHandler).serve_forever()
