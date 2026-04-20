#!/bin/bash
# Lance le serveur de dev pour Ça Swingue 3 (version évolutions)
cd "$(dirname "$0")/site"
echo "🚀 Ça Swingue 3 — http://localhost:8093/golf_manager.html"
python3 -m http.server 8093
