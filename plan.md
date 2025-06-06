# Plan to Remove Tesseract Dependency and Related Features

This document outlines the steps required to remove the external dependency on Tesseract OCR and all features that rely on it from the OCRmyPDF codebase, documentation, tests, and CI/CD configurations.

## 1. Goals and Scope

- Eliminate any runtime requirement for the `tesseract` binary.
- Remove all CLI options, API parameters, plugins, and code paths that invoke or configure Tesseract.
- Update or remove documentation, examples, and installation instructions related to Tesseract.
- Clean up tests, CI/CD, Dockerfiles, and packaging metadata that install or exercise Tesseract.
- Maintain code quality, minimal disruption to remaining features, and proper deprecation/breaking-change communication.

## 2. High-Level Milestones

1. **Deprecation Announcement (optional)**
   - Communicate planned removal in a maintainer discussion or in the next release notes.
2. **Code Removal**
   - Prune Tesseract-specific modules and plugin code.
   - Remove corresponding API parameters and defaults.
3. **CLI and Parser Cleanup**
   - Strip out all `--tesseract-*` flags and the `tesseract` PDF-renderer.
4. **Documentation Updates**
   - Remove Tesseract sections from README, docs/, and translations.
5. **Tests and CI Adjustments**
   - Delete or refactor tests that depend on Tesseract.
   - Update GitHub workflows and Dockerfiles to drop Tesseract installation.
6. **Final Verification and Release**
   - Run pre-commit, linters, and remaining tests.
   - Bump major version to signal breaking change.

## 3. Detailed Steps

### 3.0 Test Baseline

- [x] Run full test suite and capture current failures after partial removal.

### 3.1 Remove Tesseract Execution Layer

- [x] Delete `src/ocrmypdf/_exec/tesseract.py` and all associated tests/utilities.
- [x] Remove the `tesseract_ocr` plugin under `src/ocrmypdf/builtin_plugins/tesseract_ocr.py`.
- [x] Remove imports, references, and calls to `ocrmypdf._exec.tesseract` in pipelines and plugin registration.

### 3.2 Strip CLI Options and API Parameters

- [x] In `src/ocrmypdf/api.py`, remove parameters:
  - `tesseract_config`
  - `tesseract_pagesegmode`
  - `tesseract_oem`
  - `tesseract_thresholding`
  - `tesseract_timeout`
  - `tesseract_non_ocr_timeout`
  - `tesseract_downsample_above`
  - `tesseract_downsample_large_images`
- [x] In the CLI parser, remove all `--tesseract-*` flags and the tesseract PDF renderer option.

### 3.3 Update Pipelines

- [x] Adjust OCR pipeline (`src/ocrmypdf/_pipelines/ocr.py`) to skip or remove the OCR stage, as no Tesseract-based OCR is available.

### 3.4 Clean Up Documentation

- [ ] **Root README.md**: remove Tesseract description and installation snippets.
- [ ] **Translations (README_ZH.md)**: synchronize removal of Tesseract sections.
- [ ] **docs/**:
  - Remove or rewrite `advanced.md` sections on Tesseract timeouts, downsampling, and configuration.
  - Remove Tesseract invocation examples from `cookbook.md`, `introduction.md`, `installation.md`, `languages.md`, `docker.md`, and `cloud.md`.
  - Amend `release_notes.md` to note the breaking change.

### 3.5 Adjust CI/CD and Dockerfiles

- [ ] **.docker/Dockerfile** and **.docker/Dockerfile.alpine**: remove `apt install tesseract-ocr*` or `apk add tesseract-ocr` lines.
- [ ] **.github/workflows/build.yml**: drop Tesseract PPA/matrix builds and Chocolatey installs.

### 3.6 Remove or Refactor Tests

- [ ] Locate tests under `tests/` that invoke Tesseract (e.g., test plugins, integration tests), and remove or mark them as xfail/skip.

### 3.7 Final Cleanup and Release

- [ ] Run `pre-commit run --all-files` to catch formatting or style issues.
- [ ] Execute remaining test suite to confirm functionality unaffected by removal.
- [ ] Bump project major version in `pyproject.toml` and update changelog.

## 4. Deprecation and Communication

- This removal is a **breaking change**. It should land in the next major version (e.g., 14.0.0).
- Update CHANGELOG and Release Notes to clearly document that Tesseract support has been dropped.

---

*Plan authored to guide maintainers through a systematic removal of Tesseract integration.*