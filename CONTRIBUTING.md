# Contributing to StellarDataLab

Welcome! We're excited to have you contribute to StellarDataLab. This guide will walk you through adding a new dataset in about 30 minutes.

## Quick Start

### 1. Set Up Local Environment (5 minutes)

```bash
# Clone repository
git clone https://github.com/johnsaviour56-ship-it/stellar-data-lab.git
cd stellar-data-lab

# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify setup
pytest tests/ -q
```

### 2. Create Metadata File (5 minutes)

Create `datasets/metadata/my_dataset.metadata.yml`:

```yaml
name: "My New Dataset"
version: "1.0"
created_date: "2024-01-20"

description: |
  Brief description of what this dataset contains and why it's useful.

source:
  type: "api"  # or "csv", "json", "github", etc.
  endpoint: "https://api.example.com/data"
  documentation: "https://example.com/docs"

collection:
  method: "API fetch with pagination"
  script: "scripts/collect_my_data.py"
  frequency: "daily"  # or "weekly", "monthly", "once"

schema:
  file: "schemas/my_dataset.schema.json"
  version: "1.0"

transformations:
  - name: "normalize"
    description: "Normalize addresses and timestamps"

labels: []

quality_checks:
  - duplicates: "Remove by id"
  - nulls: "Reject rows with null id"
```

### 3. Define Schema (5 minutes)

Create `schemas/my_dataset.schema.json`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "My Dataset",
  "type": "object",
  "required": ["id", "timestamp", "value"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp"
    },
    "value": {
      "type": "number",
      "minimum": 0,
      "description": "Data value"
    }
  }
}
```

### 4. Write Collection Script (10 minutes)

Create `scripts/collect_my_data.py`:

```python
"""Collect data from API."""

import csv
import logging
import requests

logger = logging.getLogger(__name__)


def collect_my_data(output_file: str, **kwargs) -> int:
    """
    Collect data from API and write to CSV.
    
    Args:
        output_file: Path to output CSV file
        kwargs: Additional parameters (date_range, etc.)
    
    Returns:
        Number of records collected
    """
    api_url = "https://api.example.com/data"
    
    rows = []
    page = 1
    
    while True:
        try:
            response = requests.get(api_url, params={"page": page}, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                break
            
            for item in data:
                rows.append({
                    "id": item["id"],
                    "timestamp": item["created_at"],
                    "value": item["amount"]
                })
            
            page += 1
            logger.info(f"Fetched page {page-1}")
            
        except requests.RequestException as e:
            logger.error(f"API error: {str(e)}")
            if not rows:  # If no data fetched, fail
                raise
            break
    
    # Write to CSV
    if not rows:
        raise ValueError("No data collected")
    
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "timestamp", "value"])
        writer.writeheader()
        writer.writerows(rows)
    
    logger.info(f"Collected {len(rows)} records → {output_file}")
    return len(rows)


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    output = sys.argv[1] if len(sys.argv) > 1 else "datasets/raw/my_data_raw.csv"
    collect_my_data(output)
```

### 5. Test Locally (5 minutes)

```bash
# Run collection script
python scripts/collect_my_data.py

# Check raw data
head -5 datasets/raw/my_data_raw.csv

# Run tests (optional)
pytest tests/ -v
```

### 6. Submit Pull Request

```bash
# Create feature branch
git checkout -b feature/my-dataset

# Commit files
git add datasets/metadata/my_dataset.metadata.yml \
         schemas/my_dataset.schema.json \
         scripts/collect_my_data.py

git commit -m "Add my_dataset: [brief description]"

# Push and create PR
git push origin feature/my-dataset
```

**PR Title**: `Add my_dataset: [description]`

**PR Description**:
```
## Dataset: My New Dataset

**Source**: [API endpoint or data source]

**Purpose**: [Why this dataset is useful]

**Rows**: [Expected row count]

**Columns**: [List of main columns]

## Checklist

- [ ] Metadata file complete
- [ ] Schema file valid JSON
- [ ] Collection script tested locally
- [ ] No API keys in code
- [ ] README updated (if needed)
```

CI will automatically validate your dataset. Once approved, it will be merged and published!

## Best Practices

### Code Style

- Python: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Format with `black`: `black scripts/`
- Lint with `flake8`: `flake8 scripts/`

### Documentation

- Add docstrings to functions
- Include examples in comments
- Document error handling
- Explain any assumptions

### Error Handling

- Log errors clearly
- Don't silently fail
- Provide helpful error messages
- Handle API rate limits gracefully

### Testing

- Write unit tests if complex
- Test edge cases (empty data, malformed records)
- Run full test suite: `pytest tests/ -v`

## Troubleshooting

**"ModuleNotFoundError"**
- Ensure venv is activated
- Run `pip install -r requirements.txt`

**"Failed to import schema"**
- Check schema file path is correct
- Validate JSON: `python -m json.tool schemas/my_dataset.schema.json`

**"API request timeout"**
- Increase timeout in requests call
- Check network connectivity
- Verify API endpoint is accessible

**"Schema validation failed"**
- Review test data against schema
- Check field types and formats
- Use JSON Schema validator: https://www.jsonschemavalidator.net/

## Getting Help

- **Questions?** Open an [Issue](https://github.com/johnsaviour56-ship-it/stellar-data-lab/issues)
- **Ideas?** Start a [Discussion](https://github.com/johnsaviour56-ship-it/stellar-data-lab/discussions)
- **Bug?** Report with reproduction steps

## Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2_1/code_of_conduct/). TL;DR: Be respectful and inclusive.

---

Thank you for contributing! 🌟
