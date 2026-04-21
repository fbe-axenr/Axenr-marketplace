---
description: Bump version marketplace.json + plugin.json synchronise selon conventional commits. patch/minor/major/auto.
argument-hint: [patch|minor|major|auto]
---

# /axenr:bump-version

Increment synchronise de la version du marketplace pour que `/plugin update` detecte les nouveautes.

## USAGE

```
/axenr:bump-version          # auto (analyse les commits depuis dernier tag)
/axenr:bump-version patch    # 1.3.0 -> 1.3.1
/axenr:bump-version minor    # 1.3.0 -> 1.4.0
/axenr:bump-version major    # 1.3.0 -> 2.0.0
```

## LOGIQUE AUTO

```
Lire commits depuis dernier tag git :
  git log $(git describe --tags --abbrev=0 2>/dev/null)..HEAD --oneline

- Si un commit contient "BREAKING CHANGE" ou "!" -> major
- Sinon si un commit "feat:" -> minor
- Sinon -> patch
```

## ETAPES

### Etape 1 : Pre-flight

Executer `/axenr:doctor --strict`. Si critical, refuser (sauf --force).

### Etape 2 : Determiner la nouvelle version

- Lire `.claude-plugin/marketplace.json` -> current_version
- Appliquer le type de bump -> new_version

### Etape 3 : Mettre a jour les 2 fichiers

Edit `.claude-plugin/marketplace.json` :
- `"version": "<current>"` -> `"version": "<new>"`
- `plugins[0].version: "<current>"` -> `"<new>"` (pour le plugin axenr)

Edit `plugins/axenr/.claude-plugin/plugin.json` :
- `"version": "<current>"` -> `"version": "<new>"`

Ne PAS toucher la version du plugin axelor partenaire (2.5.0).

### Etape 4 : Commit + tag

```bash
git add .claude-plugin/marketplace.json plugins/axenr/.claude-plugin/plugin.json
GIT_COMMITTER_NAME="fbe-axenr" GIT_COMMITTER_EMAIL="f.benomar@erp-axenr.fr" \
  git commit --author="fbe-axenr <f.benomar@erp-axenr.fr>" \
  -m "chore(release): bump axenr plugin to v<new_version>"
git tag -a "v<new_version>" -m "v<new_version>"
```

### Etape 5 : Push + tag

Demander confirmation avant :

```
git push origin main
git push origin "v<new_version>"
```

### Etape 6 : Notifier l'utilisateur

```
Version bumpee : <current> -> <new>

Pour mettre a jour tes installations Claude Code :

  /plugin marketplace update fbe-axenr-Axenr-marketplace
  /plugin update axenr@fbe-axenr-Axenr-marketplace

Ou tout d'un coup (Claude Code 0.57+) :

  /plugin update --all
```
