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
    filename = "test_data/transcriptomics_rnaseq.csv",
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
    generate_report = TRUE,
    report_dir = "./reports/",
    verbose = TRUE
  )
  
  cat("\n✓ Conversion complete with report\n")
  cat("✓ Check ./reports/ directory for the conversion report\n")
  
}, error = function(e) {
  cat("⚠ Error in Example 5:", conditionMessage(e), "\n")
})


# Example 6: Pipeline with dplyr
cat("\n=============================================================\n")
cat("Example 6: Integration with dplyr Pipeline\n")
cat("=============================================================\n")

tryCatch({
  # Convert data
  result <- convert_file(
    input_file = "test_data/genomics_gwas.tsv",
    output_file = NULL,  # Don't save, just return data
    verbose = FALSE
  )
  
  # Use dplyr for analysis
  if ("pval" %in% colnames(result)) {
    significant <- result %>%
      filter(pval < 0.05) %>%
      arrange(pval) %>%
      head(10)
    
    cat("\nTop 10 significant variants:\n")
    print(significant)
    
    cat(sprintf("\n✓ Found %d significant variants (p < 0.05)\n", 
                sum(result$pval < 0.05, na.rm = TRUE)))
  } else {
    cat("\n⚠ No p-value column found in the data\n")
  }
  
}, error = function(e) {
  cat("⚠ Error in Example 6:", conditionMessage(e), "\n")
})


# Example 7: Using CLI from R (alternative approach)
cat("\n=============================================================\n")
cat("Example 7: Using bioconverter CLI from R\n")
cat("=============================================================\n")

tryCatch({
  cat("\nFor interactive mapping, use the CLI:\n")
  cat("  system('bioconverter -i input.tsv -o output.tsv --interactive')\n\n")
  
  # Example: Run CLI command
  cat("Running example CLI command...\n")
  cmd <- "bioconverter -i test_data/genomics_gwas.tsv -o output_cli_r.tsv --auto-suggest"
  
  exit_code <- system(cmd)
  
  if (exit_code == 0) {
    cat("\n✓ CLI command executed successfully\n")
    cat("✓ Output saved to: output_cli_r.tsv\n")
  } else {
    cat("\n⚠ CLI command failed with exit code:", exit_code, "\n")
  }
  
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
  "output_cli_r.tsv"
)

for (f in output_files) {
  if (file.exists(f)) {
    cat(sprintf("  ✓ %s\n", f))
  }
}

cat("\nNote: Some examples may show errors if test data files don't exist.\n")
cat("This is normal if running outside the test environment.\n")
