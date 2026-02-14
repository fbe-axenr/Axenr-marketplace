# /develop Troubleshooting Guide

Common issues and solutions for the `/develop` command.

---

## Issue: Phase 1 skipped unexpectedly

**Cause**: Architecture file detected automatically

**Solution**: Check for existing `architecture-plan.md` files in:
- `{output_directory}/architecture-plan.md`
- `docs/architecture-plan.md`

Use `--architecture-file=none` to force Mode CREATE.

---

## Issue: Validation errors in generated code

**Cause**: Skills detected issues during generation

**Solution**:
1. Check validation output in the agent response
2. Agent should auto-fix most issues
3. Complex issues may need manual intervention
4. Use ITERATE response to request specific fixes

---

## Issue: Resume not working

**Cause**: State file corrupted or missing

**Solution**:
1. Check `.axelor-develop-state.json` exists
2. Verify JSON is valid
3. If corrupted, delete and restart from Phase 1:
   ```bash
   rm .axelor-develop-state.json
   /develop docs/spec.md docs/dev
   ```

---

## Issue: Checkpoint commits missing

**Cause**: Git errors during commit (only with `--auto-commit`)

**Solution**:
1. Check git status: `git status`
2. Resolve any conflicts
3. Re-run phase to create checkpoint
4. Verify `.gitignore` doesn't exclude necessary files

---

## Issue: Webapp not detected

**Cause**: Running from wrong directory or invalid project structure

**Solution**:
1. Run from webapp root directory (contains `build.gradle`)
2. Or use explicit path: `--webapp=/path/to/webapp`
3. Verify webapp has valid structure:
   - `build.gradle` with `com.axelor.app` plugin
   - `modules/` directory
   - `gradle.properties`

---

## Issue: Axelor repositories not found

**Cause**: AOP/AOS paths not in default location

**Solution**:
1. Set environment variable: `AXELOR_REPO=/path/to/axelor`
2. Or provide path when prompted
3. Directory must contain `aop/`, `aos/`, `addons/` subdirectories

---

## Issue: Build fails after code generation

**Cause**: Generated code has compilation errors

**Solution**:
1. Agent should auto-fix and rebuild
2. If persistent, use ITERATE to request fixes
3. Check Java version compatibility (AOP 7.x → Java 11, AOP 8.x → Java 21)
4. Verify all dependencies are declared in `build.gradle`

---

## Issue: Tests fail in Phase 5

**Cause**: Test configuration or implementation issues

**Solution**:
1. Check test database configuration in `src/test/resources/`
2. Verify JaCoCo is properly configured
3. Use ITERATE to fix specific test failures
4. Or use `--skip-tests` to proceed without tests

---

## Getting Help

If issues persist:
1. Check agent output for detailed error messages
2. Review generated files for obvious issues
3. Use REJECT to abort and start fresh
4. Consult [Axelor documentation](https://docs.axelor.com/)
