# LESSONS-LEARNED.md

> Base de connaissances auto-alimentee par le ticket-solver-agent
> Derniere mise a jour : 2026-02-14

---

## STATS

| Metrique | Valeur |
|----------|--------|
| Total lecons | 55 |
| Lecons promues dans CLAUDE.md | 0 |
| Lecons en attente | 55 |
| Taux de promotion | 0% |

---

## FORMAT

```
### LESSON-XXX : <titre court>
- **Type** : domain | view | action | java | build | version | mobile | naming | i18n | rest | migration | enr
- **Projet** : axenr-app | axenr-mobile | both
- **Erreur** : description du pattern d'erreur
- **Correction** : comment corriger
- **Occurrences** : N
- **Tickets** : #XXX, #YYY
- **Promu** : false | true
```

---

## ERREURS DOMAINS

### LESSON-001 : Reference relationnelle sans package complet
- **Type** : domain
- **Projet** : axenr-app
- **Erreur** : Utiliser `ref="Company"` au lieu du chemin complet dans many-to-one/one-to-many
- **Correction** : Toujours utiliser `ref="com.axelor.apps.base.db.Company"` avec le package complet
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-002 : One-to-many sans mappedBy
- **Type** : domain
- **Projet** : axenr-app
- **Erreur** : Declarer un one-to-many sans `mappedBy`, ce qui cree une table de jointure inutile
- **Correction** : Toujours ajouter `mappedBy="parentField"` et creer le many-to-one inverse dans l'entite enfant
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-003 : Boolean avec title
- **Type** : domain
- **Projet** : axenr-app
- **Erreur** : Mettre `title="..."` sur un champ boolean. Axelor ignore le title et genere le label depuis le nom du champ
- **Correction** : Ne JAMAIS mettre de title sur un boolean. Bien nommer le champ (ex: `isProjectNotMandatory`) et utiliser `./gradlew i18n` pour generer la cle
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-004 : Boolean sans default
- **Type** : domain
- **Projet** : axenr-app
- **Erreur** : Declarer un boolean sans `default="false"` ou `default="true"` explicite
- **Correction** : Toujours mettre `default="false"` (ou `default="true"`) sur les champs boolean
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-005 : Selection sans extra-code constantes
- **Type** : domain
- **Projet** : axenr-app
- **Erreur** : Declarer un champ `selection="xxx.select"` sans definir les constantes correspondantes dans `extra-code`
- **Correction** : Toujours ajouter un bloc `<extra-code>` avec `public static final int STATUS_XXX = N;` pour chaque valeur de la selection
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-006 : Repository cree manuellement
- **Type** : domain
- **Projet** : axenr-app
- **Erreur** : Creer manuellement un fichier Repository Java. Les repositories sont auto-generes par `./gradlew generateCode`
- **Correction** : Ne jamais creer de repository manuellement. Utiliser `./gradlew generateCode` et le fichier sera dans `build/src-gen/`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-007 : Panel principal avec title
- **Type** : domain
- **Projet** : axenr-app
- **Erreur** : Mettre `title="Main"` sur le panel principal d'un formulaire
- **Correction** : Le panel principal (`mainPanel`) ne doit PAS avoir de title
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS VIEWS

### LESSON-008 : Champ relationnel sans form-view/grid-view
- **Type** : view
- **Projet** : axenr-app
- **Erreur** : Declarer un champ many-to-one ou many-to-many sans `form-view` et `grid-view`
- **Correction** : Toujours specifier `form-view="xxx-form" grid-view="xxx-grid"` sur les champs relationnels
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-009 : Elements XML sans name
- **Type** : view
- **Projet** : axenr-app
- **Erreur** : Declarer des panels ou boutons sans attribut `name`, ce qui empeche les extensions
- **Correction** : TOUJOURS nommer les panels (`name="xxxPanel"`), boutons (`name="xxxBtn"`) et autres elements
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-010 : O2M affiche avec field au lieu de panel-related
- **Type** : view
- **Projet** : axenr-app
- **Erreur** : Utiliser `<field name="lineList"/>` pour afficher un one-to-many
- **Correction** : Utiliser `<panel-related field="lineList" form-view="xxx-form" grid-view="xxx-grid"/>` pour les O2M
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-011 : Extension sans id="axenr-..." et extension="true"
- **Type** : view
- **Projet** : axenr-app
- **Erreur** : Etendre une vue sans le pattern AxENR : `id="axenr-xxx"` + `extension="true"`
- **Correction** : Toujours utiliser `<form id="axenr-xxx-form" name="xxx-form" ... extension="true">`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-012 : SchemaLocation sur 2 lignes
- **Type** : view
- **Projet** : axenr-app
- **Erreur** : Ecrire `xsi:schemaLocation` sur 2 lignes dans les fichiers XML de vues
- **Correction** : Toujours mettre le schemaLocation sur 1 seule ligne
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-013 : Combiner move et insert dans un seul extend
- **Type** : view
- **Projet** : axenr-app
- **Erreur** : Combiner `<move>` et `<insert>` dans un seul `<extend>`, ce qui fait que l'element insere se retrouve apres les elements deplaces
- **Correction** : Separer en 2 extends distincts : un pour les moves, un pour les inserts
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS ACTIONS

### LESSON-014 : Expression sans eval:
- **Type** : action
- **Projet** : axenr-app
- **Erreur** : Ecrire `expr="__date__"` sans le prefixe `eval:` dans les action-record
- **Correction** : Toujours ecrire `expr="eval: __date__"`, `expr="eval: __repo__(Model).CONSTANT"`, etc.
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-015 : Caracteres speciaux non echappes dans XML
- **Type** : action
- **Projet** : axenr-app
- **Erreur** : Utiliser `&&`, `>`, `<` dans les attributs XML au lieu de `&amp;&amp;`, `&gt;`, `&lt;`
- **Correction** : Toujours echapper : `&amp;` pour &, `&lt;` pour <, `&gt;` pour >, `&quot;` pour "
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-016 : Null safety manquante dans expressions
- **Type** : action
- **Projet** : axenr-app
- **Erreur** : Ecrire `partner.address.city` sans `?.` dans les expressions XML, causant NullPointerException
- **Correction** : Toujours utiliser `partner?.address?.city` avec l'operateur null-safe
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-017 : Action-view admin avec mauvais nommage
- **Type** : action
- **Projet** : axenr-app
- **Erreur** : Nommer une action-view admin `action.xxx` au lieu de `admin.xxx`
- **Correction** : Utiliser le format `admin.xxx` pour les action-views d'administration
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-018 : onChange ecrase sans preserver l'existant
- **Type** : action
- **Projet** : axenr-app
- **Erreur** : Remplacer un onChange existant au lieu de l'etendre
- **Correction** : Ne jamais ecraser un onChange. Ajouter la nouvelle action dans le group existant ou en creer un nouveau qui inclut l'ancien
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS JAVA

### LESSON-019 : @Transactional manquant sur methode avec save
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Methode qui appelle `repo.save()` sans `@Transactional`, pas de rollback si exception
- **Correction** : Ajouter `@Transactional(rollbackOn = {Exception.class})` sur toute methode qui fait un save
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-020 : Controller sans try-catch + TraceBackService
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Controller sans `try-catch` avec `TraceBackService.trace(response, e)`, retourne erreur 500 brute
- **Correction** : Toujours wrapper le corps du controller dans `try { ... } catch (Exception e) { TraceBackService.trace(response, e); }`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-021 : Objet contexte sauvegarde directement
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Sauvegarder directement l'objet obtenu via `request.getContext().asType()` sans le recharger depuis la base
- **Correction** : Toujours recharger avec `repo.find(obj.getId())` avant de sauvegarder. L'objet contexte n'est pas attache a Hibernate
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-022 : Messages non traduits avec I18n.get()
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Utiliser des strings en dur dans les exceptions/messages au lieu de `I18n.get(ExceptionMessage.XXX)`
- **Correction** : Creer des constantes dans `ExceptionMessage` avec le pattern `/*$$(*/  "text" /*)*/` et utiliser `I18n.get()`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-023 : @Inject inutile pour methodes statiques
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Injecter via `@Inject` une classe dont on utilise uniquement des methodes statiques (ex: `MetaFiles.getPath()`)
- **Correction** : Appeler directement les methodes statiques sans injection : `MetaFiles.getPath(metaFile).toFile()`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-024 : Commentaires dans le code genere
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Ajouter des commentaires dans le code genere. Le code doit etre auto-documente
- **Correction** : ZERO commentaire dans le code. Si le code a besoin d'un commentaire, il doit etre refactorise pour etre plus clair
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-025 : Beans.get() dans un Service
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Utiliser `Beans.get(Service.class)` dans un service au lieu de `@Inject`
- **Correction** : `Beans.get()` est OK dans les Controllers uniquement. Dans les Services, utiliser `@Inject` sur champ ou constructeur
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-026 : Wildcard imports
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Utiliser `import com.axelor.xxx.*;` (wildcard imports)
- **Correction** : Toujours utiliser des imports explicites, un par classe
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-027 : Noms francais dans le code
- **Type** : java
- **Projet** : both
- **Erreur** : Utiliser des mots francais dans les noms de code (panels, actions, champs, variables)
- **Correction** : ENGLISH ONLY pour tous les noms techniques
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-028 : SecurityCheck avec ID
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Utiliser `new SecurityCheck().readAccess(Class, id)` avec un parametre ID
- **Correction** : Utiliser `new SecurityCheck().writeAccess(Class).createAccess(Class).check()` avec Class seulement, pas (Class, id)
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS BUILD

### LESSON-029 : generateCode en minuscules
- **Type** : build
- **Projet** : axenr-app
- **Erreur** : Ecrire `generatecode` ou `copywebapp` en minuscules dans la commande gradle
- **Correction** : Respecter la casse : `generateCode` et `copyWebapp` (camelCase)
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-030 : Version Java modifiee dans build.gradle
- **Type** : build
- **Projet** : axenr-app
- **Erreur** : Modifier `languageVersion` dans `build.gradle`. Le projet DOIT rester en Java 11
- **Correction** : Ne JAMAIS modifier `JavaLanguageVersion.of(11)` dans build.gradle
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS VERSION

### LESSON-031 : Versions enterprise modules non individuelles
- **Type** : version
- **Projet** : axenr-app
- **Erreur** : Supposer que tous les modules enterprise ont la meme version AOS. Chaque module peut avoir une version differente
- **Correction** : Lire `libs.versions.toml` et verifier la version INDIVIDUELLE de chaque module (axelor-intervention=8.5.11, axelor-business-support=8.5.5, etc.)
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-032 : XSD version non alignee avec AOP
- **Type** : version
- **Projet** : axenr-app
- **Erreur** : Utiliser une version XSD qui ne correspond pas a la version AOP
- **Correction** : AOP 7.x → XSD 7.1, AOP 8.x → XSD 8.0. Verifier dans gradle.properties pour aopVersion
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS NAMING

### LESSON-033 : Menuitem admin avec prefixe axenr-
- **Type** : naming
- **Projet** : axenr-app
- **Erreur** : Nommer un menuitem admin `axenr-xxx-admin` au lieu de `xxx-admin`
- **Correction** : Les menuitems admin ne prennent PAS le prefixe `axenr-`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-034 : Element existant renomme
- **Type** : naming
- **Projet** : axenr-app
- **Erreur** : Renommer un panel, action ou champ existant (ex: `extraPanel` → `technicalSpecsPanel`)
- **Correction** : Ne JAMAIS renommer un element existant. Les extensions qui y font reference par nom seront cassees
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS I18N

### LESSON-035 : Cle ajoutee dans messages.csv manuellement
- **Type** : i18n
- **Projet** : axenr-app
- **Erreur** : Ajouter manuellement une cle dans `messages.csv`. Ce fichier est GENERE par `./gradlew i18n`
- **Correction** : Ajouter le title en anglais dans le domain, lancer `./gradlew i18n`, puis ajouter la traduction FR dans `messages_fr.csv`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-036 : Doublon de traductions
- **Type** : i18n
- **Projet** : axenr-app
- **Erreur** : Creer 2 cles similaires (`"View Equipment"` ET `"View Equipments"`) au lieu d'une seule
- **Correction** : Verifier les cles existantes dans les fichiers i18n AVANT de creer une nouvelle cle. Harmoniser sur un seul libelle
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-037 : custom_fr.csv pour cle presente dans le code
- **Type** : i18n
- **Projet** : axenr-app
- **Erreur** : Ajouter dans `custom_fr.csv` une cle qui est deja dans le code source
- **Correction** : `custom_fr.csv` est UNIQUEMENT pour les cles NON presentes dans le code (labels dynamiques, donnees importees). Les cles du code vont dans `messages_fr.csv`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-061 : Editer messages_fr.csv AVANT d'avoir lance ./gradlew i18n
- **Type** : i18n
- **Projet** : axenr-app
- **Erreur** : Editer `messages_fr.csv` pour ajouter une traduction SANS avoir lance `./gradlew i18n` d'abord. La nouvelle cle n'existe pas encore dans le fichier
- **Correction** : Workflow OBLIGATOIRE : 1) Ajouter le champ/message avec cle EN dans le code 2) Lancer `./gradlew i18n -p modules/axenr` 3) Verifier que la cle apparait dans `messages.csv` 4) PUIS editer `messages_fr.csv` pour la traduction FR
- **Occurrences** : 1
- **Tickets** : confirmed-by-dev
- **Promu** : false

---

## ERREURS SCOPE TICKET

### LESSON-062 : Supprimer du code existant (doublons inclus)
- **Type** : view
- **Projet** : both
- **Erreur** : Supprimer du code existant lors d'un ticket, meme s'il semble inutile ou en doublon (ex: supprimer un `<field>` en double, supprimer une action obsolete, supprimer un import inutilise)
- **Correction** : Ne JAMAIS supprimer du code existant. Le ticket doit contenir UNIQUEMENT les ajouts/modifications demandes. Les doublons existants sont laisses en l'etat. Seul un ticket de nettoyage dedie peut supprimer du code
- **Occurrences** : 1
- **Tickets** : confirmed-by-dev
- **Promu** : false

### LESSON-063 : Modifier du code non demande par le ticket
- **Type** : view
- **Projet** : both
- **Erreur** : Profiter d'un ticket pour renommer des elements, corriger des doublons, refactorer du code voisin, nettoyer des imports, harmoniser des conventions dans des fichiers non concernes par le ticket
- **Correction** : Le commit doit contenir STRICTEMENT ce que le ticket demande. Aucun renommage, aucun nettoyage, aucune correction hors scope. Si un probleme est detecte, le signaler au dev sans le corriger
- **Occurrences** : 1
- **Tickets** : confirmed-by-dev
- **Promu** : false

---

## ERREURS REST

### LESSON-038 : @Path sans slash initial
- **Type** : rest
- **Projet** : axenr-app
- **Erreur** : Ecrire `@Path("aos/xxx/")` sans slash initial et avec trailing slash
- **Correction** : Toujours `@Path("/aos/xxx")` avec slash initial, sans trailing slash
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-039 : ResponseConstructor pour HTML
- **Type** : rest
- **Projet** : axenr-app
- **Erreur** : Utiliser `ResponseConstructor.build()` pour retourner du HTML
- **Correction** : Utiliser `Response.ok(content).header("Content-Type", "text/html; charset=UTF-8").build()` pour HTML. `ResponseConstructor` est pour JSON
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS MOBILE

### LESSON-040 : Hook dans une condition
- **Type** : mobile
- **Projet** : axenr-mobile
- **Erreur** : Utiliser un hook React (`useSelector`, `useState`, etc.) a l'interieur d'une condition ou boucle
- **Correction** : Les hooks doivent TOUJOURS etre au top level du composant, jamais dans des conditions ou boucles
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-041 : Fonctions inline dans les props
- **Type** : mobile
- **Projet** : axenr-mobile
- **Erreur** : Passer des fonctions anonymes inline dans les props (`renderItem={({ item }) => ...}`)
- **Correction** : Utiliser `useCallback` pour memoiser les fonctions et les passer par reference
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-042 : Texte en dur sans i18n
- **Type** : mobile
- **Projet** : axenr-mobile
- **Erreur** : Ecrire `<Text>Validate</Text>` avec du texte en dur
- **Correction** : Utiliser `const I18n = useTranslator(); <Text>{I18n.t('Hr_Validate')}</Text>` avec le format `{Module}_{Action}`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS MIGRATION

### LESSON-043 : Script SQL non idempotent
- **Type** : migration
- **Projet** : axenr-app
- **Erreur** : Ecrire un script SQL qui echoue s'il est execute 2 fois (ex: `ALTER TABLE ADD COLUMN` sans `IF NOT EXISTS`)
- **Correction** : Toujours ecrire des scripts idempotents : `ADD COLUMN IF NOT EXISTS`, `ON CONFLICT DO NOTHING`, `WHERE NOT EXISTS`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-044 : Champ Studio supprime au lieu de transforme
- **Type** : migration
- **Projet** : axenr-app
- **Erreur** : Supprimer un champ Studio (`DELETE FROM meta_json_field`) au lieu de le transformer
- **Correction** : RENOMMER le champ avec UPDATE, garder `model_field='attrs'`, renommer la cle dans le JSON attrs, mettre a jour meta_view_custom
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS CODE SENIOR

### LESSON-045 : Switch verbeux remplacable par expression
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Ecrire un switch de 20 lignes pour convertir un enum en string quand une expression directe suffit
- **Correction** : Utiliser `dayOfWeek.name().toLowerCase(Locale.ROOT)` au lieu d'un switch. Exploiter les APIs Java natives
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-046 : if/else imbrique au lieu de stream
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Boucle for + if/else imbrique pour chercher dans une liste et extraire une valeur
- **Correction** : Utiliser `list.stream().filter(...).findFirst().map(...).orElse(default)` avec Optional
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-047 : Locale.ROOT manquant sur toLowerCase/toUpperCase
- **Type** : java
- **Projet** : axenr-app
- **Erreur** : Appeler `str.toLowerCase()` sans `Locale.ROOT`, causant des bugs potentiels en locale turque
- **Correction** : Toujours utiliser `str.toLowerCase(Locale.ROOT)` ou `str.toUpperCase(Locale.ROOT)`
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ERREURS GIT

### LESSON-048 : Branche creee depuis mauvaise base
- **Type** : build
- **Projet** : both
- **Erreur** : Creer une branche sans verifier qu'on est sur la bonne branche de base (ex: creer depuis une branche de ticket au lieu de dev)
- **Correction** : Toujours `git checkout <base> && git pull origin <base>` AVANT de creer la nouvelle branche
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-049 : Submodule et parent sur branches differentes
- **Type** : build
- **Projet** : axenr-app
- **Erreur** : Le submodule `modules/axenr` et le repo parent `axenr-app` ne sont pas sur la meme branche
- **Correction** : Les 2 repos DOIVENT avoir la meme branche. Synchroniser le submodule PUIS le parent, dans cet ordre
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-050 : Action existante supprimee
- **Type** : view
- **Projet** : axenr-app
- **Erreur** : Supprimer une action existante pour la remplacer par une nouvelle
- **Correction** : GARDER l'ancienne action ET ajouter la nouvelle. D'autres boutons/menus peuvent referencer l'ancienne
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

---

## ANTI-PATTERNS ENR (coherence metier)

### LESSON-051 : Nommage PV-specifique (ENR-AP-01)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Nommer un champ/classe avec des termes PV-specifiques (`solar`, `panel`, `module`, `onduleur`, `string`) sans contexte generique. Ex: `PvInstallationService`, `numberOfModules`, `inverterCapacity`
- **Correction** : Utiliser des termes generiques (`EnrInstallationService`, `numberOfEquipments`, `mainEquipmentCapacity`) ou ajouter un qualifieur de type ENR
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-052 : Bouton/action sans garde de lifecycle (ENR-AP-02)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Bouton ou action visible a toutes les etapes du cycle commercial sans condition `hideIf`/`readonlyIf` basee sur `statusSelect`. Ex: bouton "Generer facture" visible en PROSPECTION
- **Correction** : Ajouter `hideIf="statusSelect &lt; N"` ou `readonlyIf="statusSelect != N"` selon l'etape appropriee du cycle ENR (PROSPECTION=1, QUALIFICATION=2, DEVIS=3, PASSATION_BE=4, ADMINISTRATIF=5, PLANIFICATION=6, APPROVISIONNEMENT=7, CHANTIER=8, MISE_EN_SERVICE=9, FACTURATION=10, DOE_SAV=11)
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-053 : Seuil metier hardcode PV-specifique (ENR-AP-03)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Hardcoder des seuils PV-specifiques comme magic numbers : `9` (kWc autoconsommation), `36` (kWc seuil moyen), `100` (kWc seuil grande puissance). Ex: `if (power > 9)`
- **Correction** : Utiliser l'entite `AxenrConfig` avec une cle par type ENR. Ex: `axenrConfig.getThreshold(enrType)` au lieu du magic number
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-054 : Acces donnees d'une etape future (ENR-AP-04)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Acceder a un champ qui n'existe pas encore a l'etape courante du cycle. Ex: lire `installationDate` en PROSPECTION (disponible seulement apres PLANIFICATION), lire `consuelRef` en DEVIS (disponible apres ADMINISTRATIF)
- **Correction** : Garder chaque acces par une verification de l'etape (`statusSelect >= N`) et ajouter du null-safety sur les champs dependants de l'etape
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-055 : Service monolithique ENR (ENR-AP-05)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Un seul service qui gere tous les types ENR avec des if/else massifs. Ex: `if (type == PV) { ... } else if (type == PAC) { ... } else if (type == IRVE) { ... }`
- **Correction** : Utiliser le pattern Strategy avec une interface generique et une implementation par type ENR. Ou utiliser le polymorphisme avec une factory
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-056 : Selection non extensible aux nouveaux types ENR (ENR-AP-06)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Selection hardcodee qui ne couvre que certains types ENR ou qui ne permet pas d'en ajouter. Ex: selection avec uniquement "Rooftop PV" et "Ground mount PV"
- **Correction** : Utiliser une table de reference configurable au lieu d'une selection hardcodee, ou inclure des options pour TOUS les types ENR (PV, PAC, IRVE, eolien, geothermie, biomasse, solaire thermique)
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-057 : Calcul prime/subvention manquant (ENR-AP-07)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Code de facturation ou de devis qui ne prend pas en compte les subventions energetiques (MaPrimeRenov, CEE, prime autoconsommation)
- **Correction** : Ajouter un hook de calcul de prime/subvention dans le workflow de devis et facturation. Les primes varient par type ENR
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-058 : Unite PV-specifique (ENR-AP-08)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Utiliser `kWc` (kilowatt-crete) comme unite universelle alors que c'est specifique au PV. Les PAC utilisent `COP`, l'IRVE utilise `kW`, le thermique utilise `kWth`
- **Correction** : Utiliser une unite generique avec conversion par type ENR, ou stocker l'unite dans une table de reference liee au type ENR
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-059 : Contraintes site ignorees par type ENR (ENR-AP-09)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Pas de verification des contraintes specifiques au site pour chaque type ENR. Ex: PV necessite orientation/inclinaison toiture, PAC necessite distance voisins, IRVE necessite puissance electrique disponible
- **Correction** : Ajouter une validation de site parametree par type ENR dans l'etape QUALIFICATION
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false

### LESSON-060 : Planning sans consideration saisonniere (ENR-AP-10)
- **Type** : enr
- **Projet** : axenr-app
- **Erreur** : Planification de chantier sans prendre en compte les contraintes meteo/saison. Ex: installation PV en toiture en plein hiver, PAC geothermie avec sol gele
- **Correction** : Ajouter un hook de planification meteo-aware dans l'etape PLANIFICATION, avec des contraintes configurables par type ENR et region
- **Occurrences** : 1
- **Tickets** : initial-seed
- **Promu** : false
