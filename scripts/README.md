# Data Collection Scripts

This directory contains Python scripts for collecting data from various sources.

## Script Interface

All collection scripts follow a standard interface:

```python
def collect_[dataset_name](output_file: str, **kwargs) -> int:
    """
    Collect data and write to file.
    
    Args:
        output_file: Path to output CSV or JSON file
        kwargs: Additional parameters (date_range, limit, etc.)
    
    Returns:
        Number of records collected
    """
    # Implementation
    pass
```

## Available Scripts

- `collect_transactions.py` - Fetch transactions from Stellar API
- `collect_wallets.py` - Fetch wallet snapshot from Stellar API

## Running Scripts

```bash
# Run directly
python scripts/collect_transactions.py

# Run via pipeline
python -m pipeline.orchestrator process --dataset=transactions_2024
```

## Adding a New Collection Script

1. Create `scripts/collect_my_data.py`
2. Implement `collect_my_data()` function with standard interface
3. Handle errors gracefully (logging, retries)
4. Write output to `datasets/raw/`
5. Document source, method, and parameters in script docstring

## Best Practices

- **Error handling**: Log errors but don't halt on individual row failures
- **Rate limiting**: Respect API rate limits, implement backoff
- **Pagination**: Handle large result sets with pagination or streaming
- **Idempotency**: Running twice should produce same results (or document why not)
- **Reproducibility**: Include date ranges, API version, authentication method
- **Logging**: Log collection progress, counts, and any issues

## Troubleshooting

**"API rate limit exceeded"**
- Implement exponential backoff
- Reduce number of requests per second
- Check script for duplicate requests

**"Connection timeout"**
- Increase timeout values
- Retry with backoff logic
- Check network connectivity and API status

**"Malformed data"**
- Log row causing error
- Skip malformed row, continue collection
- Report count of skipped rows at end
