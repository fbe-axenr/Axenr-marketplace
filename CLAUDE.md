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

### Skills AxENR (plugins/axenr/skills/)

| Skill | Role |
|-------|------|
| error-learner | Analyse les erreurs, cree des lecons dans LESSONS-LEARNED.md |
| knowledge-updater | Promeut les lecons confirmees (3+ occurrences) dans CLAUDE.md du projet |
| pre-flight-checker | Charge les lecons pertinentes avant chaque generation de code |
| enr-coherence-checker | Valide la coherence ENR : generique tous types, temporel cycle commercial, reutilisabilite, anti-patterns |
| axenr-dev-validator | Valide les regles dev AxENR : 8 regles d'or, domains, views, actions, Java, i18n, extensions, git |

### Commands AxENR (plugins/axenr/commands/)

| Commande | Usage |
|----------|-------|
| /axenr:solve-ticket | Resoudre 1 ticket autonomement |
| /axenr:solve-batch | Resoudre 2 tickets en parallele |
| /axenr:learn-review | Auditer et consolider les lecons (optionnel, l'auto-learning est integre) |

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

## VERSIONING

Les 2 fichiers suivants DOIVENT etre synchronises :
- `.claude-plugin/marketplace.json` → version du marketplace
- `plugins/axenr/.claude-plugin/plugin.json` → version du plugin

Incrementer la version apres chaque ajout d'agent/skill/command.
Sans increment, les nouvelles commandes ne seront pas detectees par Claude Code.

## REGLES

1. NO EMOJIS in code
2. ENGLISH ONLY for technical names
3. Documentation in French (user-facing) or English (code-facing)
4. Conventional commits for this repo
5. Ne jamais modifier les agents du partenaire (plugins/axelor/) - les surcharger dans axenr/
6. Toujours incrementer la version apres ajout d'un composant
