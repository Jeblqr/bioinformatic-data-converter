#!/bin/bash
# Demonstration script for Bioinformatics Data Converter

echo "================================================================================"
echo "BIOINFORMATICS DATA CONVERTER - DEMONSTRATION"
echo "================================================================================"
echo ""

# Demo 1: Show supported patterns
echo "Demo 1: Show all supported column name patterns"
echo "--------------------------------------------------------------------------------"
python3 cli.py --show-patterns | head -40
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 2: File information
echo "Demo 2: Inspect genomics GWAS data"
echo "--------------------------------------------------------------------------------"
python3 cli.py -i test_data/genomics_gwas.tsv --info-only
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 3: Auto-suggest conversion
echo "Demo 3: Convert genomics data with auto-suggested mappings"
echo "--------------------------------------------------------------------------------"
python3 cli.py -i test_data/genomics_gwas.tsv -o /tmp/demo_genomics.tsv --auto-suggest --verbose
echo ""
echo "Output:"
zcat /tmp/demo_genomics.tsv | head -3
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 4: Different data types
echo "Demo 4: Convert transcriptomics data"
echo "--------------------------------------------------------------------------------"
python3 cli.py -i test_data/transcriptomics_rnaseq.csv -o /tmp/demo_transcriptomics.tsv --auto-suggest --verbose
echo ""
read -p "Press Enter to continue..."
echo ""

echo "Demo 5: Convert proteomics data"
echo "--------------------------------------------------------------------------------"
python3 cli.py -i test_data/proteomics_data.tsv -o /tmp/demo_proteomics.tsv --auto-suggest --verbose
echo ""
read -p "Press Enter to continue..."
echo ""

echo "Demo 6: Convert metabolomics data"
echo "--------------------------------------------------------------------------------"
python3 cli.py -i test_data/metabolomics_data.csv -o /tmp/demo_metabolomics.tsv --auto-suggest --verbose
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 7: Manual mapping
echo "Demo 7: Manual column mapping"
echo "--------------------------------------------------------------------------------"
echo "Using custom mapping: CHR=chr,POS=pos,P=pval"
python3 cli.py -i test_data/genomics_gwas.tsv -o /tmp/demo_manual.tsv --map "CHR=chr,POS=pos,P=pval" --keep-unmatched --verbose
echo ""
read -p "Press Enter to continue..."
echo ""

# Demo 8: Different output formats
echo "Demo 8: Output in different formats"
echo "--------------------------------------------------------------------------------"
echo "CSV format:"
python3 cli.py -i test_data/genomics_gwas.tsv -o /tmp/demo_output.csv --auto-suggest --output-format csv --no-compression
ls -lh /tmp/demo_output.csv
echo ""
echo "Parquet format:"
python3 cli.py -i test_data/genomics_gwas.tsv -o /tmp/demo_output.parquet --auto-suggest --output-format parquet
ls -lh /tmp/demo_output.parquet
echo ""

echo "================================================================================"
echo "DEMONSTRATION COMPLETE!"
echo "================================================================================"
echo ""
echo "Key Features Demonstrated:"
echo "  ✓ Multi-omics data type support (genomics, transcriptomics, proteomics, metabolomics)"
echo "  ✓ Auto-detection of data types and column mappings"
echo "  ✓ Manual column mapping capability"
echo "  ✓ Multiple output formats (TSV, CSV, Parquet)"
echo "  ✓ Compression support (gzip)"
echo "  ✓ File information inspection"
echo ""
echo "Try interactive mode yourself:"
echo "  python3 cli.py -i test_data/genomics_gwas.tsv -o output.tsv --interactive"
echo ""
