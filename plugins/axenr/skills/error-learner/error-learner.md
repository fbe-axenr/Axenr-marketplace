# Error Learner

> Analyse une erreur, cherche si elle est connue, sinon cree une lecon dans LESSONS-LEARNED.md

## ROLE

Recevoir une erreur (message, fichier, contexte), chercher si un pattern similaire existe deja dans LESSONS-LEARNED.md, et soit incrementer le compteur d'une lecon existante, soit creer une nouvelle lecon.

## INPUTS

| Input | Format |
|-------|--------|
| error_message | Le message d'erreur complet (stacktrace, log, ou issue de validation) |
| error_file | Le fichier ou l'erreur a ete detectee |
| error_source | L'agent ou outil qui a detecte l'erreur (code-reviewer, build, xml-validator, etc.) |
| ticket_number | Le numero du ticket en cours |
| project | axenr-app ou axenr-mobile |
| lessons_file_path | Chemin absolu vers LESSONS-LEARNED.md dans le marketplace |

## OUTPUTS

| Output | Format |
|--------|--------|
| lesson_id | LESSON-XXX (nouveau ou existant) |
| is_new | true si nouvelle lecon, false si existante |
| occurrence_count | Nombre total d'occurrences |
| fix_suggestion | La correction suggeree (issue d'une lecon existante ou a determiner) |

## LOGIQUE

```
1. Lire LESSONS-LEARNED.md
2. Extraire le PATTERN de l'erreur :
   - Retirer les noms de fichiers specifiques
   - Retirer les numeros de ligne
   - Garder le TYPE d'erreur (ex: "missing @Transactional", "ref without full package")
3. Chercher dans les lecons existantes si ce PATTERN correspond :
   - Comparaison par type d'erreur
   - Comparaison par symptome
   - Comparaison par source (meme agent/outil)
4. SI match trouve :
   - Incrementer le compteur d'occurrences
   - Ajouter le numero de ticket a la liste
   - Ajouter la date
   - Retourner la lecon existante avec son fix
5. SI pas de match :
   - Generer un nouveau LESSON-XXX (incrementer le compteur global)
   - Remplir tous les champs obligatoires
   - Determiner le fix a partir de l'erreur
   - Ecrire dans LESSONS-LEARNED.md
   - Retourner la nouvelle lecon
```

## FORMAT D'UNE LECON

```markdown
### LESSON-XXX : titre court et descriptif
- **Date** : YYYY-MM-DD
- **Projet** : axenr-app | axenr-mobile
- **Ticket** : #750, #760
- **Type** : domain | view | java | mobile | build | version
- **Source** : code-reviewer | code-analyzer | xml-validator | build | etc.
- **Erreur** : description exacte de ce qui a echoue
- **Symptome** : le message d'erreur ou le comportement observe
- **Cause** : pourquoi ca a echoue
- **Fix** : ce qui a ete fait pour corriger
- **Regle** : la regle generale a retenir
- **Occurrences** : 1
- **Promu** : false
```

## EXEMPLES

### Input : erreur de validation XML

```
error_message: "CRITICAL: missing form-view on relational field 'partner'"
error_file: "modules/axenr/src/main/resources/views/opportunity-views.xml"
error_source: "code-reviewer"
ticket_number: "#750"
project: "axenr-app"
```

### Output : nouvelle lecon

```
lesson_id: "LESSON-013"
is_new: true
occurrence_count: 1
fix_suggestion: "Add form-view='partner-form' grid-view='partner-grid' to the field"
```

### Input : erreur deja connue

```
error_message: "CRITICAL: @Transactional missing on method with save()"
error_source: "code-reviewer"
ticket_number: "#760"
```

### Output : lecon existante incrementee

```
lesson_id: "LESSON-010"
is_new: false
occurrence_count: 3
fix_suggestion: "Add @Transactional(rollbackOn = {Exception.class}) to the method"
```
