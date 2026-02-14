#!/usr/bin/env python3
"""
SessionStart hook pour détecter les repos Axelor.
Injecte les chemins AOP/AOS/Addons comme variables d'environnement.

Ce hook est exécuté au démarrage de chaque session Claude Code.
Il détecte automatiquement les chemins et les persiste via $CLAUDE_ENV_FILE.
"""
import json
import sys
import os
import subprocess
from pathlib import Path


def main():
    # Lire l'entrée du hook (JSON sur stdin)
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}

    # Trouver le script de détection (même répertoire)
    script_dir = Path(__file__).parent
    detect_script = script_dir / "detect_axelor_repos.py"

    if not detect_script.exists():
        print("Script detect_axelor_repos.py non trouve", file=sys.stderr)
        sys.exit(0)  # Non-bloquant

    # Exécuter la détection (mode non-interactif)
    try:
        result = subprocess.run(
            ["python3", str(detect_script), "--no-prompt"],
            capture_output=True,
            text=True,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        print("Timeout lors de la detection Axelor", file=sys.stderr)
        sys.exit(0)

    # Parser le résultat JSON
    try:
        repos = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Erreur parsing detection Axelor", file=sys.stderr)
        sys.exit(0)

    # Vérifier si détection réussie
    detection_method = repos.get("detection_method", "error")

    if detection_method in ("not_found", "error"):
        # Injecter un message dans le contexte Claude (stdout)
        print("AXELOR_SETUP_REQUIRED: Les repos AOP/AOS/Addons n'ont pas ete detectes.")
        print("Veuillez indiquer le chemin vers votre repertoire Axelor contenant:")
        print("  - aop/")
        print("  - aos/")
        print("  - addons/")
        print("")
        print("Exemple: /home/user/axelor ou /opt/axelor-custom")
        print("")
        print("Une fois le chemin fourni, vous pouvez configurer manuellement:")
        print("  export AXELOR_REPO=/chemin/vers/axelor")
        print("  export AXELOR_AOP_PATH=/chemin/vers/axelor/aop")
        print("  export AXELOR_AOS_PATH=/chemin/vers/axelor/aos")
        sys.exit(0)

    # Écrire les variables d'environnement dans $CLAUDE_ENV_FILE
    env_file = os.getenv("CLAUDE_ENV_FILE")
    if env_file:
        try:
            with open(env_file, "a") as f:
                f.write(f'export AXELOR_REPO="{repos["axelor_repo"]}"\n')
                f.write(f'export AXELOR_AOP_PATH="{repos["paths"]["aop"]}"\n')
                f.write(f'export AXELOR_AOS_PATH="{repos["paths"]["aos"]}"\n')

                # Addons individuels
                addons = repos["paths"]["addons"]
                f.write(f'export AXELOR_ADDONS_MESSAGE="{addons["message"]}"\n')
                f.write(f'export AXELOR_ADDONS_STUDIO="{addons["studio"]}"\n')
                f.write(f'export AXELOR_ADDONS_UTILS="{addons["utils"]}"\n')
        except IOError as e:
            print(f"Erreur ecriture env file: {e}", file=sys.stderr)

    # Afficher le contexte pour Claude (stdout = injecté dans le contexte)
    print(f"Axelor repos detectes ({detection_method}):")
    print(f"  - AXELOR_REPO={repos['axelor_repo']}")
    print(f"  - AXELOR_AOP_PATH={repos['paths']['aop']}")
    print(f"  - AXELOR_AOS_PATH={repos['paths']['aos']}")
    print(f"  - Addons: {repos['axelor_repo']}/addons")

    sys.exit(0)


if __name__ == "__main__":
    main()
