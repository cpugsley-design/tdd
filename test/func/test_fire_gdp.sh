
#!/bin/bash

# Functional tests for the fire-GDP plotting program.

set -e

# Move to the repository root.
cd "$(dirname "$0")/../.."

# Download ssshtest if necessary.
if [ ! -f ssshtest ]; then
    curl -fsSL \
        https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest \
        -o ssshtest
fi

# Load the ssshtest functions.
. ./ssshtest

# Define input files.
CO2_FILE="test/data/test_co2.csv"
GDP_FILE="test/data/test_gdp.csv"

# Create a temporary directory for output files.
OUTPUT_DIR=$(mktemp -d)

# Clean up generated files when the script exits.
trap 'rm -rf "$OUTPUT_DIR"' EXIT


# Test 1: Valid country and successful plot generation.
file_name="$OUTPUT_DIR/australia.png"

run test_valid_country \
    python src/scatter.py \
    --co2_file "$CO2_FILE" \
    --gdp_file "$GDP_FILE" \
    --country "Australia" \
    --output "$file_name"

assert_exit_code 0
assert_equal "$file_name" "$(ls "$file_name")"


# Test 2: Another valid country.
file_name="$OUTPUT_DIR/ireland.png"

run test_second_country \
    python src/scatter.py \
    --co2_file "$CO2_FILE" \
    --gdp_file "$GDP_FILE" \
    --country "Ireland" \
    --output "$file_name"

assert_exit_code 0
assert_equal "$file_name" "$(ls "$file_name")"


# Test 3: Country not present in the dataset.
run test_invalid_country \
    python src/scatter.py \
    --co2_file "$CO2_FILE" \
    --gdp_file "$GDP_FILE" \
    --country "Brazil" \
    --output "$OUTPUT_DIR/invalid.png"

assert_exit_code 1


# Test 4: Missing required argument.
run test_missing_argument \
    python src/scatter.py \
    --co2_file "$CO2_FILE" \
    --gdp_file "$GDP_FILE" \
    --output "$OUTPUT_DIR/missing.png"

assert_exit_code 2


# Test 5: Missing input file.
run test_missing_file \
    python src/scatter.py \
    --co2_file "nonexistent.csv" \
    --gdp_file "$GDP_FILE" \
    --country "Australia" \
    --output "$OUTPUT_DIR/missing_file.png"

assert_exit_code 1
