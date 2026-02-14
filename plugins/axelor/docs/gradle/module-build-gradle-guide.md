# Axelor Module build.gradle Guide

## Overview

This guide provides templates and rules for creating `build.gradle` files for Axelor modules.

**CRITICAL:** Axelor modules MUST use the `com.axelor.app` plugin.

---

## Template for Module build.gradle

### Basic Template

```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "[Module Display Name]"
}

dependencies {
    implementation project(':axelor-base')
    // Add other module dependencies as needed
}
```

### Real Example: Contract Module

```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Contract Pro"
}

dependencies {
    implementation project(':axelor-base')
}
```

### Real Example: Sales Module with External Dependencies

```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Sales Management"
}

dependencies {
    implementation project(':axelor-base')
    implementation project(':axelor-crm')

    // External dependencies (if needed)
    implementation 'org.apache.commons:commons-lang3:3.12.0'
    implementation 'com.google.guava:guava:31.1-jre'
}
```

---

## Critical Rules

### 1. Plugin Selection (ZERO TOLERANCE)

**ALWAYS:**
```gradle
plugins {
    id 'com.axelor.app'
}
```

**NEVER:**
```gradle
plugins {
    id 'java-library'  // ❌ WRONG - This is for standard Java libraries
}
```

```gradle
plugins {
    id 'java'  // ❌ WRONG - This is for standard Java projects
}
```

**Why com.axelor.app?**
- Handles Axelor-specific build tasks (generateCode, etc.)
- Manages domain XML to Java entity generation
- Configures proper classpath for Axelor runtime
- Handles module packaging and dependencies correctly

### 2. Module Title

**ALWAYS** specify a human-readable title:

```gradle
axelor {
    title = "Axelor Contract Management"  // ✅ Clear, descriptive
}
```

**NEVER** use technical names:

```gradle
axelor {
    title = "axelor-contract"  // ❌ WRONG - Use display name, not module name
}
```

### 3. Dependencies - Conditional Configuration (CRITICAL FOR CLIENT PROJECTS)

**CRITICAL:** **NEVER use only local module references (`project(":modules:...")`)** in production modules. Client projects typically use Nexus/Maven repositories, not local modules.

**WRONG - Local modules only (work only if the modules are in the webapp modules directory):**
```gradle
dependencies {
    implementation project(':modules:axelor-sale')
}
```

**CORRECT**

```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Product Pro"
}


dependencies {
  implementation "com.axelor:axelor-sale:${aosVersion}"
}
```

**Core dependencies (if needed):**

```gradle
dependencies {
 
  implementation "com.axelor:axelor-base:${aosVersion}"
    
}
```

**Optional Axelor module dependencies:**

```gradle
dependencies {

        implementation "com.axelor:axelor-base:${aosVersion}"
        implementation "com.axelor:axelor-crm:${aosVersion}"
        implementation "com.axelor:axelor-sale:${aosVersion}"
        implementation "com.axelor:axelor-account:${aosVersion}"
}
```

**External dependencies:**

```gradle
dependencies {
    // Axelor dependencies (conditional)
    implementation "com.axelor:axelor-base:${aosVersion}"
    

    // Use version variables from gradle.properties when possible
    implementation "org.apache.commons:commons-lang3:${commonsLang3Version}"
}
```

### 4. Java Version (CRITICAL)

**NEVER** specify Java version in module build.gradle:

```gradle
// ❌ WRONG - DO NOT ADD THIS IN MODULE BUILD.GRADLE
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(11)
    }
}
```

**WHY?** Java version is configured at the **parent project level** and inherited by all modules.

**Where Java version IS configured:**
- Root `build.gradle`
- Root `gradle.properties`

---

## Common Mistakes and Fixes

### Mistake 1: Wrong Plugin

**WRONG:**
```gradle
plugins {
    id 'java-library'
}

axelor {
    title = "Axelor Contract Pro"
}
```

**CORRECT:**
```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Contract Pro"
}
```

### Mistake 2: Java Version in Module

**WRONG:**
```gradle
plugins {
    id 'com.axelor.app'
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(11)  // ❌ REMOVE THIS
    }
}

axelor {
    title = "Axelor Contract Pro"
}
```

**CORRECT:**
```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Contract Pro"
}

dependencies {
    implementation project(':axelor-base')
}
```

### Mistake 3: Missing Core Dependencies

**WRONG:**
```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Contract Pro"
}

dependencies {
    // ❌ Missing needed axelor-base 
    implementation 'com.google.guava:guava:31.1-jre'
}
```

**CORRECT:**
```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Contract Pro"
}

dependencies {
    implementation project(':axelor-base') (added if needed)
    implementation 'com.google.guava:guava:31.1-jre'
}
```

---

## Module Structure and build.gradle Location

### Directory Structure

```
modules/
└── axelor-contract/
    ├── build.gradle                    ← Module build.gradle (THIS FILE)
    ├── src/
    │   ├── main/
    │   │   ├── java/
    │   │   │   └── com/axelor/apps/contract/
    │   │   └── resources/
    │   │       ├── domains/
    │   │       ├── views/
    │   │    
    │   └── test/
    └── README.md
```

**Location:** `modules/[module-name]/build.gradle`

---

## Validation Checklist

Before finalizing a module build.gradle, verify:

- [ ] Plugin is `com.axelor.app`
- [ ] Module title is specified in `axelor { title = "..." }`
- [ ] Core dependencies included if needed(`axelor-base`)
- [ ] Other module dependencies match architecture requirements
- [ ] NO Java version specification in module build.gradle
- [ ] External dependencies use version variables when available
- [ ] File is located at `modules/[module-name]/build.gradle`

---

## Integration with Architecture Plan

When generating from architecture plan:

1. **Extract module name** from architecture specification
2. **Extract module title** from architecture specification
3. **Extract dependencies** from architecture specification (look for "depends on", "integrates with")
4. **Use template** from this guide
5. **Replace placeholders** with actual values

**Example from Architecture Plan:**

```markdown
## Module Configuration

**Module Name:** axelor-contract
**Module Title:** Axelor Contract Management
**Dependencies:**
- axelor-base
- axelor-crm (for customer management)
```

**Generated build.gradle:**

```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Contract Management"
}

dependencies {
    implementation project(':axelor-base')
    implementation project(':axelor-crm')
}
```

---

## Best Practices

### 1. Keep It Simple

Module build.gradle should be minimal. Most configuration happens at the parent level.

**Good:**
```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "Axelor Contract Pro"
}

dependencies {
    implementation project(':axelor-base')
}
```

### 2. Use Version Variables

For external dependencies, use version variables from `gradle.properties`:

**gradle.properties:**
```properties
guavaVersion=31.1-jre
commonsLang3Version=3.12.0
```

**build.gradle:**
```gradle
dependencies {
    implementation project(':axelor-base')
    implementation "com.google.guava:guava:${guavaVersion}"
    implementation "org.apache.commons:commons-lang3:${commonsLang3Version}"
}
```

### 3. Order Dependencies

Keep dependencies organized:

```gradle
dependencies {
    // 1. Axelor core modules (required)
    implementation project(':axelor-base')

    // 2. Other Axelor modules (alphabetical)
    implementation project(':axelor-crm')
    implementation project(':axelor-sale')

    // 3. External dependencies (alphabetical)
    implementation 'com.google.guava:guava:31.1-jre'
    implementation 'org.apache.commons:commons-lang3:3.12.0'
}
```

---

## Troubleshooting

### Error: "Could not find method axelor() for arguments"

**Cause:** Wrong plugin (using `java-library` instead of `com.axelor.app`)

**Fix:** Change plugin to `com.axelor.app`

### Error: "generateCode task not found"

**Cause:** Wrong plugin (using `java` or `java-library`)

**Fix:** Change plugin to `com.axelor.app`

### Error: "Java version mismatch"

**Cause:** Java version specified in module build.gradle

**Fix:** Remove Java version specification from module build.gradle

---

## Summary

**THE GOLDEN RULE:** Module build.gradle files MUST use `com.axelor.app` plugin.

**THE TEMPLATE:**

```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "[Module Display Name]"
}

dependencies {
    implementation project(':axelor-base')
}
```

That's it. Keep it simple, keep it correct.
