# CLAUDE.md - AxENR Marketplace

> Marketplace interne AxENR - Systeme d'agents auto-apprenants
> Author: Fadel Benomar - Developer Backend & IA @ AxENR

---

## ARCHITECTURE

```
axenr-marketplace/
├── .claude-plugin/
│   └── marketplace.json              # Registre central (version source of truth)
├── plugins/
│   ├── axenr/                        # Plugin AxENR (nos agents maison)
│   │   ├── agents/                   # Agents autonomes AxENR
│   │   ├── skills/                   # Skills specialises AxENR
│   │   ├── commands/                 # Slash commands AxENR
│   │   ├── docs/lessons/             # LESSONS-LEARNED.md (memoire)
│   │   └── templates/                # Templates de sortie
├── docs/                             # Documentation marketplace
├── README.md                         # Installation et usage
└── CONTRIBUTING.md                   # Guide ajout d'agents
```

## AGENTS DISPONIBLES

### Agents AxENR (plugins/axenr/) - nos agents maison

| Agent | Role |
|-------|------|
| ticket-solver-agent | Resolution autonome de tickets avec auto-apprentissage |
| erp-consultant-enr | Consultant ERP senior ENR - Challenge et valide la coherence metier (genericite, temporalite, reutilisabilite) |
| pr-reviewer-axenr | Review PR AxENR : delegue a axelor:code-reviewer + checks specifiques (branding, submodule, lecons apprises, no-emoji, no-comment) |
| import-export-agent | Expert 100% import/export Axelor - Read-only sur le projet, produit Excel/CSV/guides dans ~/Downloads. Modes prepare / core-model / company-create / debug |
| axenr-template-expert | Expert senior templates Word XDocReport pour Axelor/AxENR (contrats, attestations, mandats Enedis/GRD, fiches collecte, CARD-I). Livre .docx prets a l'import Axelor dans ~/Downloads |
| axenr-bi-architect | Architecte BI senior pour Axelor/AxENR + Apache Superset. Requetes SQL PostgreSQL + dashboards. 940 tables, 21 815 champs. KPIs commercial/financier/operationnel/ENR. Detecte le client courant via cwd |

### Skills AxENR (plugins/axenr/skills/)

| Skill | Role |
|-------|------|
| error-learner | Analyse les erreurs, delegue a lesson-deduplicator, cree/incremente les lecons |
| lesson-deduplicator | Matching semantique multi-axes (rule_id, signature, Levenshtein, keywords) pour eviter les doublons de lecons |
| knowledge-updater | Promeut les lecons confirmees (3+ occurrences) dans CLAUDE.md du projet |
| pre-flight-checker | Charge les lecons pertinentes avant chaque generation de code |
| enr-coherence-checker | Valide la coherence ENR : generique tous types, temporel cycle commercial, reutilisabilite, anti-patterns |
| axenr-dev-validator | Valide les regles dev AxENR : 8 regles d'or, domains, views, actions, Java, i18n, extensions, git |
| migration-validator | Valide les migrations de donnees/schemas |
| marketplace-doctor | Audite la sante du marketplace (versions sync, frontmatters, refs, doublons, lecons stagnantes) |
| import-schema-catalog | Catalogue de reference des schemas d'import Axelor (10 feuilles fournisseurs, AccountType FRA_PCG, conventions chart-config.xml) |
| template-expert-catalog | Catalogue de reference pour axenr-template-expert (patterns XDocReport, pieges, modeles racines, 77 champs + 39 techniques, contournement Groovy 3+ niveaux) |
| client-context-detector | Detecte le client AxENR depuis le cwd (axenr-app / systeko-app / planeteenr-app / emeraude-solaire-app / synambu / energ-ia / yooz) et charge les ressources specifiques |
| bi-templates-catalog | Catalogue BI pour axenr-bi-architect (10 templates SQL pretes, KPIs strategique/tactique/operationnel/ENR, bonnes pratiques Superset, modele de donnees Axelor detaille par domaine) |

### Commands AxENR (plugins/axenr/commands/)

| Commande | Usage |
|----------|-------|
| /axenr:solve-ticket | Resoudre 1 ticket autonomement |
| /axenr:solve-batch | Resoudre 2 tickets en parallele |
| /axenr:learn-review | Auditer et consolider les lecons (legacy, utiliser /axenr:consolidate-lessons) |
| /axenr:review-pr | Review une PR avec pr-reviewer-axenr + axelor:code-reviewer partenaire |
| /axenr:doctor | Audit de sante du marketplace |
| /axenr:consolidate-lessons | Fusionne les lecons dupliquees, depile REVIEW QUEUE, declenche les promotions |
| /axenr:sync-lessons | Curator model : pousse les LOCAL-LESSONS-<hostname>.md vers LESSONS-LEARNED.md via PR |
| /axenr:bump-version | Bump version synchronise marketplace.json + plugin.json (patch/minor/major/auto) |
| /axenr:import-help | Lance import-export-agent pour preparer/corriger un import Axelor (read-only projet, outputs dans ~/Downloads) |
| /axenr:template-expert | Lance axenr-template-expert pour creer/modifier/debuger un template Word XDocReport (read-only projet, .docx dans ~/Downloads) |
| /axenr:bi-architect | Lance axenr-bi-architect pour construire requetes SQL + dashboards Superset (read-only projet, SQL/MD dans ~/Downloads) |

### Agents Axelor Partenaire (plugins/axelor/) - v2.5.0

| Agent | Role |
|-------|------|
| domain-agent | Generation domains XML |
| view-agent | Generation vues XML |
| java-agent | Generation code Java |
| code-reviewer | Revue qualite code (CRITICAL/HIGH/MEDIUM/LOW) |
| code-analyzer | Conformite, optimisations, securite |
| architect | Architecture technique |
| business-analyst | Analyse des besoins |
| agile-agent | Generation EPICs et User Stories |
| test-agent | Generation tests unitaires |
| git-agent | Operations Git avec validation |
| redmine-agent | Analyse tickets Redmine |
| repo-setup-agent | Setup des repos de reference |
| cicd-agent | Configuration CI/CD |
| doc-synthesis-agent | Synthese documentation |
| functional-validator | Validation fonctionnelle |
| spec-inspector | Inspection des specifications |
| requirements-refiner | Affinage des specifications |
| aos-analyzer | Analyse gap AOS |

### Skills Axelor Partenaire (32+ skills)

axelor-xml-validator, axelor-view-semantic-validator, axelor-java-style-validator,
axelor-naming-checker, axelor-semantic-validator, axelor-view-extension-validator,
aos-documentation-fetcher, aos-entity-searcher, aos-field-comparator,
axelor-controller-method-extractor, axelor-er-diagram-generator,
commitlint-validator, commitlint-config-generator, file-safety-checker,
functional-spec-consistency-checker, functional-spec-synthesis,
git-cliff-config-generator, gitlab-ci-generator, mr-title-validator,
pipeline-troubleshooter, pr-analyzer, quality-gate-configurator,
requirements-registry-builder, technical-architecture-synthesis,
ticket-deep-analyzer, ticket-duplicate-detector, us-dependency-mapper,
us-quality-validator, ci-validation-script-generator, etc.

## PROJETS CIBLES

| Projet | Repo | Techno | Branche de travail |
|--------|------|--------|--------------------|
| axenr-app | axenr-app (+ submodule modules/axenr) | Axelor AOP 7.4.7, Java 11, Gradle | dev, wip, ou autre (passe en argument) |
| axenr-mobile | axenr-mobile | React Native 0.75.5, TypeScript, Redux | axenr |

## SEPARATION DES RESPONSABILITES

| Ce repo (marketplace) | Le projet (axenr-app / axenr-mobile) |
|------------------------|--------------------------------------|
| Agents, skills, commands | Code metier |
| LESSONS-LEARNED.md | Domains, views, Java, TSX |
| Templates | Configs, builds |
| Intelligence et memoire | Aucun fichier de l'agent |

## MODELE DE LECONS PARTAGEES (Curator Model - Option A)

Deux fichiers coexistent dans `plugins/axenr/docs/lessons/` :

| Fichier | Scope | Git |
|---------|-------|-----|
| LESSONS-LEARNED.md | Equipe (source de verite) | Commite |
| LOCAL-LESSONS-<hostname>.md | Local par poste | Gitignore |

### Flow

```
1. L'agent apprend une erreur -> error-learner ecrit dans LOCAL-LESSONS-<hostname>.md
   (IDs: LESSON-LOCAL-NNN, ne conflit jamais avec les IDs globaux)

2. pre-flight-checker lit UNION(LOCAL, SHARED) pour chaque generation
   -> le dev beneficie immediatement de ses propres lecons

3. Periodiquement (ou sur demande) :
   /axenr:sync-lessons [--dry-run] [--auto-pr]
   -> applique lesson-deduplicator contre SHARED
   -> fusionne / ajoute
   -> ouvre une PR sur une branche lessons/sync-<hostname>-YYYYMMDD

4. Le curateur (Fabien / toi) review la PR et merge

5. Les autres devs recuperent les lecons via /plugin update
```

### Pourquoi pas de push automatique

- Le curateur garde la main sur la qualite des lecons promues en "loi d'equipe"
- Pas de conflit Git (branches separees par hostname, append-only dans LESSONS-LEARNED.md)
- Les lecons sont testees localement avant d'etre partagees

L'agent LIT le projet pour generer du code.
L'agent ECRIT ses lecons dans le marketplace uniquement.
L'agent ne depose AUCUN fichier dans le projet sauf le code demande.

## AGENTS PARTENAIRE

Les agents Axelor (v2.5.0) sont inclus directement dans `plugins/axelor/`.
Source : Axelor AI Team (`git@git.axelor.com:ia-tools/axelor-claude-marketplace.git`)

### Mise a jour du partenaire

1. Telecharger la nouvelle version depuis le repo Axelor
2. Remplacer le contenu de `plugins/axelor/`
3. Mettre a jour la version dans `.claude-plugin/marketplace.json`
4. Commit et push

## VERSIONING ET AUTO-UPDATE

Les 2 fichiers suivants DOIVENT etre synchronises :
- `.claude-plugin/marketplace.json` → version du marketplace
- `plugins/axenr/.claude-plugin/plugin.json` → version du plugin

### Trois facons de bumper

1. Automatique via GitHub Action (recommande) :
   A chaque push sur main avec des modifs dans plugins/axenr/, le workflow
   `.github/workflows/release.yml` :
   - detecte le type de bump via conventional commits (feat=minor, fix=patch, BREAKING=major)
   - bumpe marketplace.json + plugin.json
   - commit "chore(release): bump axenr plugin to vX.Y.Z"
   - tag vX.Y.Z
   - cree une GitHub Release

2. Commande Claude Code :
   `/axenr:bump-version [patch|minor|major|auto]`

3. Script local :
   `./scripts/bump-version.sh [patch|minor|major|auto]`

### CI de garde-fou

`.github/workflows/ci.yml` refuse tout PR qui modifie `plugins/axenr/` sans
bumper la version. Plus d'oubli silencieux.

### Cote utilisateur (mise a jour du plugin)

Apres un bump + push :
```
/plugin marketplace update fbe-axenr-Axenr-marketplace
/plugin update axenr@fbe-axenr-Axenr-marketplace
```

### Marketplace Doctor

`/axenr:doctor` ou `python3 scripts/marketplace-doctor.py --strict` verifie :
- sync des versions
- frontmatters valides (name, description)
- references agents/skills/commands coherentes
- pas de doublon de nom
- pas d'emoji (regle AxENR)
- lecons stagnantes (>30 jours)

## REGLES

1. NO EMOJIS in code
2. ENGLISH ONLY for technical names
3. Documentation in French (user-facing) or English (code-facing)
4. Conventional commits for this repo
5. Ne jamais modifier les agents du partenaire (plugins/axelor/) - les surcharger dans axenr/
6. Toujours incrementer la version apres ajout d'un composant
