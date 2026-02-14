# GitLab CI/CD Pipeline Optimization Guide

## Overview

This guide provides best practices for optimizing GitLab CI/CD pipelines to reduce execution time, resource usage, and costs while maintaining quality and reliability.

## 1. Caching Strategies

### Gradle Caching

**Optimal Configuration**:
```yaml
cache:
  key:
    files:
      - gradle.lockfile  # Lock file ensures cache invalidation on dependency changes
  paths:
    - .gradle/wrapper
    - .gradle/caches
  policy: pull-push      # Build jobs: upload and download
```

**Read-Only Cache** (for test/quality jobs):
```yaml
cache:
  key:
    files:
      - gradle.lockfile
  paths:
    - .gradle/caches
  policy: pull           # Only download, 30-50% faster
```

**Expected Savings**: 2-5 minutes per pipeline (40-60% reduction in dependency download time)

### Maven Caching

```yaml
cache:
  key:
    files:
      - pom.xml
  paths:
    - .m2/repository
variables:
  MAVEN_OPTS: "-Dmaven.repo.local=$CI_PROJECT_DIR/.m2/repository"
```

**Expected Savings**: 1-3 minutes per pipeline

### Node.js Caching

```yaml
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/
```

**Expected Savings**: 30-90 seconds per pipeline

## 2. Job Parallelization

### Strategy 1: Parallel Stages

Run independent jobs in parallel:

```yaml
test:unit:
  stage: test
  script: ./gradlew test

test:integration:
  stage: test
  script: ./gradlew integrationTest

# Both run simultaneously
```

**Expected Savings**: 30-50% reduction in total pipeline time

### Strategy 2: Matrix Builds

Test across multiple configurations:

```yaml
test:
  stage: test
  parallel:
    matrix:
      - JDK_VERSION: [11, 17, 21]
  image: gradle:8.5-jdk${JDK_VERSION}-alpine
  script: ./gradlew test
```

**Use Case**: Multi-version compatibility testing

### Strategy 3: Build Splitting

```yaml
build:frontend:
  stage: build
  script: npm run build

build:backend:
  stage: build
  script: ./gradlew build -x test

# Run in parallel, not sequentially
```

**Expected Savings**: 40-60% reduction in build stage time

## 3. Docker Image Optimization

### Use Specific Versions

**Bad**:
```yaml
image: gradle:latest      # Unpredictable, slower pulls
```

**Good**:
```yaml
image: gradle:8.5-jdk17-alpine  # Specific, cacheable, smaller
```

### Use Alpine Variants

| Image | Size | Pull Time |
|-------|------|-----------|
| `gradle:8.5-jdk17` | 850 MB | 60-90s |
| `gradle:8.5-jdk17-alpine` | 380 MB | 20-30s |

**Expected Savings**: 30-60 seconds per job

### Layer Caching

Docker images are cached by GitLab runners. Using consistent image versions ensures cache hits.

## 4. Artifact Management

### Minimize Artifact Size

**Bad**:
```yaml
artifacts:
  paths:
    - build/        # Entire build directory (100+ MB)
  expire_in: 1 week
```

**Good**:
```yaml
artifacts:
  paths:
    - build/libs/*.jar     # Only necessary files (5-10 MB)
  expire_in: 1 day         # Shorter expiration
```

### Use Reports Instead of Artifacts

**Bad**:
```yaml
artifacts:
  paths:
    - build/test-results/  # Upload all test files
```

**Good**:
```yaml
artifacts:
  reports:
    junit: build/test-results/test/TEST-*.xml  # Parsed by GitLab
```

**Benefits**:
- Faster upload (only XML, not HTML reports)
- Better UI integration
- Automatic failure detection

## 5. Dependency Optimization

### Use Dependency Locking

**Gradle**:
```bash
./gradlew dependencies --write-locks
```

Creates `gradle.lockfile` for deterministic builds and better caching.

**Maven**:
```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-enforcer-plugin</artifactId>
  <executions>
    <execution>
      <id>enforce-dependency-convergence</id>
      <goals><goal>enforce</goal></goals>
      <configuration>
        <rules>
          <dependencyConvergence/>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

### Offline Mode (when cache is warm)

```yaml
build:
  script:
    - ./gradlew build --offline  # Skip network checks if cache is complete
```

**Expected Savings**: 10-20 seconds per build

## 6. Conditional Job Execution

### Run Jobs Only When Needed

```yaml
spotless:
  stage: quality
  script: ./gradlew spotlessCheck
  rules:
    - if: $CI_MERGE_REQUEST_IID              # Only on MRs
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH  # Or on main

sonarqube:
  stage: quality
  script: ./gradlew sonarqube
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH  # Only on main
    - if: $CI_PIPELINE_SOURCE == "schedule"         # Or scheduled scans
```

### Path-Based Execution

```yaml
test:frontend:
  script: npm test
  rules:
    - changes:
      - "frontend/**/*"    # Only run if frontend files changed

test:backend:
  script: ./gradlew test
  rules:
    - changes:
      - "src/**/*.java"    # Only run if Java files changed
      - "build.gradle"
```

**Expected Savings**: Skip unnecessary jobs, 20-40% reduction in job count

## 7. Build Tool Configuration

### Gradle Optimizations

Add to `gradle.properties`:
```properties
# Parallel execution
org.gradle.parallel=true
org.gradle.workers.max=4

# Build cache
org.gradle.caching=true

# Daemon (disable in CI)
org.gradle.daemon=false

# Configure memory
org.gradle.jvmargs=-Xmx2048m -XX:MaxMetaspaceSize=512m
```

### Maven Optimizations

Add to `pom.xml`:
```xml
<properties>
  <maven.compiler.fork>true</maven.compiler.fork>
  <maven.compiler.maxmem>2048m</maven.compiler.maxmem>
</properties>
```

Use parallel builds:
```bash
mvn clean package -T 4  # 4 threads
```

## 8. Test Optimization

### Selective Test Execution

```yaml
test:changed:
  script:
    - ./gradlew test --tests '*ChangedFile*Test'
  rules:
    - if: $CI_MERGE_REQUEST_IID
```

### Coverage Threshold Caching

```yaml
test:
  script:
    - ./gradlew test jacocoTestReport
  coverage: '/Total.*?([0-9]{1,3})%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: build/reports/jacoco/test/jacocoTestReport.xml
```

GitLab caches coverage results for MR comparison.

## 9. Pipeline Structure

### Optimal Stage Order

```yaml
stages:
  - init        # Fast validations (30-60s)
  - build       # Compilation (2-4 min)
  - test        # Testing (3-5 min)
  - quality     # Analysis (1-3 min)
  - plan        # Publishing (optional)
  - deploy      # Deployment (optional)
```

**Fail Fast**: Place blocking validations (commitlint, MR title) in init stage to fail quickly before expensive build/test stages.

### Job Dependencies

```yaml
test:
  stage: test
  needs: [build]  # Don't wait for all build stage jobs
  script: ./gradlew test
```

**Expected Savings**: Run dependent jobs immediately without waiting for entire stage completion.

## 10. Monitoring and Profiling

### Pipeline Duration Tracking

Add metrics to jobs:
```yaml
build:
  script:
    - date +%s > start_time
    - ./gradlew build
    - echo "Build duration: $(($(date +%s) - $(cat start_time)))s"
```

### GitLab CI/CD Analytics

Use GitLab's built-in analytics:
- **CI/CD > Pipelines > Duration chart**: Identify trends
- **CI/CD > Jobs > Duration**: Find slowest jobs
- **Settings > CI/CD > Pipeline badges**: Monitor success rate

## Performance Benchmarks

### Typical Pipeline Durations (Gradle Project)

| Configuration | Init | Build | Test | Quality | Total |
|---------------|------|-------|------|---------|-------|
| **Unoptimized** | 2m | 5m | 6m | 3m | 16m |
| **Basic Cache** | 2m | 3m | 4m | 2m | 11m |
| **Full Optimization** | 1m | 2m | 3m | 1.5m | 7.5m |

**Optimization Impact**: 53% reduction in total pipeline time

### Cost Savings

Assuming GitLab SaaS pricing (~$0.50/compute minute):
- Unoptimized: $8.00 per pipeline
- Optimized: $3.75 per pipeline
- **Savings**: $4.25 per pipeline (53%)

For 100 pipelines/month: **$425/month savings**

## Quick Wins Checklist

High-impact, low-effort optimizations:

- [ ] Enable Gradle/Maven dependency caching with lockfiles
- [ ] Use alpine Docker images
- [ ] Set cache policy to 'pull' for read-only jobs
- [ ] Add artifact expiration times (1 day for temporary, 1 week for releases)
- [ ] Use `needs:` to avoid waiting for entire stages
- [ ] Run expensive jobs (sonarqube) only on main branch
- [ ] Enable Gradle build cache (org.gradle.caching=true)
- [ ] Use specific Docker image versions (not 'latest')
- [ ] Minimize artifact paths (only .jar files, not entire build/)
- [ ] Use GitLab reports (junit, coverage_report) instead of raw artifacts

**Expected Total Impact**: 40-60% reduction in pipeline duration

## Advanced Techniques

### Remote Build Cache (Gradle Enterprise)

For large teams, use shared build cache:
```properties
# gradle.properties
org.gradle.caching=true
org.gradle.cache.remote.url=https://cache.example.com
org.gradle.cache.remote.push=true
```

**Expected Savings**: 60-80% cache hit rate, 5-10 minute reduction

### Distributed Testing

Split tests across multiple jobs:
```yaml
test:
  parallel: 4
  script:
    - ./gradlew test --parallel
```

**Expected Savings**: 50-75% reduction in test time for large test suites

### Incremental Builds

Configure Gradle for incremental compilation:
```groovy
tasks.withType(JavaCompile) {
    options.incremental = true
}
```

**Expected Savings**: 30-50% faster builds for code changes
