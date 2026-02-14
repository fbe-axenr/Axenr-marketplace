# Analyze Requirements - Guide Complet

Ce guide complète la commande `/analyze-requirements` avec des conseils avancés, exemples détaillés et résolution de problèmes.

---

## Exemples d'utilisation

### Exemple 1: Depuis une description textuelle

```
/analyze-requirements I need a CRM module to manage customer leads with automatic scoring based on activity, qualification workflow with multiple stages, and automatic assignment to sales representatives based on territory and workload
```

L'agent va:
1. Analyser ce besoin
2. Identifier les entités (Lead, Territory, User, Activity)
3. Poser des questions de clarification sur les règles de scoring, les étapes du workflow, la logique d'assignation
4. Procéder au raffinement et à la génération des EPICs après vos réponses

### Exemple 2: Depuis un PDF Cahier des Charges

```
/analyze-requirements /home/user/documents/cahier-des-charges-crm-v2.pdf
```

L'agent va:
1. Lire le document PDF (supporte 150+ pages)
2. Appliquer une stratégie d'analyse progressive section par section
3. Extraire entités, fonctionnalités et exigences
4. Générer une analyse complète avec questions ciblées
5. Poursuivre les phases du workflow

### Exemple 3: Depuis un DOCX de spécifications fonctionnelles

```
/analyze-requirements ./specs/functional-specifications-lead-management.docx
```

L'agent va:
1. Lire le document DOCX
2. Appliquer la méthodologie d'analyse appropriée à la taille du document
3. Générer un rapport d'analyse structuré
4. Continuer avec le raffinement et la génération des US

### Exemple 4: Avec répertoire de sortie personnalisé

```
/analyze-requirements "E-commerce order management module" analysis/ecommerce-2025
```

L'agent va:
1. Analyser le besoin
2. Générer tous les artefacts dans `analysis/ecommerce-2025/`:
   - `analysis/ecommerce-2025/analysis-report.md`
   - `analysis/ecommerce-2025/gap-analysis-report.md`
   - `analysis/ecommerce-2025/detailed-specifications.md`
   - `analysis/ecommerce-2025/epic-us-breakdown.textile`
3. Créer le répertoire s'il n'existe pas

**Cas d'usage pour répertoires personnalisés:**
- Analyses parallèles pour différents projets
- Organisation par client: `analysis/client-acme/`
- Organisation par date: `analysis/2025-01/`
- Séparation des tests de la documentation de production

---

## Conseils pour réussir

### Documents volumineux (100+ pages)

- **Soyez patient**: L'analyse prend du temps (~2-3 heures pour un document de 120 pages)
- **Les documents structurés fonctionnent mieux**: Sections claires, table des matières
- **Processus interactif**: Soyez prêt à répondre aux questions de clarification pendant la Phase 1
- **Points de validation**: Examinez attentivement chaque sortie de phase avant de continuer

Pour les détails méthodologiques, voir @docs/analysis/large-document-strategy.md

### Besoins courts (< 10 pages)

- **Délai rapide**: L'analyse se termine généralement en 15-30 minutes
- **Posez quand même des questions**: Ne sautez pas la clarification même pour des besoins "simples"
- **Validez la compréhension**: Toujours revoir l'analyse avant de passer au raffinement

### Besoins conversationnels (sans document)

- **Soyez détaillé**: Fournissez autant de contexte que possible dès le départ
- **Attendez-vous à beaucoup de questions**: L'agent posera de nombreuses questions pour combler les lacunes
- **Itératif**: Peut nécessiter plusieurs échanges

### Maximiser la qualité

- **Répondez à toutes les questions CRITIQUES**: Elles bloquent la conception de l'architecture
- **Fournissez des exemples**: Les scénarios concrets aident à clarifier les exigences
- **Soyez spécifique**: "Workflow de statut" est vague; "BROUILLON → SOUMIS → APPROUVÉ → REJETÉ" est clair
- **Pensez aux cas limites**: L'agent demandera, mais vous pouvez anticiper

---

## Résolution de problèmes

### Problème: Le rapport d'analyse contient trop de questions

**Solution**:
- Répondez d'abord aux questions CRITIQUE et HAUTE priorité
- Certaines questions MOYENNE/BASSE peuvent être répondues pendant le raffinement
- Considérez si le besoin initial était trop vague

### Problème: La phase de raffinement continue de poser des questions

**Solution**:
- C'est normal pour des besoins complexes
- Le raffinement est conversationnel et progressif
- Faites des pauses entre entités/fonctionnalités si nécessaire

### Problème: Les User Stories semblent trop/pas assez granulaires

**Solution**:
- Fournissez des retours pendant la validation de la structure EPIC en Phase 3
- L'agent peut ajuster la décomposition selon vos préférences
- Considérez la capacité de sprint de votre équipe

### Problème: L'analyse de document volumineux prend très longtemps

**Solution**:
- C'est attendu pour les documents de 100+ pages
- L'agent utilise une stratégie progressive (section par section)
- Peut être mis en pause et repris aux points de validation
- Envisagez de pré-extraire les sections clés si le document contient beaucoup de contenu superflu

---

## Livrables détaillés

À la fin du workflow, vous aurez trois documents clés:

### 1. {OUTPUT_DIR}/analysis-report.md
- Analyse métier avec questions de clarification **répondues**
- Entités et fonctionnalités identifiées
- Recommandations de patterns Axelor
- **Prêt pour**: Phase de raffinement

### 2. {OUTPUT_DIR}/detailed-specifications.md
- Spécifications fonctionnelles complètes
- Modèle de données avec toutes les définitions d'entités
- Layouts de vues (formulaires, grilles, tableaux de bord)
- Workflows de fonctionnalités avec validations
- Sécurité et aspects transversaux
- **Prêt pour**: Conception d'architecture et implémentation

### 3. {OUTPUT_DIR}/epic-us-breakdown.textile
- EPICs avec objectifs et tests d'acceptation
- User Stories avec critères d'acceptation
- Détails techniques d'implémentation (domaines, vues, services)
- Estimations de complexité et dépendances
- Roadmap de développement
- **Prêt pour**: Import Redmine et planification de sprints

---

## Intégration avec le workflow complet

Cette commande couvre la **Phase 1 (Étapes 1-4)** du workflow de développement complet.

### Après avoir terminé /analyze-requirements

Vous aurez:
- ✅ Rapport d'analyse métier avec questions répondues
- ✅ Spécifications fonctionnelles détaillées
- ✅ EPICs et User Stories prêts pour import Redmine

### Continuer avec le développement

**Option 1**: Continuer avec le workflow de développement complet
```
/develop-complete-feature resume from step 5
```

Cela continuera avec:
- Étape 5: Conception d'architecture (architect)
- Étape 6-7: Génération de domaines
- Étape 8-9: Génération de vues
- Étape 10-12: Implémentation de services
- Étape 13-19: Tests, déploiement, documentation

**Option 2**: Continuation manuelle
Utilisez les artefacts générés (`detailed-specifications.md`, `epic-us-breakdown.textile`) pour:
- Conception d'architecture manuelle
- Planification de sprints avec l'équipe de développement
- Gestion du backlog dans Redmine

---

## Quand utiliser cette commande

### ✅ Utilisez `/analyze-requirements` quand:

- Vous démarrez un nouveau module ou fonctionnalité de zéro
- Vous avez un document de spécification écrit (PDF/DOCX/texte)
- Vous avez besoin du workflow complet du besoin aux User Stories
- Vous voulez une analyse structurée avec points de validation
- Vous travaillez sur des besoins complexes nécessitant clarification

### ❌ N'utilisez pas quand:

- Vous avez seulement besoin d'architecture technique (utilisez `architect` directement)
- Vous avez déjà des spécifications détaillées (passez à la Phase 3 avec `agile-agent`)
- Vous faites de la revue de code ou validation (utilisez `code-reviewer`)
- Les besoins sont triviaux (quelques champs sur une entité existante)

---

## Voir aussi

- @agents/business-analyst.md - Documentation agent Phase 1
- @agents/requirements-refiner.md - Documentation agent Phase 2
- @agents/agile-agent.md - Documentation agent Phase 3
- @docs/analysis/large-document-strategy.md - Stratégie pour documents volumineux
- @docs/analysis/question-templates.md - Référence format questions
- @commands/develop-complete-feature.md - Workflow développement complet
