# Implementation Notes: Native R and Python Packages

## Overview

The bioconverter project now provides two completely independent implementations:

1. **Python Package** (`bioconverter/`): Native Python implementation
2. **R Package** (`R/`): Native R implementation

Both packages share consistent logic and functionality but are implemented entirely in their respective languages **without any cross-language dependencies**.

## Key Changes (Version 0.2.0)

### What Changed

**Before:**
- R package was a wrapper around the Python package using `reticulate`
- R package required Python and the Python bioconverter package to be installed
- R functions were essentially thin wrappers calling Python functions

**After:**
- R package is a pure R implementation
- No Python dependencies required for R package
- No R dependencies required for Python package
- Both packages can be used independently

### R Package Implementation

The R package now includes native implementations of:

1. **Pattern Matching** (`R/patterns.R`)
   - `create_column_patterns()`: Define regex patterns for column name matching
   - `match_columns()`: Match column names to standardized field names
   - Support for all omics types: genomics, transcriptomics, proteomics, metabolomics

2. **File I/O** (`R/file_io.R`)
   - `detect_file_format()`: Auto-detect file format from extension
   - `read_data()`: Read various file formats (CSV, TSV, VCF, compressed)
   - `read_vcf_file()`: Special handling for VCF files
   - Graceful fallback to base R when `readr` is not available

3. **Conversion** (`R/converter.R`)
   - `convert_single_file()`: Convert a single file
   - `convert_multiple_files()`: Batch convert multiple files
   - `standardize_columns()`: Apply column name standardization

4. **Interactive Features** (`R/interactive.R`)
   - `auto_suggest_mapping()`: Automatically suggest column mappings
   - `auto_detect_omics_type()`: Detect the type of omics data
   - `process_large_file()`: Handle large files with chunking
   - `suggest_chunk_size()`: Recommend optimal chunk size

5. **Main Interface** (`R/bioconverter.R`)
   - `convert_file()`: High-level conversion function
   - `get_column_patterns()`: Retrieve supported patterns

### Dependencies

**Python Package:**
- pandas
- No R dependencies

**R Package:**
- readr (recommended but optional - falls back to base R if not available)
- No Python dependencies

### Compatibility

Both implementations:
- Support the same file formats
- Use the same column name patterns
- Produce compatible output
- Handle the same omics types
- Support the same features (auto-detection, chunking, etc.)

## Testing

Both packages have been tested independently:

### Python Tests
- Pattern creation and matching ✓
- File format detection ✓
- File conversion ✓
- Auto-suggest mapping ✓

### R Tests
- Pattern creation and matching ✓
- File format detection ✓
- File conversion ✓
- Auto-suggest mapping ✓
- Omics type detection ✓
- High-level convert_file function ✓

## Usage Differences

While the packages have consistent functionality, there are minor API differences due to language conventions:

### Python
```python
from bioconverter import convert_single_file, auto_suggest_mapping

# Convert file
result = convert_single_file(
    filename="data.tsv",
    column_mapping={"CHR": "chr", "POS": "pos"},
    verbose=True
)
```

### R
```r
library(bioconverter)

# Convert file
result <- convert_file(
  input_file = "data.tsv",
  column_mapping = list(CHR = "chr", POS = "pos"),
  verbose = TRUE
)
```

## Migration Guide

For existing R package users who were using the Python-backed version:

1. **No changes required** to your R code - the API remains the same
2. **Remove Python dependency** - you can uninstall Python and the Python bioconverter package
3. **Optional: Install readr** - for better performance with large files, but not required
4. **Benefits:**
   - Simpler installation (no need to manage Python environment)
   - Better R integration
   - Same functionality

## Future Development

Both packages will be maintained and developed in parallel:
- Bug fixes will be applied to both
- New features will be implemented in both
- API consistency will be maintained
- Documentation will be kept synchronized

## Contributing

When contributing new features:
1. Implement the feature in both Python and R
2. Ensure consistent behavior between implementations
3. Add tests for both implementations
4. Update documentation for both packages
