# Skill: Redmine Ticket Parser

## Objectif

Parser et extraire des informations structurées à partir de tickets Redmine exportés en markdown. Ce skill analyse le contenu des tickets pour identifier les éléments clés utiles à l'analyse et à la consolidation.

## Entrée Requise

| Paramètre | Description | Obligatoire |
|-----------|-------------|-------------|
| `ticket_path` | Chemin vers le fichier markdown du ticket | Oui |
| `extraction_mode` | Mode d'extraction: `full`, `metadata`, `business_rules` | Non (défaut: `full`) |

## Processus

### Étape 1: Lecture du Ticket

Utilise l'outil **Read** pour charger le contenu du fichier markdown.

### Étape 2: Extraction des Métadonnées

Extraire les informations de la table de métadonnées:

```
- id_redmine: Numéro du ticket (#XXXXX)
- url: Lien vers le ticket original
- projet: Nom du projet Redmine
- tracker: Type de demande (Bug, Fonctionnalité, Support, etc.)
- statut: État actuel (Nouveau, En cours, Résolu, etc.)
- priorité: Niveau de priorité
- auteur: Créateur du ticket
- assigné: Personne responsable
- date_création: Date de création
- date_mise_à_jour: Dernière modification
- version_cible: Version prévue
- sprint: Sprint associé
- module: Module Axelor concerné
```

### Étape 3: Extraction de la Description

Analyser la section "Description" pour extraire:

1. **Contexte fonctionnel**: Quel est le contexte métier?
2. **Comportement attendu**: Qu'est-ce qui devrait se passer?
3. **Comportement actuel** (si bug): Qu'est-ce qui se passe actuellement?
4. **Étapes de reproduction** (si bug): Comment reproduire le problème?
5. **Critères d'acceptation** (si fonctionnalité): Quand considère-t-on que c'est terminé?

### Étape 4: Extraction des Règles Métier

Identifier dans la description et les notes:

- **Règles de validation**: Contraintes sur les données
- **Règles de calcul**: Formules et algorithmes
- **Règles de workflow**: Transitions d'état, actions automatiques
- **Règles d'affichage**: Conditions de visibilité, formatage

Pattern de détection des règles:
```
- "Si ... alors ..."
- "Quand ... doit ..."
- "Ne peut pas ... si ..."
- "Automatiquement ..."
- "Doit être calculé ..."
- "Obligatoire si ..."
```

### Étape 5: Extraction des Entités Mentionnées

Identifier les entités Axelor potentiellement concernées:

- Noms d'entités en PascalCase (ex: `SaleOrder`, `Partner`)
- Références aux modules (ex: `axelor-sale`, `axelor-stock`)
- Champs mentionnés (ex: `statusSelect`, `totalExTaxTotal`)

### Étape 6: Analyse des Relations

Extraire les informations de la section "Demandes Liées":

```
- type_relation: (Lié à, Bloque, Bloqué par, Duplique, etc.)
- ticket_lié: ID du ticket associé
- direction: (entrant/sortant)
```

### Étape 7: Synthèse des Notes

Analyser les commentaires pour extraire:

- **Décisions prises**: Choix validés en commentaire
- **Clarifications**: Réponses aux questions
- **Obstacles**: Problèmes rencontrés
- **Évolutions**: Changements de périmètre

## Format de Sortie

```yaml
ticket:
  id: "XXXXX"
  url: "https://..."
  titre: "..."

metadata:
  projet: "..."
  tracker: "..."
  statut: "..."
  priorité: "..."
  auteur: "..."
  assigné: "..."
  version_cible: "..."
  sprint: "..."
  module: "..."

description:
  contexte: "..."
  comportement_attendu: "..."
  comportement_actuel: "..."  # Si bug
  étapes_reproduction: []      # Si bug
  critères_acceptation: []     # Si fonctionnalité

règles_métier:
  - type: "validation|calcul|workflow|affichage"
    description: "..."
    conditions: []

entités_détectées:
  - nom: "SaleOrder"
    module_probable: "axelor-sale"
    champs_mentionnés: ["statusSelect", "totalExTaxTotal"]

relations:
  - type: "Lié à"
    ticket_id: "12345"
  - type: "Bloqué par"
    ticket_id: "12340"

notes_synthèse:
  décisions: []
  clarifications: []
  obstacles: []
  évolutions_périmètre: []

qualité:
  score_complétude: 75  # Pourcentage de sections remplies
  informations_manquantes:
    - "Critères d'acceptation non définis"
    - "Module non spécifié"
```

## Indicateurs de Qualité

| Score | Signification |
|-------|---------------|
| 90-100 | Ticket très bien documenté, prêt pour l'implémentation |
| 70-89 | Ticket correct, quelques clarifications souhaitables |
| 50-69 | Ticket incomplet, nécessite des compléments |
| < 50 | Ticket insuffisant, requiert une refonte |

## Critères de Complétude

- [ ] ID et URL présents
- [ ] Tracker identifié
- [ ] Description non vide
- [ ] Au moins un critère d'acceptation (si fonctionnalité)
- [ ] Étapes de reproduction (si bug)
- [ ] Module ou entité identifiable
- [ ] Priorité définie
- [ ] Version cible définie

## Exemple d'Utilisation

```
Input: ticket_path = "./Analysis/Ticket/Scrap/Fonctionnalité/00123.md"

Output:
ticket:
  id: "123"
  url: "https://redmine.axelor.com/issues/123"
  titre: "Ajout export Excel sur la liste des commandes"

metadata:
  projet: "AOS"
  tracker: "Fonctionnalité"
  statut: "Nouveau"
  priorité: "Normal"
  module: "axelor-sale"

description:
  contexte: "Les utilisateurs souhaitent exporter la liste des commandes"
  comportement_attendu: "Un bouton Excel permet d'exporter les données visibles"
  critères_acceptation:
    - "Export des colonnes visibles uniquement"
    - "Respect des filtres actifs"
    - "Format xlsx compatible Excel 2016+"

entités_détectées:
  - nom: "SaleOrder"
    module_probable: "axelor-sale"
    champs_mentionnés: ["saleOrderSeq", "clientPartner", "totalExTaxTotal"]

qualité:
  score_complétude: 85
  informations_manquantes:
    - "Version cible non définie"
```

## Version

- **Version**: 1.0.0
- **Dernière mise à jour**: 2025-01-21
