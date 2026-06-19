# Dataset Schemas

This directory contains JSON Schema (Draft 7) definitions for all StellarDataLab datasets.

## Schema Files

Each dataset has a corresponding `.schema.json` file that defines:

- Required fields
- Field types and constraints
- Validation rules (patterns, ranges, enums)
- Examples

## JSON Schema Reference

Learn more about JSON Schema:
- [JSON Schema Official Docs](https://json-schema.org/)
- [JSON Schema Draft 7](https://json-schema.org/specification-links.html#draft-7)

## Using Schemas

### Validate Python Data

```python
import jsonschema
import json

# Load schema
with open('schemas/transaction.schema.json') as f:
    schema = json.load(f)

# Validate data
row = {...}
jsonschema.validate(instance=row, schema=schema)  # Raises ValidationError if invalid
```

### Example Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Transaction",
  "type": "object",
  "required": ["tx_id", "timestamp", "sender", "receiver", "amount"],
  "properties": {
    "tx_id": {
      "type": "string",
      "description": "Unique transaction ID",
      "minLength": 64
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp"
    },
    "amount": {
      "type": "number",
      "minimum": 0,
      "description": "Transaction amount in stroops"
    }
  }
}
```

## Contributing

When adding a new dataset, create a corresponding schema file that:

1. Follows JSON Schema Draft 7 syntax
2. Includes `title` and `description`
3. Specifies all `required` fields
4. Documents each field with type and constraints
5. Includes examples or patterns where applicable

See [docs/schema-guide.md](../docs/schema-guide.md) for detailed schema design guidelines.
