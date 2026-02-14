# Gradle Configuration Documentation

This directory contains documentation for Gradle configuration in Axelor projects.

## Files

### [module-build-gradle-guide.md](module-build-gradle-guide.md)

**Complete guide for module build.gradle files**

Topics covered:
- Templates for module build.gradle
- Plugin selection (`com.axelor.app` vs `java-library`)
- Dependency configuration
- Common mistakes and fixes
- Validation checklist
- Troubleshooting

**CRITICAL RULE:** Axelor modules MUST use `com.axelor.app` plugin, NOT `java-library`


## Quick Reference

### Module build.gradle Template

```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Module Display Name"
}

dependencies {
    implementation project(':axelor-base')
}
```


## Usage

These guides are referenced by:
- **architect agent** - For architecture planning (Phase 7: Module Configuration)
- **java-agent agent** - For generating module configuration files (Step 2.5)
- **Developers** - For manual module creation and troubleshooting

## Critical Rules Summary

1. **build.gradle plugin:** ALWAYS use `com.axelor.app` (NEVER `java-library` or `java`)
2. **Java version:** NEVER specify in module build.gradle (handled by parent)
3. **Module title:** MUST be descriptive and match architecture specification

## See Also

- **@docs/java/gradle-guide.md** - Parent project Gradle configuration
- **@docs/architecture/architecture-design-process.md** - Phase 7: Module Configuration
