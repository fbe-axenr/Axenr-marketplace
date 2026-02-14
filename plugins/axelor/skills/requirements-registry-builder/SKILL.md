---
name: requirements-registry-builder
description: Builds a structured requirements registry from analyzed tickets. Groups tickets by functional need and produces specifications ready for /develop command.
user-invocable: false
---

# Skill: Requirements Registry Builder

## Objectif

Construire un registre des besoins structuré à partir des tickets analysés. Ce skill regroupe intelligemment les tickets par besoin fonctionnel, préserve l'information source, et produit des spécifications prêtes pour la commande `/develop`.

## Entrée Requise

| Paramètre | Description | Obligatoire |
|-----------|-------------|-------------|
| `analyzed_tickets` | Liste des tickets analysés (sortie de `ticket-deep-analyzer`) | Oui |
| `output_directory` | Répertoire de sortie pour le registre | Oui |
| `grouping_threshold` | Seuil de similarité pour regroupement (défaut: 70) | Non |

## Processus

### Étape 1: Indexation des Tickets Analysés

Créer un index des tickets avec leurs caractéristiques clés:

```yaml
index:
  - ticket_id: "104248"
    need_title: "Blocage paiement HoldBack"
    type: "bug"
    modules: ["axelor-account"]
    entities: ["Invoice", "InvoiceTerm", "PaymentSession"]
    keywords: ["holdback", "payment", "reconcile", "invoiceterm"]
    priority_score: 75
```

### Étape 2: Regroupement par Besoin

Algorithme de regroupement multi-critères:

1. **Similarité du besoin** (40%):
   - Comparaison des titres reformulés
   - Comparaison des descriptions

2. **Chevauchement d'entités** (30%):
   - Entités primaires communes
   - Entités secondaires communes

3. **Même workflow/processus** (20%):
   - Workflows identiques
   - États de workflow communs

4. **Même module** (10%):
   - Modules AOS identiques

**Règles de regroupement**:
- Score >= 80%: Fusion automatique (même besoin)
- Score 60-79%: Regroupement en besoin parent avec sous-besoins
- Score < 60%: Besoins distincts

### Étape 3: Construction des Besoins

Pour chaque groupe de tickets, construire un besoin consolidé:

```json
{
  "requirement_id": "REQ-001",
  "title": "Validation paiement échéances HoldBack",
  "type": "bug",
  "tracker": "Anomaly",  // OBLIGATOIRE - extrait du chemin source Scrap/{Tracker}/
  "status": "draft",

  "description": {
    "summary": "Le système doit bloquer le paiement des échéances de retenue de garantie (HoldBack) tant que les autres échéances de la facture ne sont pas soldées",
    "context": "Fonctionnalité de contrôle des paiements dans le module comptabilité",
    "problem_statement": "Actuellement, PaymentSession et le lettrage manuel permettent de payer/lettrer une échéance HoldBack même si les autres échéances ne sont pas soldées",
    "expected_outcome": "Blocage automatique avec message d'alerte dans tous les scénarios de paiement"
  },

  "scope": {
    "modules": [
      {"name": "axelor-account", "confidence": 95}
    ],
    "entities": [
      {"name": "InvoiceTerm", "role": "primary", "fields": ["isPaid", "holdBackPercent"]},
      {"name": "PaymentSession", "role": "primary"},
      {"name": "Reconcile", "role": "primary"},
      {"name": "Invoice", "role": "secondary"}
    ],
    "workflows": ["payment-session", "manual-reconcile"],
    "estimated_complexity": "medium"
  },

  "business_rules": [
    {
      "id": "BR001",
      "type": "validation",
      "description": "Échéance HoldBack non payable si autres échéances non soldées",
      "conditions": ["invoiceTerm.holdBackPercent > 0", "siblingTerms.anyUnpaid"],
      "action": "block_with_alert"
    }
  ],

  "acceptance_criteria": [
    {"id": "AC001", "description": "PaymentSession: blocage paiement HoldBack prématuré"},
    {"id": "AC002", "description": "Lettrage manuel: blocage lettrage HoldBack prématuré"},
    {"id": "AC003", "description": "Message d'alerte explicite affiché"}
  ],

  "source_tickets": [
    {
      "id": "104248",
      "url": "https://redmine.axelor.com/issues/104248",
      "contribution": "primary",
      "specific_info": ["Reproduction steps", "PaymentSession scenario"]
    }
  ],

  "priority": {
    "score": 75,
    "level": "high",
    "rationale": "Impact fonctionnel critique sur processus de paiement"
  },

  "ready_for_develop": true
}
```

### Étape 4: Génération des Spécifications `/develop`

Pour chaque besoin `ready_for_develop: true`, générer une spec compatible:

```markdown
# Spécification: REQ-001 - Validation paiement échéances HoldBack

## Contexte

Le système doit bloquer le paiement des échéances de retenue de garantie (HoldBack)
tant que les autres échéances de la facture ne sont pas soldées.

## Problème Actuel

PaymentSession et le lettrage manuel permettent de payer/lettrer une échéance HoldBack
même si les autres échéances ne sont pas soldées.

## Comportement Attendu

Blocage automatique avec message d'alerte dans tous les scénarios de paiement.

## Scope Technique

### Modules
- axelor-account (principal)

### Entités
- **InvoiceTerm** (primary): champs isPaid, holdBackPercent
- **PaymentSession** (primary)
- **Reconcile** (primary)
- **Invoice** (secondary)

### Workflows Impactés
- payment-session
- manual-reconcile

## Règles Métier

### BR001: Validation HoldBack
- **Type**: Validation
- **Règle**: Une échéance avec holdBackPercent > 0 ne peut être payée/lettrée que si toutes les autres échéances de la même facture sont soldées
- **Action**: Blocage avec message d'erreur

## Critères d'Acceptation

- [ ] AC001: PaymentSession bloque le paiement d'une échéance HoldBack si d'autres échéances non soldées
- [ ] AC002: Lettrage manuel bloque le lettrage d'une ligne HoldBack si d'autres échéances non soldées
- [ ] AC003: Message d'alerte explicite et compréhensible affiché à l'utilisateur

## Tickets Source

- #104248: SUPPLIERINVOICE / INVOICETERMS / HOLDBACK - Add alert when trying to reconcile

## Estimation

- **Complexité**: Medium
- **Priorité**: High (score: 75)
```

### Étape 5: Construction du Registre

Produire le fichier `requirements-registry.json`:

```json
{
  "registry_version": "1.0",
  "generated_at": "2025-11-22T10:30:00Z",
  "source": {
    "tickets_analyzed": 100,
    "requirements_created": 45,
    "grouping_ratio": 2.22
  },

  "statistics": {
    "by_type": {
      "bug": 32,
      "enhancement": 8,
      "new_feature": 3,
      "configuration": 2
    },
    "by_module": {
      "axelor-account": 25,
      "axelor-sale": 10,
      "axelor-stock": 8,
      "axelor-base": 12
    },
    "by_priority": {
      "critical": 5,
      "high": 15,
      "medium": 20,
      "low": 5
    },
    "ready_for_develop": 38,
    "needs_clarification": 7
  },

  "requirements": [
    // Liste complète des besoins (format ci-dessus)
  ],

  "groupings": [
    {
      "requirement_id": "REQ-001",
      "tickets": ["104248"],
      "similarity_scores": {}
    },
    {
      "requirement_id": "REQ-002",
      "tickets": ["103456", "103789", "104001"],
      "similarity_scores": {
        "103456-103789": 85,
        "103456-104001": 72,
        "103789-104001": 78
      },
      "grouping_rationale": "Même entité Invoice, même type de problème calcul TVA"
    }
  ]
}
```

## Format de Sortie

```
{output_directory}/
├── requirements-registry.json      # Registre complet
├── specs/
│   ├── Anomaly/                    # Organisé par tracker (OBLIGATOIRE)
│   │   ├── REQ-001.md
│   │   └── REQ-002.md
│   ├── Feature/
│   │   ├── REQ-050.md
│   │   └── REQ-051.md
│   └── Support/
│       └── REQ-100.md
└── index/
    ├── by-module.json              # Index par module
    ├── by-entity.json              # Index par entité
    ├── by-tracker.json             # Index par tracker (NEW)
    └── by-priority.json            # Index par priorité
```

**CRITIQUE**: Les specs DOIVENT être organisées par tracker source. Le tracker est extrait du chemin du ticket source: `Scrap/Anomaly/xxx.md` → `specs/Anomaly/REQ-xxx.md`

## Règles de Qualité du Registre

| Critère | Requis |
|---------|--------|
| Chaque ticket assigné à un requirement | Oui |
| Pas de perte d'information source | Oui |
| Specs générées pour requirements ready | Oui |
| Traçabilité ticket → requirement | Oui |

## Métriques de Sortie

```yaml
metrics:
  tickets_processed: 100
  requirements_created: 45
  average_tickets_per_requirement: 2.22
  ready_for_develop_count: 38
  needs_clarification_count: 7
  coverage_percentage: 100
```

## Version

- **Version**: 1.0.0
- **Dernière mise à jour**: 2025-11-22
