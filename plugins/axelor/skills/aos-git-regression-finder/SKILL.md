# Skill: AOS Git Regression Finder

## Objectif

Identifier l'origine d'une régression en analysant l'historique Git du code source Axelor. Ce skill recherche les commits suspects qui ont pu introduire le bug, en se basant sur les fichiers/méthodes identifiés dans l'analyse du ticket.

## Entrée Requise

| Paramètre | Description | Obligatoire |
|-----------|-------------|-------------|
| `aos_path` | Chemin vers le repository AOS | Oui |
| `suspect_files` | Liste des fichiers suspects (services, entités) | Oui |
| `suspect_methods` | Liste des méthodes suspectes | Non |
| `date_range` | Plage de dates à analyser (ex: "6 months") | Non (défaut: 1 an) |
| `ticket_date` | Date de création du ticket (pour borner la recherche) | Non |

## Processus

### Étape 1: Identification des Fichiers Cibles

À partir des informations du ticket, construire la liste des fichiers à analyser :

```bash
# Exemple pour CostSheetServiceBusinessImpl
aos_path="/path/to/axelor-open-suite"
file_pattern="**/CostSheetServiceBusinessImpl.java"

# Trouver le fichier exact
find $aos_path -name "CostSheetServiceBusinessImpl.java" -type f
```

### Étape 2: Analyse Git Log

Pour chaque fichier suspect, récupérer l'historique des modifications :

```bash
cd $aos_path

# Historique des commits sur le fichier
git log --oneline --since="1 year ago" --follow -- "path/to/file.java"

# Avec plus de détails
git log --pretty=format:"%h|%ad|%an|%s" --date=short --since="1 year ago" -- "path/to/file.java"
```

### Étape 3: Git Blame sur les Lignes Suspectes

Si des numéros de ligne sont fournis :

```bash
# Blame sur une plage de lignes
git blame -L 85,105 path/to/CostSheetServiceBusinessImpl.java

# Format pour parsing
git blame -L 85,105 --line-porcelain path/to/file.java | grep -E "^(author|author-time|summary|filename)"
```

### Étape 4: Analyse des Commits Suspects

Pour chaque commit identifié, récupérer :

```bash
# Détails du commit
git show --stat <commit_hash>

# Message complet
git log -1 --format="%B" <commit_hash>

# Fichiers modifiés dans le même commit
git diff-tree --no-commit-id --name-only -r <commit_hash>

# Recherche de références à des tickets
git log -1 --format="%B" <commit_hash> | grep -Eo "#[0-9]+"
```

### Étape 5: Corrélation avec le Ticket

Analyser si le commit est lié au bug :

1. **Date du commit** vs **Date de signalement** : Le bug est-il apparu après ce commit ?
2. **Auteur** : Qui contacter pour plus d'infos ?
3. **Message de commit** : Mentionne-t-il un ticket Redmine ?
4. **Fichiers associés** : Autres fichiers modifiés en même temps ?

## Format de Sortie

```json
{
  "regression_analysis": {
    "search_scope": {
      "repository": "/path/to/axelor-open-suite",
      "files_analyzed": ["CostSheetServiceBusinessImpl.java"],
      "date_range": "2024-01-01 to 2025-11-24",
      "lines_blamed": [87, 91, 101]
    },

    "suspect_commits": [
      {
        "hash": "abc1234",
        "short_hash": "abc1234",
        "date": "2024-06-15",
        "author": "John Doe",
        "author_email": "john.doe@axelor.com",
        "message": "fix: improve cost calculation performance",
        "full_message": "fix: improve cost calculation performance\n\nOptimized the duration calculation to use seconds instead of hours.\n\nCloses #98765",
        "files_changed": [
          "axelor-business-production/src/main/java/.../CostSheetServiceBusinessImpl.java",
          "axelor-production/src/main/java/.../CostSheetService.java"
        ],
        "lines_modified": {
          "CostSheetServiceBusinessImpl.java": [85, 87, 91, 101, 105]
        },
        "related_tickets": ["#98765"],
        "confidence": 85,
        "confidence_reason": "Commit modifies exact lines mentioned in bug report, date matches regression window"
      },
      {
        "hash": "def5678",
        "date": "2024-05-20",
        "author": "Jane Smith",
        "message": "refactor: extract date calculation to utility",
        "confidence": 45,
        "confidence_reason": "Modifies related code but not the exact lines"
      }
    ],

    "most_likely_cause": {
      "commit": "abc1234",
      "confidence": 85,
      "evidence": [
        "Modifies lines 87, 91, 101 - exact lines from bug report",
        "Commit message mentions 'duration calculation' - matches bug description",
        "Date (2024-06-15) is before ticket creation (2025-11-20)",
        "Same author worked on related CostSheetService"
      ],
      "recommendation": "Review commit abc1234 - likely introduced the date order and duration unit bugs"
    },

    "blame_details": [
      {
        "file": "CostSheetServiceBusinessImpl.java",
        "line": 87,
        "commit": "abc1234",
        "author": "John Doe",
        "date": "2024-06-15",
        "code": "previousCostSheetDate, parentCostSheetLine.getCostSheet().getCalculationDate()"
      },
      {
        "file": "CostSheetServiceBusinessImpl.java",
        "line": 91,
        "commit": "abc1234",
        "author": "John Doe",
        "date": "2024-06-15",
        "code": "duration = timesheetLineList.stream()..."
      }
    ],

    "timeline": [
      {"date": "2024-05-20", "event": "commit def5678 - refactor date utility"},
      {"date": "2024-06-15", "event": "commit abc1234 - LIKELY REGRESSION INTRODUCED"},
      {"date": "2024-07-01", "event": "release v8.0.0"},
      {"date": "2025-11-20", "event": "ticket #100040 created - bug reported"}
    ],

    "contacts": [
      {
        "name": "John Doe",
        "email": "john.doe@axelor.com",
        "role": "Primary suspect commit author",
        "commits_on_file": 5
      }
    ]
  }
}
```

## Calcul du Score de Confiance

Le score de confiance (0-100) est calculé ainsi :

| Critère | Points |
|---------|--------|
| Modifie les lignes exactes mentionnées | +30 |
| Date du commit < date du ticket | +20 |
| Message de commit mentionne fonctionnalité liée | +15 |
| Modifie plusieurs fichiers liés au scope | +10 |
| Commit récent (< 6 mois avant ticket) | +10 |
| Auteur a d'autres commits sur le fichier | +5 |
| Commit référence un ticket Redmine | +10 |

## Commandes Git Utiles

```bash
# Historique d'un fichier avec stats
git log --stat --follow -- "path/to/file.java"

# Blame avec date ISO
git blame --date=iso -L 80,110 "path/to/file.java"

# Commits entre deux dates
git log --after="2024-01-01" --before="2024-12-31" -- "path/to/file.java"

# Recherche dans les messages de commit
git log --grep="CostSheet" --oneline

# Trouver quand une ligne a été ajoutée
git log -S "previousCostSheetDate" --oneline -- "*.java"

# Diff entre deux commits
git diff abc1234..def5678 -- "path/to/file.java"

# Commits d'un auteur sur un fichier
git log --author="John Doe" -- "path/to/file.java"
```

## Intégration avec ticket-deep-analyzer

Ce skill est appelé comme **Étape 12** après l'identification des fichiers suspects :

```yaml
# Dans ticket-deep-analyzer, après bug_analysis
git_regression_search:
  trigger: bug_analysis.root_cause_analysis exists
  inputs:
    aos_path: "{aos_path}"
    suspect_files: bug_analysis.root_cause_analysis[].location
    suspect_methods: bug_analysis.root_cause_analysis[].method
    ticket_date: metadata.created_at
```

## Outils Requis

- `Bash`: Exécution des commandes Git
- `Grep`: Parsing des résultats
- `Read`: Lecture des fichiers de code

## Limitations

1. **Repository local requis** : Le path AOS doit pointer vers un repo Git cloné
2. **Historique disponible** : Dépend de la profondeur de l'historique Git
3. **Performance** : `git blame` peut être lent sur de gros fichiers
4. **Faux positifs** : Les refactorings peuvent masquer l'origine réelle

## Version

- **Version**: 1.0.0
- **Dernière mise à jour**: 2025-11-24
