---
name: us-quality-validator
description: Validates User Stories and EPICs against quality standards - business orientation, Given-When-Then format, and Dev/QA/PM-BA estimation breakdown.
user-invocable: false
---

# US Quality Validator Skill (v2)

Valide les User Stories et EPICs selon les standards de qualité v2 : orientation métier, format Given-When-Then, et estimation Dev/QA/PM-BA.

## Purpose

Ce skill valide :
- **Orientation métier** : Pas de contenu technique dans les US
- **Rôles business** : Utilisateurs métier uniquement
- **Given-When-Then** : Format obligatoire pour les AC
- **Estimation par profil** : Répartition Dev/QA/PM-BA
- **INVEST** : Critères Agile standards
- **Complétude** : Toutes les sections requises présentes

## Usage

**Input** : Document EPIC/US généré ou User Story individuelle
**Output** : Rapport de validation avec pass/fail et recommandations

---

## Validations v2 (Nouvelles règles)

### 1. Pas de contenu technique

**Critère** : Les User Stories ne doivent contenir AUCUN élément technique.

**Éléments interdits** :
- ❌ Code XML (domaines, vues)
- ❌ Code Java (services, controllers)
- ❌ Code SQL (queries, indexes)
- ❌ Chemins de fichiers (`src/main/resources/...`)
- ❌ Noms de classes (`ProductOptionService`, `SaleOrderLineController`)
- ❌ Détails d'architecture technique
- ❌ Schémas de base de données

**Validation** :
```
- [ ] Aucun bloc de code (<pre>, ```)
- [ ] Aucun chemin de fichier
- [ ] Aucun nom de classe/méthode technique
- [ ] Aucune référence à des packages Java
- [ ] Aucun schéma de base de données
```

**PASS** :
```markdown
**En tant que** responsable produit
**Je veux** définir les options par défaut pour mes produits
**Afin de** permettre aux commerciaux de proposer automatiquement les accessoires
```

**FAIL** :
```markdown
**En tant que** développeur
**Je veux** créer l'entité ProductOption avec les champs:
  - product (many-to-one)
  - defaultQuantity (decimal)
Path: src/main/resources/domains/ProductOption.xml
```

---

### 2. Rôles business uniquement

**Critère** : Le "En tant que..." doit utiliser un rôle métier, pas technique.

**Rôles autorisés** :
- ✅ Commercial / Sales representative
- ✅ Responsable produit / Product manager
- ✅ Gestionnaire de stock / Stock manager
- ✅ Comptable / Accountant
- ✅ Acheteur / Buyer
- ✅ Administrateur métier / Business admin
- ✅ Manager
- ✅ Client

**Rôles interdits** :
- ❌ Développeur / Developer
- ❌ Architecte / Architect
- ❌ DBA / Database administrator
- ❌ Admin système / System admin
- ❌ DevOps
- ❌ Testeur technique / Technical tester
- ❌ System architect

**Validation** :
```
- [ ] Rôle = utilisateur métier
- [ ] Rôle ≠ profil technique
```

---

### 3. Format Given-When-Then obligatoire

**Critère** : Tous les critères d'acceptation doivent suivre le format Given-When-Then.

**Structure requise** :
```
Given [contexte/pré-condition]
When [action de l'utilisateur]
Then [résultat observable]
```

**Validation** :
```
- [ ] Chaque AC commence par "Given"
- [ ] Chaque AC contient "When"
- [ ] Chaque AC contient "Then"
- [ ] Le résultat est observable et mesurable
```

**PASS** :
```markdown
1. **Given** un produit avec 3 options configurées
   **When** le commercial ajoute ce produit à un devis
   **Then** les 3 options apparaissent automatiquement
```

**FAIL** :
```markdown
1. Les options doivent s'afficher correctement
2. L'utilisateur peut modifier les options
```

---

### 4. Estimation avec répartition par profil

**Critère** : L'estimation doit inclure Dev/QA/PM-BA séparés.

**Format requis** :
```markdown
| Profil | Effort | Justification |
|--------|--------|---------------|
| Dev | X h | [raison] |
| QA | Y h | [raison] |
| PM/BA | Z h | [raison] |
| **Total** | **N h** | |
```

**Validation** :
```
- [ ] Ligne Dev présente avec effort
- [ ] Ligne QA présente avec effort
- [ ] Ligne PM/BA présente avec effort
- [ ] Total calculé
- [ ] Justification fournie
```

**FAIL** (ancien format) :
```markdown
Complexity: M
Effort: 1 day
```

---

## Validations INVEST (Maintenues)

### I - Indépendante

**Critère** : La US peut être développée indépendamment.

**Validation** :
- [ ] Dépendances explicites
- [ ] Pas de développement parallèle requis
- [ ] Livrable de valeur même si dépendances retardées

---

### N - Négociable

**Critère** : Les détails peuvent être discutés.

**Validation** :
- [ ] AC focus sur "quoi" pas "comment"
- [ ] Détails techniques = guidance, pas obligations
- [ ] Marge pour choix d'implémentation

---

### V - Valuable (Valeur)

**Critère** : Apporte de la valeur métier.

**Validation** :
- [ ] "En tant que... Je veux... Afin de..." complet
- [ ] "Afin de" décrit un bénéfice métier réel
- [ ] US pas purement technique

---

### E - Estimable

**Critère** : Peut être estimée avec précision.

**Validation** :
- [ ] Estimation Dev/QA/PM-BA fournie
- [ ] Scope clair
- [ ] Pas d'inconnues majeures

---

### S - Small (Petite)

**Critère** : Réalisable dans un sprint.

**Validation** :
- [ ] Effort total ≤ 16 heures (2 jours)
- [ ] Si > 16h, marquer comme XL et découper
- [ ] Scope focalisé

---

### T - Testable

**Critère** : AC clairs et vérifiables.

**Validation** :
- [ ] AC spécifiques et mesurables
- [ ] Pass/fail objectif
- [ ] Pas de langage subjectif ("looks good", "feels right")

---

## Checklist de validation complète

### Pour chaque User Story

```markdown
## Validation US-XXX

### v2 - Nouvelles règles
- [ ] **Pas de technique** : Aucun code, chemin, classe
- [ ] **Rôle métier** : "En tant que" = utilisateur business
- [ ] **Given-When-Then** : Tous les AC suivent le format
- [ ] **Estimation profil** : Dev/QA/PM-BA séparés

### INVEST
- [ ] **Indépendante** : Développable seule
- [ ] **Négociable** : AC focus sur "quoi"
- [ ] **Valuable** : Bénéfice métier clair
- [ ] **Estimable** : Effort par profil fourni
- [ ] **Small** : ≤ 16h total
- [ ] **Testable** : AC mesurables

### Complétude
- [ ] Titre orienté valeur
- [ ] Statement complet (En tant que... Je veux... Afin de...)
- [ ] Minimum 3 AC en Given-When-Then
- [ ] Estimation avec tableau Dev/QA/PM-BA
- [ ] Dépendances listées ou "Aucune"

### Résultat
**Status** : ✅ PASS / ⚠️ REVIEW / ❌ FAIL
```

---

## Format de rapport de validation

### Rapport individuel

```markdown
## Validation Report: US-005

### v2 Compliance
- ✅ No technical content: Clean business language
- ✅ Business role: "Commercial" (valid)
- ✅ Given-When-Then: All 4 AC follow format
- ✅ Profile estimation: Dev 6h / QA 2h / PM 1h

### INVEST Criteria
- ✅ Independent: Dependencies listed (US-003)
- ✅ Negotiable: AC describe outcomes
- ✅ Valuable: Clear benefit for sales team
- ✅ Estimable: 9h total with breakdown
- ✅ Small: 9h < 16h limit
- ✅ Testable: All AC are measurable

### Completeness
- ✅ Title: Business-oriented
- ✅ Statement: Complete
- ✅ AC: 4 criteria in Given-When-Then
- ✅ Estimation: Profile breakdown provided
- ✅ Dependencies: Explicit

**OVERALL: ✅ PASS (16/16)**
```

### Rapport EPIC

```markdown
## Validation Report: EPIC-001

### Structure
- ✅ Markdown format (not Textile)
- ✅ Single file (no INDEX/DEPENDENCIES)
- ✅ All US in same file

### US Quality Summary
| US | v2 Rules | INVEST | Complete | Status |
|----|----------|--------|----------|--------|
| US-001 | 4/4 | 6/6 | 5/5 | ✅ PASS |
| US-002 | 4/4 | 6/6 | 5/5 | ✅ PASS |
| US-003 | 3/4 | 6/6 | 5/5 | ⚠️ REVIEW |

### Issues Found
1. **US-003** (REVIEW):
   - v2 Rule: AC #2 missing "Given" keyword
   - **Fix**: Add context before "When"

### Summary
- **Total US**: 3
- **PASS**: 2
- **REVIEW**: 1
- **FAIL**: 0
- **Ready**: YES (after minor fix)
```

---

## Erreurs courantes et corrections

### Erreur 1 : Contenu technique dans US

**Problème** :
```markdown
Technical Details:
- Domain: src/main/resources/domains/ProductOption.xml
- Service: ProductOptionService.java
```

**Correction** : Supprimer toute la section technique. Les US ne doivent pas contenir ces informations.

---

### Erreur 2 : Rôle technique

**Problème** :
```markdown
**En tant que** développeur
**Je veux** créer une entité
```

**Correction** :
```markdown
**En tant que** responsable produit
**Je veux** configurer les options des produits
```

---

### Erreur 3 : AC sans Given-When-Then

**Problème** :
```markdown
- Les options s'affichent correctement
- L'utilisateur peut modifier
```

**Correction** :
```markdown
1. **Given** un produit avec des options
   **When** le commercial ouvre la fiche produit
   **Then** les options s'affichent dans l'onglet dédié
```

---

### Erreur 4 : Estimation sans profil

**Problème** :
```markdown
Complexity: M
Effort: 1 day
```

**Correction** :
```markdown
| Profil | Effort | Justification |
|--------|--------|---------------|
| Dev | 5h | Form + service |
| QA | 2h | Tests fonctionnels |
| PM/BA | 1h | Validation |
| **Total** | **8h = 1j** | |
```

---

## Related Skills

- [Epic Estimator](../epic-estimator/SKILL.md)
- [US Dependency Mapper](../us-dependency-mapper/SKILL.md)

## Related Documents

- [EPIC Template](../../docs/templates/epic-template.md)
- [User Story Template](../../docs/templates/user-story-template.md)

---

**Version** : 2.0 (Validation orientation métier, Given-When-Then, estimation par profil)
**Dernière mise à jour** : 2025-11-28
