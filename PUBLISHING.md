# Publishing Guide for Bioconverter

Instructions for publishing the bioconverter package to official repositories (PyPI for Python and CRAN for R).

---

## Table of Contents

1. [Publishing to PyPI (Python)](#publishing-to-pypi-python)
2. [Publishing to CRAN (R)](#publishing-to-cran-r)
3. [Pre-Publication Checklist](#pre-publication-checklist)
4. [Version Management](#version-management)

---

## Publishing to PyPI (Python)

PyPI (Python Package Index) is the official repository for Python packages.

### Prerequisites

1. **Create PyPI Account**
   - Register at https://pypi.org/account/register/
   - Register at https://test.pypi.org/account/register/ (for testing)
   - Enable 2FA for security

2. **Install Publishing Tools**
   ```bash
   pip install --upgrade pip setuptools wheel twine
   ```

### Step-by-Step Publication

#### 1. Prepare Your Package

```bash
cd /path/to/bioinformatic-data-converter

# Verify setup.py is correct
python setup.py check

# Run tests (if available)
pytest tests/

# Check code quality
flake8 *.py
black --check *.py
```

#### 2. Build Distribution Packages

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build source distribution and wheel
python setup.py sdist bdist_wheel

# Verify the build
ls -lh dist/
```

You should see:
- `bioconverter-0.1.0.tar.gz` (source distribution)
- `bioconverter-0.1.0-py3-none-any.whl` (wheel distribution)

#### 3. Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# You'll be prompted for credentials
# Username: __token__
# Password: your-testpypi-token

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ bioconverter

# Test the installed package
python -c "import convertor; print('Success!')"
```

#### 4. Upload to PyPI

```bash
# Upload to real PyPI
twine upload dist/*

# You'll be prompted for credentials
# Username: __token__
# Password: your-pypi-token
```

#### 5. Verify Publication

```bash
# Install from PyPI
pip install bioconverter

# Test
bioconverter --help
```

Visit your package page: https://pypi.org/project/bioconverter/

### Using API Tokens (Recommended)

Create `.pypirc` in your home directory:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...your-token...

[testpypi]
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw...your-token...
```

Then simply:
```bash
twine upload dist/*
```

### Updating Your Package

```bash
# Update version in setup.py
# version="0.1.1"

# Rebuild and upload
rm -rf build/ dist/ *.egg-info/
python setup.py sdist bdist_wheel
twine upload dist/*
```

---

## Publishing to CRAN (R)

CRAN (Comprehensive R Archive Network) is the official repository for R packages.

### Prerequisites

1. **Required Tools**
   - R >= 3.6.0
   - RStudio (recommended)
   - Rtools (Windows) or Xcode (macOS)

2. **Install Development Packages**
   ```r
   install.packages(c("devtools", "roxygen2", "testthat", "rcmdcheck"))
   ```

### Step-by-Step Publication

#### 1. Prepare Your Package

```r
library(devtools)
library(roxygen2)

# Set working directory to package root
setwd("/path/to/bioinformatic-data-converter")

# Generate documentation from roxygen2 comments
document()

# Check package structure
check_built()
```

#### 2. Run R CMD check

The most important step - CRAN requires zero ERRORS, WARNINGS, or NOTES.

```r
# Run comprehensive checks
check_results <- rcmdcheck::rcmdcheck()

# View results
print(check_results)
```

Common issues to fix:
- Missing documentation
- Non-standard file structure
- Dependency issues
- Code that writes to home directory
- Long-running examples (>5 seconds)

#### 3. Additional CRAN Requirements

**Create/Update Required Files:**

1. **LICENSE** file:
   ```
   MIT License
   
   Copyright (c) 2024 Bioconverter Contributors
   
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction...
   ```

2. **NEWS.md** file:
   ```markdown
   # bioconverter 0.1.0
   
   * Initial CRAN submission
   * Support for genomics, transcriptomics, proteomics, metabolomics
   * Interactive column mapping
   * Large file processing with chunking
   ```

3. **cran-comments.md** file:
   ```markdown
   ## Test environments
   * local R installation, R 4.3.0
   * ubuntu 20.04 (on GitHub Actions), R 4.3.0
   * win-builder (devel)
   
   ## R CMD check results
   0 errors | 0 warnings | 0 notes
   
   ## Downstream dependencies
   There are currently no downstream dependencies for this package.
   ```

#### 4. Test on Multiple Platforms

```r
# Check on Windows
devtools::check_win_devel()
devtools::check_win_release()

# Check on macOS (if not already on macOS)
devtools::check_mac_release()

# Use rhub for comprehensive testing
library(rhub)
check(platform = c(
  "windows-x86_64-devel",
  "ubuntu-gcc-release",
  "macos-highsierra-release-cran"
))
```

#### 5. Build Source Package

```r
# Build the package
devtools::build()

# This creates: bioconverter_0.1.0.tar.gz
```

Or from command line:
```bash
R CMD build .
```

#### 6. Final Checks

```bash
# Final comprehensive check
R CMD check --as-cran bioconverter_0.1.0.tar.gz
```

Must return: `Status: OK`

#### 7. Submit to CRAN

**Option A: Web Form (Recommended for First Submission)**

1. Go to: https://cran.r-project.org/submit.html
2. Upload `bioconverter_0.1.0.tar.gz`
3. Fill in the form:
   - Package name: bioconverter
   - Version: 0.1.0
   - Your name and email
   - Confirm you ran R CMD check --as-cran
4. Submit

**Option B: devtools (After First Submission)**

```r
devtools::release()
```

This will:
- Run final checks
- Build the package
- Submit to CRAN
- Update cran-comments.md

#### 8. Respond to CRAN Review

CRAN maintainers will review your package (usually within 1-2 weeks). They may:

1. **Auto-reject** if critical issues found
   - Fix issues and resubmit

2. **Request changes**
   - Make requested changes
   - Increment version (e.g., 0.1.0 -> 0.1.1)
   - Resubmit with explanation

3. **Accept**
   - Package will be published within 24 hours
   - You'll receive confirmation email

### CRAN Package Maintenance

After acceptance:

```r
# For updates
# 1. Update version in DESCRIPTION
# 2. Add changes to NEWS.md
# 3. Run all checks
# 4. Resubmit

# Updates usually processed faster (1-3 days)
```

---

## Pre-Publication Checklist

### Python Package Checklist

- [ ] Version number updated in `setup.py`
- [ ] All dependencies listed in `setup.py` and `requirements.txt`
- [ ] README.md is comprehensive and up-to-date
- [ ] LICENSE file included
- [ ] Tests pass (`pytest`)
- [ ] Code quality checked (`flake8`, `black`)
- [ ] Package builds successfully
- [ ] Tested on TestPyPI
- [ ] Documentation is complete
- [ ] CHANGELOG.md updated

### R Package Checklist

- [ ] Version number updated in `DESCRIPTION`
- [ ] All dependencies listed in `DESCRIPTION`
- [ ] NAMESPACE file is correct
- [ ] All functions documented with roxygen2
- [ ] LICENSE file included
- [ ] NEWS.md updated
- [ ] cran-comments.md created
- [ ] `R CMD check --as-cran` returns 0 errors, 0 warnings, 0 notes
- [ ] Tested on multiple platforms (Windows, macOS, Linux)
- [ ] Examples run in < 5 seconds each
- [ ] No writes to home directory without permission
- [ ] All URLs in documentation are valid
- [ ] Package size < 5MB (excluding data)

---

## Version Management

### Semantic Versioning

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: Add functionality (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

Examples:
- `0.1.0` - Initial release
- `0.1.1` - Bug fixes
- `0.2.0` - New features
- `1.0.0` - Stable API

### Release Workflow

1. **Development**
   ```bash
   git checkout -b develop
   # Make changes
   git commit -m "Add feature X"
   ```

2. **Pre-release Testing**
   ```bash
   # Update version to 0.2.0-rc1
   # Test thoroughly
   ```

3. **Release**
   ```bash
   # Update version to 0.2.0
   git tag -a v0.2.0 -m "Release version 0.2.0"
   git push origin v0.2.0
   ```

4. **Publish**
   ```bash
   # Python
   python setup.py sdist bdist_wheel
   twine upload dist/*
   
   # R
   R CMD check --as-cran package_0.2.0.tar.gz
   # Submit to CRAN
   ```

### Maintaining Both Packages

**When to Update:**
- Bug fixes: Update both immediately
- New features: Update both simultaneously
- Keep version numbers synchronized

**Release Strategy:**
1. Develop and test changes
2. Update version in both `setup.py` and `DESCRIPTION`
3. Update both `README.md` and `MANUAL.md`
4. Test both packages thoroughly
5. Release to PyPI first (faster)
6. Then submit to CRAN (longer review)

---

## Troubleshooting

### PyPI Issues

**Problem**: "File already exists"
```bash
# Solution: Increment version number
# Cannot reuse version numbers on PyPI
```

**Problem**: "Invalid distribution"
```bash
# Solution: Check setup.py
python setup.py check --restructuredtext
```

### CRAN Issues

**Problem**: "Non-standard file"
```r
# Solution: Remove or move files
# CRAN doesn't allow certain file types
# Move data to inst/extdata/
```

**Problem**: "Examples too slow"
```r
# Solution: Use \dontrun{} or \donttest{}
#' @examples
#' \dontrun{
#'   # Long-running example
#' }
```

**Problem**: "Writing to home directory"
```r
# Solution: Use tempdir()
temp_dir <- tempdir()
output_file <- file.path(temp_dir, "output.txt")
```

---

## Additional Resources

### Python (PyPI)
- PyPI Documentation: https://packaging.python.org/
- TestPyPI: https://test.pypi.org/
- Twine Documentation: https://twine.readthedocs.io/

### R (CRAN)
- CRAN Repository Policy: https://cran.r-project.org/web/packages/policies.html
- R Packages Book: https://r-pkgs.org/
- Writing R Extensions: https://cran.r-project.org/doc/manuals/r-release/R-exts.html
- CRAN Submission Checklist: https://cran.r-project.org/web/packages/submission_checklist.html

### Testing Platforms
- GitHub Actions: https://github.com/features/actions
- Travis CI: https://travis-ci.org/
- AppVeyor (Windows): https://www.appveyor.com/

---

## Support

For questions or issues with publication:

- **Python/PyPI**: https://github.com/Jeblqr/bioinformatic-data-converter/issues
- **R/CRAN**: CRAN team will contact you directly via email
- **General**: Open an issue on GitHub

---

**Good luck with your publication!**
