#!/usr/bin/env Rscript
#' R Example: Using bioconverter for data conversion
#'
#' This example demonstrates how to use bioconverter in R scripts.

library(bioconverter)
library(dplyr)

cat("=============================================================\n")
cat("bioconverter R Examples\n")
cat("=============================================================\n\n")

# Example 1: Basic single file conversion
cat("=============================================================\n")
cat("Example 1: Basic Single File Conversion\n")
cat("=============================================================\n")

tryCatch({
  result <- convert_file(
    input_file = "test_data/genomics_gwas.tsv",
    output_file = "output_gwas_r.tsv",
    verbose = TRUE
  )
  
  cat("\nResult dimensions:", nrow(result), "rows,", ncol(result), "columns\n")
  cat("Columns:", paste(colnames(result), collapse = ", "), "\n")
  cat("\nFirst few rows:\n")
  print(head(result))
  cat("\n✓ Output saved to: output_gwas_r.tsv\n")
  
}, error = function(e) {
  cat("⚠ Error in Example 1:", conditionMessage(e), "\n")
})


# Example 2: Auto-suggest column mapping
cat("\n=============================================================\n")
cat("Example 2: Auto-suggest Column Mapping\n")
cat("=============================================================\n")

tryCatch({
  # Get suggested mappings
  suggestions <- auto_suggest_mapping(
    input_file = "test_data/transcriptomics_rnaseq.csv",
    n_rows = 100
  )
  
  cat("\nSuggested column mappings:\n")
  for (name in names(suggestions)) {
    cat(sprintf("  %-20s -> %s\n", name, suggestions[[name]]))
  }
  
  # Apply the mapping
  result <- convert_file(
    input_file = "test_data/transcriptomics_rnaseq.csv",
    output_file = "output_rnaseq_r.tsv",
    column_mapping = suggestions,
    verbose = FALSE
  )
  
  cat(sprintf("\n✓ Conversion complete: %d rows, %d columns\n", 
              nrow(result), ncol(result)))
  
}, error = function(e) {
  cat("⚠ Error in Example 2:", conditionMessage(e), "\n")
})


# Example 3: Custom column mapping
cat("\n=============================================================\n")
cat("Example 3: Custom Column Mapping\n")
cat("=============================================================\n")

tryCatch({
  # Define custom mapping
  custom_mapping <- list(
    chr = "chr",
    pos = "pos",
    pval = "pval",
    beta = "beta",
    se = "se"
  )
  
  cat("\nCustom mapping:\n")
  for (name in names(custom_mapping)) {
    cat(sprintf("  %s -> %s\n", name, custom_mapping[[name]]))
  }
  
  # Apply custom mapping
  result <- convert_file(
    input_file = "test_data/genomics_gwas.tsv",
    output_file = "output_custom_r.tsv",
    column_mapping = custom_mapping,
    keep_unmatched = TRUE,
    verbose = FALSE
  )
  
  cat(sprintf("\n✓ Result columns: %s\n", 
              paste(colnames(result), collapse = ", ")))
  
}, error = function(e) {
  cat("⚠ Error in Example 3:", conditionMessage(e), "\n")
})


# Example 4: Get supported column patterns
cat("\n=============================================================\n")
cat("Example 4: View Supported Column Patterns\n")
cat("=============================================================\n")

tryCatch({
  patterns <- get_column_patterns()
  
  cat("\nSupported omics types:\n")
  cat("  -", paste(names(patterns), collapse = "\n  - "), "\n")
  
  cat("\nExample: Genomics patterns (first 5):\n")
  genomics_patterns <- patterns$genomics
  if (length(genomics_patterns) > 0) {
    for (i in 1:min(5, length(genomics_patterns))) {
      cat(sprintf("  %s\n", names(genomics_patterns)[i]))
    }
  }
  
}, error = function(e) {
  cat("⚠ Error in Example 4:", conditionMessage(e), "\n")
})


# Example 5: Generate conversion report
cat("\n=============================================================\n")
cat("Example 5: Generate Conversion Report\n")
cat("=============================================================\n")

tryCatch({
  result <- convert_file(
    input_file = "test_data/proteomics_data.tsv",
    output_file = "output_proteomics_r.tsv",
    verbose = TRUE
  )
  
  cat("\n✓ Conversion complete\n")
  
}, error = function(e) {
  cat("⚠ Error in Example 5:", conditionMessage(e), "\n")
})


# Example 6: Return data without saving
cat("\n=============================================================\n")
cat("Example 6: Return Data Without Saving File\n")
cat("=============================================================\n")

tryCatch({
  # Convert data without saving to file
  result <- convert_file(
    input_file = "test_data/genomics_gwas.tsv",
    output_file = NULL,  # Don't save, just return data
    verbose = FALSE
  )
  
  cat(sprintf("\n✓ Data converted: %d rows, %d columns\n", 
              nrow(result), ncol(result)))
  cat("Columns:", paste(colnames(result), collapse = ", "), "\n")
  
  # You can now work with the data directly
  if ("pval" %in% colnames(result)) {
    n_significant <- sum(result$pval < 0.05, na.rm = TRUE)
    cat(sprintf("Found %d significant variants (p < 0.05)\n", n_significant))
  }
  
}, error = function(e) {
  cat("⚠ Error in Example 6:", conditionMessage(e), "\n")
})


# Example 7: Process large files with chunking
cat("\n=============================================================\n")
cat("Example 7: Process Large Files with Chunking\n")
cat("=============================================================\n")

tryCatch({
  cat("\nProcessing file with chunking...\n")
  
  # Suggest optimal chunk size
  chunk_size <- suggest_chunk_size("test_data/genomics_gwas.tsv")
  cat(sprintf("Suggested chunk size: %d rows\n", chunk_size))
  
  # Process large file
  process_large_file(
    filename = "test_data/genomics_gwas.tsv",
    output_file = "output_large_r.tsv",
    chunk_size = 1000,  # Use smaller for demo
    verbose = TRUE
  )
  
  cat("\n✓ Large file processed successfully\n")
  
}, error = function(e) {
  cat("⚠ Error in Example 7:", conditionMessage(e), "\n")
})


# Summary
cat("\n=============================================================\n")
cat("All examples completed!\n")
cat("=============================================================\n")
cat("\nGenerated output files:\n")
output_files <- c(
  "output_gwas_r.tsv",
  "output_rnaseq_r.tsv",
  "output_custom_r.tsv",
  "output_proteomics_r.tsv",
  "output_large_r.tsv"
)

for (f in output_files) {
  if (file.exists(f)) {
    cat(sprintf("  ✓ %s\n", f))
  }
}

cat("\nNote: Some examples may show errors if test data files don't exist.\n")
cat("This is normal if running outside the test environment.\n")
