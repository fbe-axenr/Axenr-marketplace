#!/usr/bin/env python3
"""
Détection automatique des chemins AOP/AOS/Addons.
Utilisé par le workflow /develop pour configurer l'accès aux repos.

Usage:
    python3 detect_axelor_repos.py                      # Auto-detect or prompt
    python3 detect_axelor_repos.py --no-prompt          # Auto-detect only, no prompt
    python3 detect_axelor_repos.py /path/to/repo        # Use provided path

Detection Priority:
    1. Provided path parameter (absolute priority)
    2. .axelor/ in working directory (NEW - project-local)
    3. /opt/axelor/ (legacy fallback)
    4. User prompt (if allowed)
"""

import sys
import os
from pathlib import Path
import json
import argparse


def check_axelor_dir_structure(working_dir=None):
    """
    Check if .axelor/ directory exists in working directory with required structure.

    The .axelor/ directory uses a FLAT structure (no addons/ subdirectory):
    .axelor/
    ├── aop/
    ├── aos/
    ├── axelor-utils/      (not addons/axelor-utils)
    ├── axelor-message/
    └── axelor-studio/

    Returns:
        str: Path to .axelor/ if valid, None otherwise
    """
    if working_dir is None:
        working_dir = os.getcwd()

    axelor_dir = Path(working_dir) / ".axelor"
    if not axelor_dir.exists():
        return None

    # Required directories (at minimum aop/ and aos/)
    required_dirs = ['aop', 'aos']
    if not all((axelor_dir / dir_name).exists() for dir_name in required_dirs):
        return None

    return str(axelor_dir.resolve())


def build_paths_from_axelor_dir(axelor_path, detection_method):
    """
    Build paths structure from .axelor/ directory (flat structure).

    .axelor/ uses a FLAT structure where addons are at root level:
    - .axelor/axelor-message/ (NOT .axelor/addons/axelor-message/)
    - .axelor/axelor-studio/
    - .axelor/axelor-utils/
    """
    axelor_path = Path(axelor_path)

    # Build addon paths (flat structure - addons at root level)
    addons = {}
    addon_names = {
        'message': 'axelor-message',
        'studio': 'axelor-studio',
        'utils': 'axelor-utils'
    }

    for key, addon_name in addon_names.items():
        addon_path = axelor_path / addon_name
        if addon_path.exists():
            addons[key] = str(addon_path)
        else:
            addons[key] = None

    return {
        "axelor_repo": str(axelor_path),
        "detection_method": detection_method,
        "paths": {
            "aop": str(axelor_path / "aop"),
            "aos": str(axelor_path / "aos"),
            "addons": addons
        }
    }


def check_default_structure(base_path="/opt/axelor"):
    """Vérifie si le chemin par défaut contient aop/, aos/, et addons/"""
    axelor_path = Path(base_path)
    if not axelor_path.exists():
        return False

    required_dirs = ['aop', 'aos', 'addons']
    return all((axelor_path / dir_name).exists() for dir_name in required_dirs)

def validate_repo_structure(repo_path):
    """Valide que le repo contient les 3 sous-dossiers requis"""
    repo = Path(repo_path)
    if not repo.exists():
        return None, f"Le chemin {repo_path} n'existe pas"

    required_dirs = ['aop', 'aos', 'addons']
    missing_dirs = [d for d in required_dirs if not (repo / d).exists()]

    if missing_dirs:
        return None, f"Dossiers manquants: {', '.join(missing_dirs)}"

    return str(repo.resolve()), None

def prompt_user_for_repo():
    """Demande à l'utilisateur de fournir un repo path"""
    print("\n⚠️  Les dossiers AOP/AOS/Addons ne sont pas trouvés dans /opt/axelor/", file=sys.stderr)
    print("Veuillez fournir le chemin vers un répertoire contenant les 3 sous-dossiers:", file=sys.stderr)
    print("  - aop/", file=sys.stderr)
    print("  - aos/", file=sys.stderr)
    print("  - addons/", file=sys.stderr)
    print(file=sys.stderr)

    repo_path = input("Chemin du repo: ").strip()
    return validate_repo_structure(repo_path)

def build_paths_from_repo(repo_path, detection_method):
    """Construit la structure de chemins depuis un repo"""
    return {
        "axelor_repo": str(repo_path),
        "detection_method": detection_method,
        "paths": {
            "aop": f"{repo_path}/aop",
            "aos": f"{repo_path}/aos",
            "addons": {
                "message": f"{repo_path}/addons/axelor-message",
                "studio": f"{repo_path}/addons/axelor-studio",
                "utils": f"{repo_path}/addons/axelor-utils"
            }
        }
    }

def detect_axelor_repos(provided_path=None, allow_prompt=True, working_dir=None):
    """
    Détecte l'emplacement des repos AOP/AOS/Addons.

    Priorités:
    1. Chemin fourni en paramètre (si fourni)
    2. .axelor/ dans le répertoire de travail (projet local)
    3. /opt/axelor/ (fallback legacy)
    4. Mode interactif (prompt utilisateur) - seulement si allow_prompt=True

    Args:
        provided_path: Chemin optionnel fourni par l'utilisateur
        allow_prompt: Si False, retourne une erreur au lieu de demander à l'utilisateur
        working_dir: Répertoire de travail pour chercher .axelor/ (défaut: cwd)

    Returns:
        dict: Structure avec axelor_repo, detection_method, et paths
    """

    # ============================================
    # PRIORITÉ 1: Chemin fourni en paramètre
    # ============================================
    if provided_path:
        repo_path, error = validate_repo_structure(provided_path)
        if error:
            return {
                "axelor_repo": None,
                "detection_method": "error",
                "error": f"Chemin fourni invalide: {error}",
                "paths": None
            }
        return build_paths_from_repo(repo_path, "parameter")

    # ============================================
    # PRIORITÉ 2: .axelor/ dans le répertoire de travail
    # ============================================
    axelor_dir = check_axelor_dir_structure(working_dir)
    if axelor_dir:
        return build_paths_from_axelor_dir(axelor_dir, "local-axelor-dir")

    # ============================================
    # PRIORITÉ 3: Répertoire legacy /opt/axelor/
    # ============================================
    if check_default_structure("/opt/axelor"):
        return build_paths_from_repo("/opt/axelor", "legacy-opt")

    # ============================================
    # PRIORITÉ 4: Mode interactif (seulement si allow_prompt=True)
    # ============================================
    if not allow_prompt:
        return {
            "axelor_repo": None,
            "detection_method": "not_found",
            "error": "Aucun repo détecté. Exécutez /axelor:setup ou fournissez un chemin.",
            "paths": None
        }

    print("ℹ️  Mode interactif: aucune configuration automatique trouvée", file=sys.stderr)
    repo_path, error = prompt_user_for_repo()

    if error:
        return {
            "axelor_repo": None,
            "detection_method": "error",
            "error": error,
            "paths": None
        }

    return build_paths_from_repo(repo_path, "user-prompt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Détecte l'emplacement des repos AOP/AOS/Addons"
    )
    parser.add_argument(
        'repo_path',
        nargs='?',
        default=None,
        help="Chemin optionnel vers le repo contenant aop/, aos/, addons/"
    )
    parser.add_argument(
        '--no-prompt',
        action='store_true',
        help="Ne pas demander à l'utilisateur si la détection échoue"
    )

    args = parser.parse_args()
    result = detect_axelor_repos(
        provided_path=args.repo_path,
        allow_prompt=not args.no_prompt
    )
    print(json.dumps(result, indent=2))
