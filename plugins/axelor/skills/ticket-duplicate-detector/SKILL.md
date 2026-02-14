---
name: ticket-duplicate-detector
description: Detects potentially duplicate or highly similar Redmine tickets by analyzing titles, descriptions, and related entities.
user-invocable: false
---

# Skill: Ticket Duplicate Detector

## Objectif

Détecter les tickets potentiellement dupliqués ou fortement similaires dans un ensemble de tickets Redmine. Ce skill analyse les titres, descriptions et entités concernées pour identifier les regroupements possibles.

## Entrée Requise

| Paramètre | Description | Obligatoire |
|-----------|-------------|-------------|
| `tickets_directory` | Répertoire contenant les tickets parsés | Oui |
| `similarity_threshold` | Seuil de similarité (0-100, défaut: 70) | Non |
| `output_format` | Format de sortie: `report`, `groups`, `matrix` | Non (défaut: `report`) |

## Processus

### Étape 1: Chargement des Tickets

1. Utiliser **Glob** pour lister tous les fichiers `*.md` dans le répertoire
2. Pour chaque fichier, extraire avec **Read**:
   - ID du ticket
   - Titre
   - Description (premiers 500 caractères)
   - Tracker
   - Module/Entités détectées

### Étape 2: Normalisation du Texte

Avant comparaison, normaliser le texte:

```
1. Conversion en minuscules
2. Suppression des caractères spéciaux
3. Suppression des mots vides (le, la, les, de, du, etc.)
4. Extraction des tokens significatifs
5. Identification des termes métier Axelor
```

**Termes métier à préserver**:
- Noms d'entités: `SaleOrder`, `Partner`, `Invoice`, `StockMove`...
- Modules: `axelor-sale`, `axelor-stock`, `axelor-account`...
- Actions: `valider`, `confirmer`, `annuler`, `dupliquer`...

### Étape 3: Calcul de Similarité

Utiliser une approche multi-critères:

#### 3.1 Similarité du Titre (Poids: 40%)

```
score_titre = (mots_communs / max(mots_titre1, mots_titre2)) * 100
```

#### 3.2 Similarité de la Description (Poids: 30%)

```
score_description = (tokens_communs / max(tokens_desc1, tokens_desc2)) * 100
```

#### 3.3 Similarité des Entités (Poids: 20%)

```
score_entités = (entités_communes / max(entités1, entités2)) * 100
```

#### 3.4 Même Tracker (Poids: 10%)

```
score_tracker = 100 si même tracker, 50 sinon
```

#### Score Final

```
score_final = (score_titre * 0.4) + (score_description * 0.3) +
              (score_entités * 0.2) + (score_tracker * 0.1)
```

### Étape 4: Identification des Groupes

Regrouper les tickets par similarité:

```
1. Pour chaque paire de tickets avec score >= seuil:
   - Créer une relation de similarité

2. Construire les clusters:
   - Un ticket peut appartenir à plusieurs groupes
   - Identifier le ticket "principal" (le plus ancien ou le plus complet)

3. Classifier les relations:
   - DUPLICATE: score >= 90 (probable doublon exact)
   - SIMILAR: score >= 75 (très similaire, possible fusion)
   - RELATED: score >= threshold (lié, à vérifier)
```

### Étape 5: Analyse des Différences

Pour chaque groupe détecté, identifier:

```
- Informations communes
- Informations uniques à chaque ticket
- Recommandation de fusion
- Ticket suggéré comme principal
```

## Format de Sortie

### Mode `report` (défaut)

```markdown
# Rapport de Détection des Doublons

## Résumé

- Tickets analysés: 45
- Groupes de doublons détectés: 8
- Tickets potentiellement dupliqués: 12
- Taux de duplication: 26.7%

## Doublons Détectés (score >= 90)

### Groupe 1: Export Excel
| Ticket | Titre | Score |
|--------|-------|-------|
| #123 (Principal) | Export Excel des commandes | - |
| #456 | Ajouter export XLS sur SaleOrder | 92% |

**Analyse**: Les deux tickets demandent la même fonctionnalité.
**Recommandation**: Fusionner #456 dans #123, conserver les critères
d'acceptation de #456.

### Groupe 2: ...

## Tickets Similaires (score 75-89)

...

## Tickets Liés (score 70-74)

...

## Matrice de Similarité

| | #123 | #456 | #789 |
|--|------|------|------|
| #123 | - | 92% | 45% |
| #456 | 92% | - | 48% |
| #789 | 45% | 48% | - |
```

### Mode `groups`

```yaml
groupes:
  - id: "group-1"
    type: "DUPLICATE"
    score_moyen: 92
    ticket_principal: "123"
    tickets:
      - id: "123"
        titre: "Export Excel des commandes"
        score: 100
      - id: "456"
        titre: "Ajouter export XLS sur SaleOrder"
        score: 92
    recommandation: "Fusionner #456 dans #123"

  - id: "group-2"
    type: "SIMILAR"
    ...
```

### Mode `matrix`

```csv
ticket_1,ticket_2,score,type
123,456,92,DUPLICATE
123,789,45,NONE
456,789,48,NONE
```

## Règles de Détection Spécifiques Axelor

### Patterns de Duplication Fréquents

1. **Même entité, action différente**:
   - "Ajouter bouton export" vs "Export des données"
   - Score bonus: +10 si même entité

2. **Formulation différente, même besoin**:
   - "Impossible de valider" vs "Erreur lors de la validation"
   - Détection via verbes d'action similaires

3. **Bug vs Amélioration**:
   - Bug: "Le calcul TVA est faux"
   - Amélioration: "Revoir le calcul TVA"
   - Signaler le lien même si trackers différents

### Termes Synonymes Axelor

```yaml
synonymes:
  commande: [order, bon de commande, purchase order, sale order]
  facture: [invoice, bill, avoir]
  client: [partner, tiers, customer]
  article: [product, produit, item]
  stock: [inventory, inventaire]
  valider: [confirmer, approve, confirm]
  annuler: [cancel, supprimer]
```

## Indicateurs de Qualité

| Métrique | Description |
|----------|-------------|
| Précision | % de vrais doublons parmi les détectés |
| Rappel | % de doublons réels détectés |
| Faux positifs | Tickets marqués à tort comme doublons |

## Seuils Recommandés

| Contexte | Seuil | Justification |
|----------|-------|---------------|
| Analyse stricte | 85 | Moins de faux positifs |
| Analyse standard | 70 | Équilibre précision/rappel |
| Analyse exhaustive | 60 | Plus de détection, plus de bruit |

## Exemple d'Utilisation

```
Input:
  tickets_directory: "./Analysis/Ticket/Scrap"
  similarity_threshold: 70
  output_format: "report"

Output:
  # Rapport généré dans ./Analysis/Ticket/Consolidated/duplicate-report.md

  Résumé:
  - 45 tickets analysés
  - 3 groupes de doublons exacts (score >= 90)
  - 5 groupes de tickets similaires (score 75-89)
  - 12 paires de tickets liés (score 70-74)
```

## Intégration avec Autres Skills

Ce skill peut être combiné avec:

- `@skills/redmine-ticket-parser`: Pour obtenir les données structurées
- `@skills/aos-entity-searcher`: Pour enrichir la détection par entités

## Version

- **Version**: 1.0.0
- **Dernière mise à jour**: 2025-01-21
