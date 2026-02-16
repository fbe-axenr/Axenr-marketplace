Resolve the following ticket using the ticket-solver-agent workflow.

## ARGUMENTS

$ARGUMENTS

Expected format: `<project> <branch> #<number> | <title> | <description>`

Examples:
- `axenr-app wip #750 | Add estimated power field | decimal field on Opportunity, calculated from numberOfModules * 400 / 1000`
- `axenr-app dev #733 | Fix project start date | Use current date instead of null in ProjectService`
- `axenr-mobile axenr #801 | Add timesheet duration filter | Filter by duration on TimesheetListScreen`

## PARSING

Parse $ARGUMENTS to extract:
1. **project**: first word (axenr-app or axenr-mobile)
2. **branch**: second word (dev, wip, axenr, or other)
3. **ticket_number**: the #XXX part
4. **title**: text between first and second |
5. **description**: text after second |

If any required field is missing, ASK the developer. Do not guess.

---

## EXECUTION STRICTE - CHECKPOINT SYSTEM

CRITICAL : Chaque phase DOIT etre executee dans l'ordre. Aucune phase ne peut etre sautee ou fusionnee avec une autre.

Apres chaque phase, l'agent DOIT afficher le checkpoint suivant dans le terminal AVANT de passer a la phase suivante :

```
[OK] PHASE <N> TERMINEE : <resume en 1 ligne>
>>  Passage a PHASE <N+1>...
```

SI une phase echoue, l'agent affiche :
```
[ERREUR] PHASE <N> ECHOUEE : <raison>
[PAUSE]  En attente d'instruction du dev...
```

L'agent NE PASSE PAS a la phase suivante tant que la phase courante n'est pas completee avec succes.

---

## PHASE 1 : GIT PULL

**Objectif** : Synchroniser le code local avec la branche cible.

**Actions** :
- Si axenr-app :
  1. `cd <projet>/modules/axenr && git pull origin <branch>`
  2. `cd ../..`
  3. `git pull origin <branch>`
- Si axenr-mobile :
  1. `cd <projet> && git pull origin <branch>`

**Checkpoint** :
```
[OK] PHASE 1 TERMINEE : Code synchronise sur <branch>
>>  Passage a PHASE 2...
```

---

## PHASE 2 : PRE-FLIGHT

**Objectif** : Charger tout le contexte necessaire AVANT de commencer.

**Actions OBLIGATOIRES** (toutes, sans exception) :
1. Lire LESSONS-LEARNED.md du marketplace → extraire lecons pertinentes
2. Lire CLAUDE.md du projet cible → charger les regles du projet
3. Si axenr-app : lire axelor-dev-guide.md
4. Si axenr-app : lire gradle.properties → extraire aopVersion, version projet
5. Si axenr-app : lire gradle/libs.versions.toml → extraire versions AOS, modules enterprise, addons
6. Lire les fichiers i18n existants du projet → inventorier les cles de traduction
7. Identifier le code reutilisable dans le projet (services, composants, methodes)
8. Si repo Axelor de reference disponible (.axelor/) → verifier compatibilite API

**Checkpoint** :
```
[OK] PHASE 2 TERMINEE : Contexte charge
   - Lecons pertinentes : <N>
   - Versions : AOP <version>, AOS <version>
   - Cles i18n existantes : <N>
   - Code reutilisable identifie : <N> elements
>>  Passage a PHASE 3...
```

---

## PHASE 3 : ANALYSE + PLAN

**Objectif** : Analyser le ticket, planifier l'implementation, et obtenir la validation du dev.

**Etape 3.1 : Analyse du ticket**

1. Parser les arguments : projet, branche, numero, titre, description
2. Determiner le type de changement : domain, view, java, mobile, ou mix
3. Lister les fichiers a creer ou modifier
4. Identifier le code existant reutilisable
5. Verifier la compatibilite API avec la version AOS du projet
6. SI information manquante → DEMANDER au dev, ne pas deviner

**Etape 3.2 : Presentation du plan au dev**

CRITICAL : L'agent DOIT presenter le plan et ATTENDRE la confirmation AVANT de continuer.

```
## PLAN - Ticket #<numero> : <titre>

### Contexte
- Projet : <projet> (branche <branche>)
- Type : <domain|view|java|mobile|mix>
- Versions : AOP <version>, AOS <version>, Module <module> <version>

### Ce que je vais faire
1. <action 1> - <fichier concerne>
2. <action 2> - <fichier concerne>
3. ...

### Code existant reutilise
- <service/composant/methode> → <comment reutilise>

### Fichiers concernes
| Fichier | Action | Detail |
|---------|--------|--------|
| path/to/file.xml | Creer / Modifier / Etendre | Description courte |

### Agents utilises
1. <agent-1> → pour <quoi>

### Risques identifies
- <risque si applicable>

### Questions (si info manquante)
- <question si applicable>
```

**Etape 3.3 : Attendre la confirmation**

- ATTENDRE que le dev reponde OK / confirme / valide
- SI le dev demande des modifications → ajuster et re-presenter
- SI le dev dit NON → STOP et demander des precisions
- NE JAMAIS passer a PHASE 3.5 sans confirmation explicite du dev

**Checkpoint** :
```
[OK] PHASE 3 TERMINEE : Plan valide par le dev
   - Type : <type>
   - Fichiers : <N> a creer, <N> a modifier
   - Code reutilise : <N> elements
>>  Passage a PHASE 3.5...
```

---

## PHASE 3.5 : ANALYSE CRITIQUE DU CODE EXISTANT

**Objectif** : Analyser le code existant AVANT de generer quoi que ce soit pour connaitre le terrain et eviter de casser ou toucher du code inutilement.

CRITICAL : Cette phase est OBLIGATOIRE. Elle ne peut PAS etre sautee.

**Actions** :

1. **Identifier les fichiers existants a analyser** : tous les fichiers du projet qui seront modifies ou etendus (PAS les fichiers a creer)

2. **Lancer `axelor:analyze-code`** sur ces fichiers existants
   - L'agent DOIT appeler le skill axelor:analyze-code (axelor:code-analyzer agent)
   - L'analyse porte sur le code EXISTANT, pas sur le code a generer

3. **Extraire les points critiques** du rapport d'analyse :
   - Issues CRITICAL → **ZONES INTERDITES** : ne pas toucher ces lignes
   - Issues HIGH → **ZONES FRAGILES** : prudence maximale si on doit les modifier
   - Bad practices existantes → ne pas les reproduire, ne pas les corriger non plus (hors scope)
   - Dependencies critiques → code appele par d'autres modules, ne pas casser les signatures

4. **Produire le RAPPORT DE TERRAIN** :

```
## RAPPORT DE TERRAIN - Analyse pre-generation

### ZONES INTERDITES (ne pas toucher)
- <fichier>:<lignes> → CRITICAL: <description> → NE PAS MODIFIER
- ...

### ZONES FRAGILES (prudence)
- <Service.java> → methode X() appellee par Y et Z → garder la signature intacte
- ...

### POINTS D'ATTENTION
- Pattern observe : <pattern> → le respecter dans le code genere
- Convention locale : <convention> → s'y conformer
- ...

### PERIMETRE AUTORISE
- Fichiers a creer : <liste>
- Fichiers a modifier : <liste avec sections precises>
- Fichiers a NE PAS TOUCHER : <liste>
```

5. **Presenter le rapport au dev** pour validation du perimetre

6. **Verrouiller** : ce rapport devient la contrainte pour TOUTES les phases suivantes. L'agent ne peut PAS modifier un fichier hors du PERIMETRE AUTORISE.

**SI l'analyse est impossible** (fichiers introuvables, aucun fichier existant a analyser car tout est nouveau) → signaler au dev et demander s'il veut continuer sans analyse.

**Checkpoint** :
```
[OK] PHASE 3.5 TERMINEE : Terrain analyse
   - Zones interdites : <N>
   - Zones fragiles : <N>
   - Perimetre autorise : <N> fichiers
   - Rapport valide par le dev
>>  Passage a PHASE 4...
```

---

## PHASE 4 : GENERATION

**Objectif** : Generer le code en respectant le plan ET le rapport de terrain.

CRITICAL : AVANT de generer la moindre ligne, consulter le RAPPORT DE TERRAIN de PHASE 3.5 :
- Ne JAMAIS modifier les ZONES INTERDITES
- Respecter les signatures des ZONES FRAGILES
- Suivre les conventions identifiees dans POINTS D'ATTENTION
- Ne generer que dans le PERIMETRE AUTORISE

**Pour axenr-app** : appeler les agents dans cet ordre strict :
1. **domain-agent** (si domains concernes) → XSD version AOP
2. **view-agent** (si vues concernees) → XSD version AOP + check i18n
3. **java-agent** (si Java concerne) → check API version AOS

**Pour axenr-mobile** : generer directement (TSX, Redux, API calls, types)

**Regles** :
- Suivre TOUTES les regles du CLAUDE.md du projet
- Reutiliser le code existant identifie en PHASE 3
- Verifier les cles i18n avant d'en creer de nouvelles
- Utiliser le XSD correspondant a la version AOP
- Code senior : concis, robuste, lisible, performant

**Checkpoint** :
```
[OK] PHASE 4 TERMINEE : Code genere
   - Fichiers crees : <liste>
   - Fichiers modifies : <liste>
   - Agents utilises : <liste>
   - Perimetre respecte : OUI/NON
>>  Passage a PHASE 5...
```

---

## PHASE 5 : VALIDATION

**Objectif** : Valider le code genere avec les agents partenaire ET les skills AxENR.

3 etapes OBLIGATOIRES dans cet ordre. Aucune etape ne peut etre sautee.

**Etape 5.1 : Charger les lecons** (OBLIGATOIRE)
1. Lire LESSONS-LEARNED.md
2. Separer en enr_lessons (type enr) et dev_lessons (type domain/view/java/etc.)
3. Calculer le reinforcement_level (1 occ → severite originale, 2+ → +1 niveau, 3+ promu → CRITICAL)

**Etape 5.2 : Appeler les agents de validation** (OBLIGATOIRE)

Etape A - Agents partenaire Axelor :
| Ordre | Agent | Quand |
|-------|-------|-------|
| 1 | axelor-xml-validator | SI fichiers XML modifies |
| 2 | axelor-view-semantic-validator | SI fichiers views modifies |
| 3 | axelor-java-style-validator | SI fichiers Java modifies |
| 4 | axelor-naming-checker | TOUJOURS |
| 5 | code-reviewer | TOUJOURS |
| 6 | code-analyzer | TOUJOURS |

Pour axenr-mobile, seuls naming-checker + code-reviewer + code-analyzer.

Etape B - Skills AxENR (EN PARALLELE, avec resultats agents) :
| Skill | Recoit | Seuil |
|-------|--------|-------|
| enr-coherence-checker | violations agents + enr_lessons | Score >= 70 |
| axenr-dev-validator | violations TOUS agents + dev_lessons | Score >= 70 |

Etape C - MERGE et DEDUPLICATION de toutes les violations.

**Etape 5.3 : Build de verification** (OBLIGATOIRE)
- axenr-app : `./gradlew build`
- axenr-mobile : `yarn build && yarn lint`

**Checkpoint** :
```
[OK] PHASE 5 TERMINEE : Validation effectuee
   - Agents appeles : <liste>
   - Violations CRITICAL : <N>
   - Violations HIGH : <N>
   - Violations MEDIUM/LOW : <N>
   - Build : OK/KO
>>  Passage a PHASE 6...
```

---

## PHASE 6 : CORRECTION + APPRENTISSAGE (max 3 iterations)

**Objectif** : Corriger les issues CRITICAL/HIGH et enregistrer les lecons.

Pour chaque issue CRITICAL ou HIGH :
1. Analyser l'erreur (message, fichier, ligne, source)
2. Appeler **error-learner** → enregistrer/incrementer dans LESSONS-LEARNED.md
3. Appliquer le fix dans le code du projet
4. Appeler **knowledge-updater** → promouvoir dans CLAUDE.md si 3+ occurrences
5. Re-lancer PHASE 5

SI apres 3 iterations il reste des CRITICAL → STOP avec rapport d'erreur detaille.

**Checkpoint** :
```
[OK] PHASE 6 TERMINEE : Corrections appliquees
   - Iterations : <N>/3
   - CRITICAL restantes : 0
   - Lecons enregistrees : <N>
   - Lecons promues : <N>
>>  Passage a PHASE 7...
```

---

## PHASE 7 : BUILD

**Objectif** : Build complet du projet.

- axenr-app : `./gradlew clean generateCode copyWebapp build`
- axenr-mobile : `yarn build && yarn lint`

SI le build echoue :
1. Parser l'erreur
2. Verifier si c'est lie a une incompatibilite de version (libs.versions.toml)
3. Appeler error-learner
4. Appliquer le fix
5. Re-lancer le build (compteur partage avec PHASE 6, max 3 total)

**Checkpoint** :
```
[OK] PHASE 7 TERMINEE : Build reussi
   - Commande : <commande executee>
   - Resultat : BUILD SUCCESSFUL
>>  Passage a PHASE 8...
```

---

## PHASE 8 : LIVRAISON

**Objectif** : Produire le rapport final et le test plan.

1. Generer le TEST PLAN (template test-plan-template.md)
2. Lister tous les fichiers modifies avec leur chemin complet
3. Resumer ce qui a ete fait en 3-5 lignes
4. Indiquer le code reutilise vs le code cree
5. Rapport de compatibilite versions (AOP, AOS, modules, risques montee)
6. Afficher le tout dans le terminal
7. Ne PAS commit, ne PAS push, ne PAS creer de branche

**Checkpoint final** :
```
[OK] PHASE 8 TERMINEE : Livraison complete
   - Fichiers modifies : <N>
   - Tests plan : genere
   - Build : SUCCESSFUL
[OK] TICKET #<numero> RESOLU
```

---

## RESUME DES PHASES (CHECKLIST)

L'agent DOIT suivre cette checklist exacte, dans cet ordre, sans sauter aucune etape :

```
[ ] PHASE 1  : GIT PULL         → Synchroniser le code
[ ] PHASE 2  : PRE-FLIGHT       → Charger contexte (lecons, versions, i18n, code reutilisable)
[ ] PHASE 3  : ANALYSE + PLAN   → Analyser le ticket + presenter le plan + ATTENDRE validation dev
[ ] PHASE 3.5: ANALYSE CRITIQUE → Lancer axelor:analyze-code sur code existant + rapport de terrain
[ ] PHASE 4  : GENERATION       → Generer le code dans le perimetre autorise uniquement
[ ] PHASE 5  : VALIDATION       → Agents partenaire + skills AxENR + build verification
[ ] PHASE 6  : CORRECTION       → Fix CRITICAL/HIGH + error-learner + knowledge-updater
[ ] PHASE 7  : BUILD            → Build complet du projet
[ ] PHASE 8  : LIVRAISON        → Test plan + rapport final
```

---

## CRITICAL RULES

- JAMAIS sauter une phase ou fusionner des phases ensemble
- JAMAIS passer a la phase suivante sans avoir affiche le checkpoint de la phase courante
- JAMAIS generer du code sans avoir analyse le code existant (PHASE 3.5)
- JAMAIS generer du code sans la validation du plan par le dev (PHASE 3.3)
- JAMAIS modifier un fichier hors du PERIMETRE AUTORISE (PHASE 3.5)
- JAMAIS supprimer du code existant
- JAMAIS renommer un element existant
- JAMAIS modifier du code non demande par le ticket
- JAMAIS ecrire des commentaires dans le code genere
- JAMAIS creer des cles i18n en doublon
- JAMAIS utiliser des API deprecees
- JAMAIS deviner une information manquante
- Le code genere DOIT etre de qualite senior
- Les lecons sont ecrites dans le marketplace UNIQUEMENT, jamais dans le projet
