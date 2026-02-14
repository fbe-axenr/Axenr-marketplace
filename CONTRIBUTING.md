# Contributing to AxENR Marketplace

Guide pour ajouter de nouveaux agents, skills et commands au marketplace.

---

## Ajouter un Agent

### 1. Creer le fichier

```bash
plugins/axenr/agents/<nom-agent>.md
```

### 2. Structure du fichier

```markdown
# <Nom Agent>

> Description courte

## ROLE
Explication du role de l'agent.

## INPUTS
| Input | Format |
|-------|--------|
| ... | ... |

## WORKFLOW
### PHASE 1 : ...
### PHASE 2 : ...

## CRITICAL RULES
- Regle 1
- Regle 2
```

### 3. Enregistrer dans plugin.json

Editer `plugins/axenr/.claude-plugin/plugin.json` :

```json
{
  "agents": [
    { "name": "existing-agent", "source": "agents/existing-agent.md" },
    { "name": "new-agent", "source": "agents/new-agent.md" }
  ]
}
```

### 4. Incrementer la version

Dans `plugins/axenr/.claude-plugin/plugin.json` ET `.claude-plugin/marketplace.json` :

```json
"version": "1.1.0"
```

---

## Ajouter un Skill

### 1. Creer le dossier et fichier

```bash
mkdir plugins/axenr/skills/<nom-skill>
touch plugins/axenr/skills/<nom-skill>/<nom-skill>.md
```

### 2. Structure du fichier

```markdown
# <Nom Skill>

> Description courte

## ROLE
Explication du role du skill.

## INPUTS
| Input | Format |
|-------|--------|

## OUTPUTS
| Output | Format |
|--------|--------|

## LOGIQUE
1. Etape 1
2. Etape 2

## EXEMPLES
### Cas 1
```

### 3. Enregistrer dans plugin.json

```json
{
  "skills": [
    { "name": "new-skill", "source": "skills/new-skill/new-skill.md" }
  ]
}
```

---

## Ajouter une Command

### 1. Creer le fichier

```bash
plugins/axenr/commands/<nom-command>.md
```

### 2. Structure du fichier

```markdown
Description de ce que fait la commande.

## ARGUMENTS

$ARGUMENTS

Explication du format des arguments.

## WORKFLOW

### STEP 1 : ...
### STEP 2 : ...

## CRITICAL RULES
- ...
```

### 3. Enregistrer dans plugin.json

```json
{
  "commands": [
    { "name": "new-command", "source": "commands/new-command.md" }
  ]
}
```

---

## Conventions

| Element | Convention |
|---------|------------|
| Noms de fichiers | kebab-case |
| Noms d'agents | kebab-case dans plugin.json |
| Documentation | Francais pour user-facing, anglais pour code |
| Code technique | ENGLISH ONLY |
| Commits | Conventional commits en anglais |
| Pas d'emojis | Nulle part dans les fichiers |

## Commits

```bash
feat(agent): add new-agent for X functionality
feat(skill): add new-skill for Y detection
feat(command): add /axenr:new-command
fix(agent): correct ticket-solver retry logic
docs: update README with new command usage
```

## Checklist avant PR

- [ ] Fichier .md cree avec structure correcte
- [ ] Enregistre dans plugin.json
- [ ] Version incrementee dans plugin.json ET marketplace.json
- [ ] Pas d'emojis
- [ ] Noms techniques en anglais
- [ ] Teste localement avec `claude plugin add`
