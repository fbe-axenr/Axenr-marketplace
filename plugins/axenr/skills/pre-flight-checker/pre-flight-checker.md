# Pre-Flight Checker

> Charge le contexte complet avant toute generation de code : lecons, regles, versions, i18n, code existant

## ROLE

Collecter toutes les informations necessaires avant que le ticket-solver-agent ne commence a generer du code. Retourner un contexte structure que l'agent utilisera tout au long du workflow.

## INPUTS

| Input | Format |
|-------|--------|
| project | `axenr-app` ou `axenr-mobile` |
| project_path | Chemin absolu vers le projet |
| marketplace_path | Chemin absolu vers le marketplace |
| ticket_type | `domain`, `view`, `java`, `mobile`, `mix` |

## OUTPUTS

Un objet contexte structure contenant :

| Champ | Description |
|-------|-------------|
| lessons | Liste des lecons pertinentes extraites de LESSONS-LEARNED.md |
| project_rules | Contenu du CLAUDE.md du projet |
| dev_guide | Contenu de axelor-dev-guide.md (si axenr-app) |
| aop_version | Version AOP (ex: 7.4.7) |
| aos_version | Version AOS (ex: 8.5.11) |
| project_version | Version du projet (ex: 2.2.0-SNAPSHOT) |
| module_versions | Map des versions de chaque module enterprise et addon |
| xsd_version | Version XSD a utiliser (ex: 7.1) |
| existing_i18n_keys | Liste des cles i18n existantes |
| reusable_code | Liste des services/composants/methodes reutilisables |

## LOGIQUE

```
1. LECONS
   Lire <marketplace_path>/plugins/axenr/docs/lessons/LESSONS-LEARNED.md
   Filtrer les lecons par :
   - projet (axenr-app ou axenr-mobile)
   - type (domain, view, java, mobile, build, version)
   Retourner les lecons pertinentes au ticket_type

2. REGLES PROJET
   Lire <project_path>/CLAUDE.md (ou le chemin connu du CLAUDE.md)
   SI projet == axenr-app :
     Lire aussi axelor-dev-guide.md

3. VERSIONS (axenr-app uniquement)
   Lire <project_path>/gradle.properties :
     → Extraire aopVersion (ex: 7.4.7)
     → Extraire version (ex: 2.2.0-SNAPSHOT)
   Lire <project_path>/gradle/libs.versions.toml :
     → Extraire axelorOpenSuite (ex: 8.5.11)
     → Extraire CHAQUE version de module enterprise individuellement
     → Extraire les versions des addons
   Calculer xsd_version :
     → AOP 7.x → XSD 7.1
     → AOP 8.x → XSD 8.0 (a verifier)

4. I18N
   SI projet == axenr-app :
     Lire <project_path>/modules/axenr/src/main/resources/i18n/messages_fr.csv
     Lire <project_path>/modules/axenr/src/main/resources/i18n/custom_fr.csv
     Lire <project_path>/modules/axenr/src/main/resources/i18n/messages.csv
     Extraire toutes les cles (premiere colonne)
   SI projet == axenr-mobile :
     Lire <project_path>/src/axenr/i18n/ (tous les fichiers)
     Extraire toutes les cles

5. CODE REUTILISABLE
   SI ticket_type contient "java" :
     Lister les services dans <project_path>/modules/axenr/src/main/java/fr/axenr/service/
     Lister les controllers dans <project_path>/modules/axenr/src/main/java/fr/axenr/action/
   SI ticket_type contient "domain" :
     Lister les domains dans <project_path>/modules/axenr/src/main/resources/domains/
   SI ticket_type contient "view" :
     Lister les vues dans <project_path>/modules/axenr/src/main/resources/views/
   SI ticket_type contient "mobile" :
     Lister les composants dans <project_path>/src/axenr/components/
     Lister les slices dans <project_path>/src/axenr/features/

6. Retourner le contexte complet
```

## EXEMPLES

### Contexte pour un ticket domain+view sur axenr-app

```
{
  "lessons": [
    "LESSON-005: boolean sans title avec default='false'",
    "LESSON-013: form-view et grid-view obligatoires sur relationnels"
  ],
  "aop_version": "7.4.7",
  "aos_version": "8.5.11",
  "project_version": "2.2.0-SNAPSHOT",
  "xsd_version": "7.1",
  "module_versions": {
    "axelor-intervention": "8.5.11",
    "axelor-business-support": "8.5.5",
    "axelor-project-scheduler": "8.5.0"
  },
  "existing_i18n_keys": ["Estimated Power", "Number of modules", ...],
  "reusable_code": ["OpportunityService.java", "Opportunity.xml", ...]
}
```
