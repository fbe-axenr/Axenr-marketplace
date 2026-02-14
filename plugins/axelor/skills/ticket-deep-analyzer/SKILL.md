---
name: ticket-deep-analyzer
description: Deep analysis of Redmine tickets to extract precise requirement characterization, including scope, business rules, and derived acceptance criteria.
user-invocable: false
---

# Skill: Ticket Deep Analyzer

## Objectif

Analyser en profondeur un ticket Redmine pour extraire une caractérisation exacte et précise du besoin, incluant le scope, les règles métier, et les critères d'acceptation dérivés. Ce skill produit une sortie optimisée pour les agents de développement.

## Entrée Requise

| Paramètre | Description | Obligatoire |
|-----------|-------------|-------------|
| `ticket_path` | Chemin vers le fichier markdown du ticket | Oui |
| `tracker_type` | Type de tracker: `anomaly`, `feature`, `support` | Non (auto-détecté) |

## Embedded Documentation

@docs/requirements/business-types-reference.md - Mapping termes métier vers types Axelor
@docs/requirements/requirements-refining-methodology.md - Méthodologie extraction règles métier
@docs/framework/axelor-conventions.md - Conventions de nommage Axelor
@docs/analysis/axelor-patterns-for-analysis.md - Patterns d'entités reconnaissables
@docs/domains/domain-patterns.md - Patterns de domaines XML

## Processus

### Étape 1: Lecture Complète

Utiliser l'outil **Read** pour charger l'intégralité du ticket (description, notes, métadonnées, demandes liées).

### Étape 2: Identification du Besoin Principal

Extraire:
1. **Titre du besoin** (reformulé si nécessaire)
2. **Type de besoin**: `bug`, `enhancement`, `new_feature`, `configuration`, `performance`, `ux`, `data`, `integration`
3. **Description précise** (1-3 phrases):
   - Bug: "Le système fait X au lieu de Y dans le contexte Z"
   - Feature: "Le système doit permettre X pour que Y"

### Étape 3: Extraction du Scope

Identifier le périmètre impacté en utilisant les conventions de nommage Axelor:
- Entités en PascalCase: `SaleOrder`, `Invoice`, `StockMove`
- Champs en camelCase avec patterns: `*Select` (enum), `*List` (collection), `*Date`, `*Amount`

```yaml
scope:
  modules:
    - name: "axelor-account"
      confidence: 95
  entities:
    - name: "Invoice"
      role: "primary"  # primary|secondary|related
      fields_mentioned: ["statusSelect", "invoiceTermList"]
  workflows:
    - name: "invoice-payment"
```

### Étape 4: Extraction des Règles Métier

Identifier les règles en utilisant les patterns de détection:
- Explicites: "doit", "ne peut pas", "obligatoire", "interdit"
- Implicites: "quand", "si", "lorsque", "dans le cas où"
- Exceptions: "sauf si", "excepté", "à moins que"

```yaml
business_rules:
  - id: "BR001"
    type: "validation"  # validation|calculation|workflow|display|constraint
    description: "Description de la règle"
    conditions: ["condition1", "condition2"]
    expected_behavior: "Comportement attendu"
    source: "description"  # description|note|inferred
```

### Étape 5: Analyse du Comportement (Bug uniquement)

Pour les anomalies, extraire:
- `current_behavior`: Ce qui se passe actuellement
- `expected_behavior`: Ce qui devrait se passer
- `reproduction_steps`: Étapes pour reproduire
- `affected_scenarios`: Scénarios impactés
- `working_scenarios`: Scénarios fonctionnels

### Étape 6: Dérivation des Critères d'Acceptation

Générer les critères d'acceptation à partir des règles métier:

```yaml
acceptance_criteria:
  - id: "AC001"
    description: "Description du critère"
    type: "functional"  # functional|ux|performance|security
    derived_from: "BR001"
```

### Étape 7: Calcul du Score de Priorité

Score de 0-100 basé sur:
- `urgency` (30%): Priorité Redmine et ancienneté
- `impact` (30%): Scope (nombre d'entités/modules)
- `clarity` (20%): Qualité de la description
- `frequency` (20%): Fréquence estimée du problème

### Étape 8: Identification des Besoins Connexes

Extraire sous-besoins (`sub_need`) et prérequis (`prerequisite`).

### Étape 9-11: Validation AOS (optionnel)

**Prérequis**: Paramètre `aos_path` fourni.

Utiliser les skills de validation AOS pour:
- Vérifier l'existence des entités dans AOS
- Valider les champs mentionnés
- Enrichir le contexte module

### Étape 12: Recherche de Régression Git (Bug uniquement)

**Prérequis**: `aos_path` fourni ET type `bug`.

Identifier l'origine de la régression via analyse Git.

## Format de Sortie

Voir [output-example.json](reference/output-example.json) pour un exemple complet.

Structure principale:
```json
{
  "ticket_id": "string",
  "need": { "id", "title", "type", "description", "summary" },
  "scope": { "modules", "entities", "workflows", "ui_elements" },
  "business_rules": [{ "id", "type", "description", "conditions" }],
  "bug_analysis": { "current_behavior", "expected_behavior", "reproduction_steps" },
  "acceptance_criteria": [{ "id", "description", "type", "derived_from" }],
  "priority_score": { "value", "factors" },
  "aos_validation": { "entities_validated", "fields_validated", "validation_score" },
  "regression_analysis": { "suspect_commits", "most_likely_cause" },
  "ready_for_develop": boolean,
  "quality_score": number
}
```

## Règles de Qualité

| Champ | Requis pour `ready_for_develop: true` |
|-------|---------------------------------------|
| `need.description` | Oui, min 50 caractères |
| `scope.entities` | Oui, au moins 1 entité |
| `business_rules` | Oui pour bugs, recommandé pour features |
| `acceptance_criteria` | Oui, au moins 1 critère |
| `bug_analysis` (si bug) | Oui, avec reproduction_steps |

## Indicateurs de Qualité

| Score | Signification |
|-------|---------------|
| 90-100 | Analyse complète avec validation AOS, prêt pour `/develop` |
| 80-89 | Analyse complète, quelques entités non validées |
| 70-79 | Analyse suffisante, quelques inférences |
| 50-69 | Analyse partielle, informations manquantes |
| < 50 | Ticket trop vague, nécessite clarification |

**Bonus avec AOS validation**: +5 (entités validées) +5 (champs validés) +2 (services identifiés)
**Bonus avec regression_analysis**: +5 (commit suspect ≥70%) +3 (cause identifiée) +2 (contacts extraits)

## Outils Requis

- `Read`: Lecture du fichier ticket
- `Write`: Écriture du JSON de sortie
- `Bash`, `Grep`: Pour enrichissement AOS (optionnel)

## Version

- **Version**: 2.1.0
- **Dernière mise à jour**: 2025-11-24
