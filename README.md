# AxENR Marketplace

Marketplace interne d'agents auto-apprenants pour le developpement Axelor ERP et React Native mobile.

**Author** : Fadel Benomar - Developer Backend & IA @ AxENR

---

## Installation

### 1. Ajouter le marketplace dans Claude Code

```
/plugin marketplace add fbe-axenr/Axenr-marketplace
```

### 2. Installer le plugin

```
/plugin install axenr@fbe-axenr-Axenr-marketplace
```

### 3. Verifier

```
/plugin
```

Aller sur l'onglet **Installed** pour confirmer.

## Commandes disponibles

| Commande | Description |
|----------|-------------|
| `/axenr:solve-ticket` | Resoudre 1 ticket autonomement |
| `/axenr:solve-batch` | Resoudre 2 tickets en parallele |
| `/axenr:learn-review` | Auditer et consolider les lecons |

## Usage

### Resoudre un ticket

```
/axenr:solve-ticket axenr-app wip #750 | Add estimated power field | decimal field on Opportunity
```

### Resoudre 2 tickets en parallele

```
/axenr:solve-batch axenr-app wip #750|Add power field|decimal on Opportunity ,, #751|Add panel notes|notes panel on SaleOrder form
```

### Format des arguments

```
<project> <branch> #<number> | <title> | <description>
```

| Argument | Description | Exemples |
|----------|-------------|----------|
| project | Nom du projet | `axenr-app`, `axenr-mobile` |
| branch | Branche de travail | `dev`, `wip`, `axenr` |
| number | Numero du ticket | `#750` |
| title | Titre court | `Add estimated power field` |
| description | Description detaillee | `decimal field on Opportunity, calculated from numberOfModules * 400 / 1000` |

## Projets supportes

| Projet | Techno | Branche par defaut |
|--------|--------|--------------------|
| axenr-app | Axelor AOP 7.4.7, Java 11 | dev, wip |
| axenr-mobile | React Native 0.75.5, TypeScript | axenr |

## Architecture

```
axenr-marketplace/
├── plugins/
│   └── axenr/                    # Agents maison AxENR
│       ├── agents/               # ticket-solver-agent
│       ├── skills/               # error-learner, knowledge-updater, pre-flight-checker
│       ├── commands/             # solve-ticket, solve-batch, learn-review
│       ├── docs/lessons/         # LESSONS-LEARNED.md (memoire)
│       └── templates/            # Templates de sortie
├── CLAUDE.md                     # Regles globales
└── README.md
```

## Auto-apprentissage

L'agent apprend de ses erreurs :

1. **Detection** : L'agent valide son code avec les agents Axelor
2. **Correction** : Il corrige les erreurs trouvees (max 3 retries)
3. **Enregistrement** : Chaque erreur est enregistree dans `LESSONS-LEARNED.md` via error-learner
4. **Promotion** : A 3 occurrences d'un pattern, knowledge-updater le promeut dans `CLAUDE.md`
5. **Prevention** : Au prochain ticket, pre-flight-checker charge les lecons pertinentes

## Agents partenaire (Axelor)

Les agents du partenaire sont installes separement via leur propre marketplace :

```
/plugin marketplace add git@git.axelor.com:ia-tools/axelor-claude-marketplace.git
/plugin install axelor
```

### Agents disponibles (18 agents, 32+ skills)

Agents de generation : `domain-agent`, `view-agent`, `java-agent`, `test-agent`

Agents de validation : `code-reviewer`, `code-analyzer`, `axelor-xml-validator`, `axelor-view-semantic-validator`, `axelor-java-style-validator`, `axelor-naming-checker`

## Mise a jour

```
/plugin marketplace update fbe-axenr-Axenr-marketplace
```
