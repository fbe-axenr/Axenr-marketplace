# Gradle Dependency Management

This guide provides comprehensive information about Gradle dependency management in Axelor projects.

## Gradle Dependency Management

### Overview

**ALL Axelor projects MUST use Gradle for dependency management.**

### Dependency Declaration

**Rule**: Declare dependencies explicitly and avoid version conflicts.

**Pattern**:
```groovy
dependencies {
    // Explicit versions for third-party libraries
    implementation 'com.google.guava:guava:31.1-jre'
    implementation 'org.apache.commons:commons-lang3:3.12.0'
    implementation 'org.apache.commons:commons-collections4:4.4'

    // Test dependencies
    testImplementation 'junit:junit:4.13.2'
    testImplementation 'org.mockito:mockito-core:4.11.0'

    // Avoid transitive dependencies when possible
    implementation('org.some.library:library:1.0.0') {
        exclude group: 'commons-logging', module: 'commons-logging'
    }
}
```

### Detecting Obsolete Dependencies

**Rule**: Regularly check for dependency issues and outdated dependencies.

**Commands**:
```bash
# Generate dependency report
./gradlew dependencies > dependencies.txt

# Check for outdated dependencies
./gradlew dependencyUpdates
```

### Java Version Compatibility

**Rule**: Verify dependencies are compatible with project Java version.

**build.gradle**:
```groovy
// For AOP 7.x projects (Java 11)
java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

// For AOP 8.x projects (Java 21)
java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
}

```

### Dependency Version Management

**Rule**: Use version variables and BOM (Bill of Materials) when available.

**gradle.properties**:
```properties
aopVersion=8.0.0
guavaVersion=31.1-jre
commonsLang3Version=3.12.0
```

**build.gradle**:
```groovy
dependencies {
    // Use version variables
    implementation "com.google.guava:guava:${guavaVersion}"
    implementation "org.apache.commons:commons-lang3:${commonsLang3Version}"
}
```

### Transitive Dependency Management

**Rule**: Exclude unnecessary transitive dependencies to reduce classpath size.

**Pattern**:
```groovy
dependencies {
    implementation('org.some.library:library:1.0.0') {
        // Exclude commons-logging (we use SLF4J)
        exclude group: 'commons-logging', module: 'commons-logging'

        // Exclude specific transitive dependency
        exclude group: 'org.slf4j', module: 'slf4j-log4j12'
    }

    // Use SLF4J with Logback instead
    implementation 'ch.qos.logback:logback-classic:1.4.11'
}
```

### Security: Vulnerability Scanning

**Rule**: Scan dependencies for known vulnerabilities.

**build.gradle**:
```groovy
plugins {
    id 'org.owasp.dependencycheck' version '8.4.0'
}

dependencyCheck {
    format = 'ALL'
    suppressionFile = file('dependency-check-suppressions.xml')
}

// Run on every build
tasks.build.dependsOn dependencyCheckAnalyze
```

### Java-Aware Build Commands (CRITICAL)

**RULE:** All Gradle commands MUST use the correct Java version based on AOP version.

**Java Version Mapping:**

| AOP Version | Java Version |
|-------------|--------------|
| AOP 7.x | Java 11 |
| AOP 8.x | Java 21 |

**Java Home Detection Function (Ubuntu):**

```bash
# Function to detect Java home on Ubuntu
get_java_home() {
    local version=$1
    local java_home=""

    # Method 1: Try update-java-alternatives (most reliable)
    java_home=$(update-java-alternatives --list 2>/dev/null | grep "java-${version}" | awk '{print $3}' | head -1)

    # Method 2: Fallback to /usr/lib/jvm/ directory listing
    if [[ -z "$java_home" || ! -d "$java_home" ]]; then
        java_home=$(ls -d /usr/lib/jvm/java-${version}-* 2>/dev/null | head -1)
    fi

    echo "$java_home"
}
```

**Complete Build Script Pattern:**

```bash
# 1. Detect AOP version from gradle.properties
AOP_VERSION=$(grep "aopVersion" gradle.properties 2>/dev/null | cut -d'=' -f2 | tr -d ' ')

# 2. Determine required Java version
if [[ "$AOP_VERSION" == 8.* ]]; then
    REQUIRED_JAVA="21"
else
    REQUIRED_JAVA="11"
fi

# 3. Detect Java home (try update-java-alternatives first, fallback to /usr/lib/jvm/)
JAVA_HOME_PATH=$(update-java-alternatives --list 2>/dev/null | grep "java-${REQUIRED_JAVA}" | awk '{print $3}' | head -1)

if [[ -z "$JAVA_HOME_PATH" || ! -d "$JAVA_HOME_PATH" ]]; then
    JAVA_HOME_PATH=$(ls -d /usr/lib/jvm/java-${REQUIRED_JAVA}-* 2>/dev/null | head -1)
fi

# 4. Verify Java home was found
if [[ -z "$JAVA_HOME_PATH" || ! -d "$JAVA_HOME_PATH" ]]; then
    echo "ERROR: Java ${REQUIRED_JAVA} not found. Please install openjdk-${REQUIRED_JAVA}-jdk"
    exit 1
fi

echo "Using Java ${REQUIRED_JAVA} from: ${JAVA_HOME_PATH}"

# 5. Execute Gradle with correct Java
./gradlew clean build -Dorg.gradle.java.home="${JAVA_HOME_PATH}"
```

**One-liner for agents (copy-paste ready):**

```bash
# For generateCode
AOP_VER=$(grep "aopVersion" gradle.properties | cut -d'=' -f2 | tr -d ' '); JAVA_VER=$([[ "$AOP_VER" == 8.* ]] && echo "21" || echo "11"); JAVA_HOME_PATH=$(update-java-alternatives --list 2>/dev/null | grep "java-${JAVA_VER}" | awk '{print $3}' | head -1); [[ -z "$JAVA_HOME_PATH" ]] && JAVA_HOME_PATH=$(ls -d /usr/lib/jvm/java-${JAVA_VER}-* 2>/dev/null | head -1); ./gradlew generateCode -Dorg.gradle.java.home="${JAVA_HOME_PATH}"

# For clean build
AOP_VER=$(grep "aopVersion" gradle.properties | cut -d'=' -f2 | tr -d ' '); JAVA_VER=$([[ "$AOP_VER" == 8.* ]] && echo "21" || echo "11"); JAVA_HOME_PATH=$(update-java-alternatives --list 2>/dev/null | grep "java-${JAVA_VER}" | awk '{print $3}' | head -1); [[ -z "$JAVA_HOME_PATH" ]] && JAVA_HOME_PATH=$(ls -d /usr/lib/jvm/java-${JAVA_VER}-* 2>/dev/null | head -1); ./gradlew clean build -Dorg.gradle.java.home="${JAVA_HOME_PATH}"

# For tests
AOP_VER=$(grep "aopVersion" gradle.properties | cut -d'=' -f2 | tr -d ' '); JAVA_VER=$([[ "$AOP_VER" == 8.* ]] && echo "21" || echo "11"); JAVA_HOME_PATH=$(update-java-alternatives --list 2>/dev/null | grep "java-${JAVA_VER}" | awk '{print $3}' | head -1); [[ -z "$JAVA_HOME_PATH" ]] && JAVA_HOME_PATH=$(ls -d /usr/lib/jvm/java-${JAVA_VER}-* 2>/dev/null | head -1); ./gradlew test -Dorg.gradle.java.home="${JAVA_HOME_PATH}"
```

**IMPORTANT:** Always detect the AOP version from `gradle.properties` BEFORE running any Gradle command.

---

### Agent Integration with Gradle

**When generating code, the agent MUST**:

1. **Detect Java version FIRST** (CRITICAL):
   ```bash
   # Read aopVersion and determine Java version
   AOP_VER=$(grep "aopVersion" gradle.properties | cut -d'=' -f2 | tr -d ' ')
   # AOP 7.x → Java 11, AOP 8.x → Java 21
   JAVA_VER=$([[ "$AOP_VER" == 8.* ]] && echo "21" || echo "11")

   # Detect Java home (Ubuntu)
   JAVA_HOME_PATH=$(update-java-alternatives --list 2>/dev/null | grep "java-${JAVA_VER}" | awk '{print $3}' | head -1)
   [[ -z "$JAVA_HOME_PATH" ]] && JAVA_HOME_PATH=$(ls -d /usr/lib/jvm/java-${JAVA_VER}-* 2>/dev/null | head -1)
   ```

2. **Check build.gradle** to determine:
   - AOP version (7.x → Java 11, 8.x → Java 21)
   - Existing dependencies (avoid duplicates)
   - Project structure (module vs webapp)

3. **Verify dependencies** are available before using classes:
   ```java
   // Only use Guava if present in build.gradle
   import com.google.common.collect.ImmutableList;
   ```

4. **Suggest dependencies** when needed:
   ```
   NOTE: This code requires the following dependency in build.gradle:
   implementation 'org.apache.commons:commons-lang3:3.12.0'
   ```

5. **Run Gradle commands with correct Java** (CRITICAL):
   ```bash
   # ALWAYS use the one-liner pattern to detect and run with correct Java

   # generateCode
   AOP_VER=$(grep "aopVersion" gradle.properties | cut -d'=' -f2 | tr -d ' '); JAVA_VER=$([[ "$AOP_VER" == 8.* ]] && echo "21" || echo "11"); JAVA_HOME_PATH=$(update-java-alternatives --list 2>/dev/null | grep "java-${JAVA_VER}" | awk '{print $3}' | head -1); [[ -z "$JAVA_HOME_PATH" ]] && JAVA_HOME_PATH=$(ls -d /usr/lib/jvm/java-${JAVA_VER}-* 2>/dev/null | head -1); ./gradlew generateCode -Dorg.gradle.java.home="${JAVA_HOME_PATH}"

   # clean build
   AOP_VER=$(grep "aopVersion" gradle.properties | cut -d'=' -f2 | tr -d ' '); JAVA_VER=$([[ "$AOP_VER" == 8.* ]] && echo "21" || echo "11"); JAVA_HOME_PATH=$(update-java-alternatives --list 2>/dev/null | grep "java-${JAVA_VER}" | awk '{print $3}' | head -1); [[ -z "$JAVA_HOME_PATH" ]] && JAVA_HOME_PATH=$(ls -d /usr/lib/jvm/java-${JAVA_VER}-* 2>/dev/null | head -1); ./gradlew clean build -Dorg.gradle.java.home="${JAVA_HOME_PATH}"

   # test
   AOP_VER=$(grep "aopVersion" gradle.properties | cut -d'=' -f2 | tr -d ' '); JAVA_VER=$([[ "$AOP_VER" == 8.* ]] && echo "21" || echo "11"); JAVA_HOME_PATH=$(update-java-alternatives --list 2>/dev/null | grep "java-${JAVA_VER}" | awk '{print $3}' | head -1); [[ -z "$JAVA_HOME_PATH" ]] && JAVA_HOME_PATH=$(ls -d /usr/lib/jvm/java-${JAVA_VER}-* 2>/dev/null | head -1); ./gradlew test -Dorg.gradle.java.home="${JAVA_HOME_PATH}"
   ```

### Summary: Gradle Enforcement Checklist

When generating Java code, VERIFY:

- [ ] Check build.gradle for AOP version to determine Java version
- [ ] Check build.gradle for existing dependencies
- [ ] Only use classes from declared dependencies
- [ ] Suggest new dependencies when needed (with version)
- [ ] Run ./gradlew generateCode after domain changes
- [ ] Run ./gradlew compileJava after code generation
- [ ] NO EMOJIS anywhere
- [ ] ALL code and comments in ENGLISH
