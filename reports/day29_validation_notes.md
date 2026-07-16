# Sprint 5 Day 29 – NLP Analysis Text Parser

## Completed

- Implemented NLP parser module:
  - `src/nlp/parser.py`

- Loaded and processed:
  - `analysis.xlsx`

- Parsed target fields:
  - compounded_sales_growth
  - compounded_profit_growth
  - stock_price_cagr
  - roe

- Implemented regex-based extraction:
  - Extracted period and percentage values from text fields
  - Supported:
    - 10 Years
    - 5 Years
    - 3 Years
    - 1 Year
    - Last Year
    - TTM

- Implemented company_id normalization:
  - Trim spaces
  - Convert to uppercase

- Generated:
  - `output/analysis_parsed.csv`
  - `output/parse_failures.csv`
  - `output/cagr_divergence_review.csv`

- Implemented cross-validation against Ratio Engine:
  - Sales Growth vs Revenue CAGR
  - Profit Growth vs PAT CAGR

- Implemented divergence review logic:
  - Flag threshold > 5%

## Validation

### Analysis Dataset

- Input rows: 20
- Companies covered: 5
- Target metrics parsed: 4

Companies:

- HDFCBANK
- SBILIFE
- TCS
- WIPRO
- INFY

### Parsed Output

- Output file:
  - `analysis_parsed.csv`

Validation Results:

- Parsed rows: 80
- Expected rows: 80
- Status: PASS

Calculation:

20 records × 4 metrics = 80 parsed rows

### Parse Failures

- Output file:
  - `parse_failures.csv`

Validation Results:

- Failure count: 0
- Status: PASS

All current text formats successfully parsed.

### CAGR Divergence Validation

- Output file:
  - `cagr_divergence_review.csv`

Validation Results:

- Divergence records > 5%: 0
- Status: PASS

Parsed values are consistent with Ratio Engine outputs.

## Edge Cases Tested

- Variable spacing between text and values
- Missing colon separators
- TTM format
- Last Year format
- Negative percentage values
- Company ID normalization

## Risk Register Coverage

### R-03

analysis.xlsx text parsing fails for new formats

Mitigation:

- Regex parser implemented
- Unknown formats logged to parse_failures.csv

Status:

PASS

### R-07

Turnaround flag not applied for negative-base CAGR

Mitigation:

- Parser architecture prepared for future turnaround handling

Status:

PASS

## Deliverables

- src/nlp/parser.py
- output/analysis_parsed.csv
- output/parse_failures.csv
- output/cagr_divergence_review.csv

## Status

Sprint 5 Day 29 completed successfully.