# Developer Guide

Guide for contributing to and extending the Ethopy Analysis package.

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool

### Installation
```bash
# Clone repository
git clone <repository-url>
cd ethopy_analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev,docs,export]"
```

### Development Dependencies
The `[dev]` extra includes:
- **pytest**: Testing framework
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Style checking
- **mypy**: Type checking
- **jupyter**: Notebook support

## Code Quality

### Linting with ruff
```bash
# Check code style
ruff check src/

# Fix automatically
ruff check --fix src/

# Check specific files
ruff check src/ethopy_analysis/cli.py
```

### Additional linting with pylint
```bash
# Check code quality
pylint src/ethopy_analysis/

# Check specific module
pylint src/ethopy_analysis/data/loaders.py

# Generate report
pylint --output-format=text src/ethopy_analysis/ > pylint_report.txt
```

### Code Formatting
```bash
# Format code with black
black src/ethopy_analysis/

# Check formatting without changes
black --check src/ethopy_analysis/

# Sort imports
isort src/ethopy_analysis/
```

## Package Architecture

### Directory Structure
```
src/ethopy_analysis/
├── __init__.py              # Package initialization
├── cli.py                   # Command-line interface
├── data/                    # Data handling
│   ├── __init__.py
│   ├── loaders.py          # Data loading functions
│   ├── analysis.py         # Analysis functions
│   └── utils.py            # Data utilities
├── plots/                   # Visualization
│   ├── __init__.py
│   ├── animal.py           # Animal-level plots
│   ├── session.py          # Session-level plots
│   ├── comparison.py       # Multi-animal comparisons
│   └── utils.py            # Plotting utilities
├── db/                      # Database access
│   ├── __init__.py
│   └── schemas.py          # Database schemas
└── config/                  # Configuration
    ├── __init__.py
    ├── settings.py         # Configuration management
    └── styles.py           # Plot styling
```

### Design Principles

**1. DataFrame-First**
- All functions work with pandas DataFrames
- DataJoint-based data loading with DataFrame interfaces
- Easy testing and debugging

**2. Function-Based**
- Prefer functions over classes
- Clear, descriptive function names
- Composable and reusable

**3. Consistent Signatures**
- Common parameter patterns
- Standard return types
- Predictable behavior

## Adding New Features

### Adding Data Loading Functions
```python
# In src/ethopy_analysis/data/loaders.py
def get_new_data_type(animal_id, session, format="df"):
    """Load new data type for analysis.
    
    Parameters
    ----------
    animal_id : int
        Animal identifier
    session : int
        Session number
    format : str
        Return format ("df" or "dj")
        
    Returns
    -------
    pandas.DataFrame or datajoint.Table
        Data for analysis
    """
    # Implementation here
    pass
```

### Adding Plotting Functions
```python
# In src/ethopy_analysis/plots/animal.py or session.py
def plot_new_analysis(animal_id, session, save_path=None):
    """Create new analysis plot.
    
    Parameters
    ----------
    animal_id : int
        Animal identifier
    session : int
        Session number
    save_path : str, optional
        Path to save plot
        
    Returns
    -------
    matplotlib.figure.Figure
        Plot figure
    matplotlib.axes.Axes
        Plot axes
    """
    import matplotlib.pyplot as plt
    
    # Create plot
    fig, ax = plt.subplots()
    
    # Add plot logic here
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, ax
```

### Adding CLI Commands
```python
# In src/ethopy_analysis/cli.py
@main.command()
@click.option('--animal-id', type=int, required=True, help='Animal ID')
@click.option('--output-dir', default='./output', help='Output directory')
def new_command(animal_id, output_dir):
    """New CLI command description."""
    try:
        # Implementation here
        click.echo(f"Processing animal {animal_id}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
```

## Code Style Guidelines

### Function Documentation
```python
def example_function(param1, param2, optional_param=None):
    """Brief description of function.
    
    Longer description if needed. Explain what the function does,
    its purpose, and any important details.
    
    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
    optional_param : type, optional
        Description of optional parameter
        
    Returns
    -------
    type
        Description of return value
        
    Examples
    --------
    >>> result = example_function(1, 2)
    >>> print(result)
    3
    """
    # Implementation
    pass
```

### Error Handling
```python
def robust_function(animal_id, session):
    """Function with proper error handling."""
    if not isinstance(animal_id, int):
        raise ValueError("animal_id must be an integer")
    
    if animal_id < 0:
        raise ValueError("animal_id must be positive")
    
    try:
        # Main logic
        result = process_data(animal_id, session)
        return result
    except ConnectionError:
        raise ConnectionError("Database connection failed")
    except Exception as e:
        raise RuntimeError(f"Processing failed: {str(e)}")
```

### Type Hints
```python
from typing import Optional, List, Dict, Tuple
import pandas as pd

def typed_function(
    animal_id: int,
    sessions: List[int],
    config: Optional[Dict] = None
) -> Tuple[pd.DataFrame, Dict]:
    """Function with type hints."""
    # Implementation
    pass
```

## Configuration Management

### Adding Configuration Options
```python
# In src/ethopy_analysis/config/settings.py
DEFAULT_CONFIG = {
    "database": {
        "host": "",
        "user": "",
        "password": "",
        "schemas": {
            "experiment": "lab_experiments",
            "stimulus": "lab_stimuli",
            "behavior": "lab_behavior"
        }
    },
    "analysis": {
        "min_trials_per_session": 2,
        "performance_threshold": 0.8,
        "new_option": "default_value"  # Add new option
    }
}
```

## Documentation

### Building Documentation
```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

### Adding Documentation
- Update relevant `.md` files in `docs/`
- Add examples to docstrings
- Update API reference for new functions
- Test documentation builds locally

## CI/CD and Automation

### GitHub Actions Workflows

We use GitHub Actions for automated testing, building, and deployment.

#### Release Workflow (`.github/workflows/release.yml`)
**Triggers**: Push tags matching `v*.*.*`
**Actions**:
- Builds package with setuptools_scm
- Uploads to PyPI with API token
- Creates GitHub release with changelog
- Tests installation

**Setup**: Add `PYPI_API_TOKEN` to repository secrets

#### Documentation Workflow (`.github/workflows/docs.yml`)
**Triggers**: Push to main branch
**Actions**:
- Builds MkDocs documentation
- Deploys to GitHub Pages

**Setup**: Enable GitHub Pages with "GitHub Actions" source

### Release Process

1. **Update CHANGELOG.md** with new version section
2. **Commit changes**: `git commit -m "docs: update changelog for v1.0.0"`
3. **Create tag**: `git tag v1.0.0 && git push origin v1.0.0`
4. **Monitor workflows**: Check GitHub Actions for success

### Version Management

Uses **setuptools_scm** for automatic versioning:
- Version from Git tags (e.g., `v1.0.0` → `1.0.0`)
- Development versions include commit hash
- No manual version updates needed

### Troubleshooting

**Common Issues**:
- **403 GitHub release error**: Add `permissions: contents: write` to workflow
- **PyPI upload fails**: Check API token in repository secrets
- **Version conflicts**: Ensure tag doesn't already exist

**Recovery**:
```bash
# Delete problematic tag and retry
git tag -d v1.0.0
git push origin --delete v1.0.0
git tag v1.0.0 && git push origin v1.0.0
```

## Common Development Tasks

### Adding a New Analysis Function
1. Add function to appropriate module
2. Write comprehensive docstring
3. Add unit tests
4. Update API documentation
5. Add example usage

### Debugging Database Issues
```python
# Test database connection
from ethopy_analysis.db.schemas import test_connection
print(test_connection())

# Check configuration
from ethopy_analysis.config.settings import get_database_config
print(get_database_config())
```

### Performance Optimization
```python
# Profile code
import cProfile
cProfile.run('your_function()', 'profile_output.prof')

# Time specific operations
import time
start = time.time()
result = your_function()
print(f"Execution time: {time.time() - start:.2f}s")
```

## Contributing Guidelines

### Code Review Process
1. Create feature branch
2. Implement changes with tests
3. Ensure code quality (ruff, pylint)
4. Update documentation
5. Submit pull request

### Commit Messages
```
feat: add new analysis function for behavioral states
fix: resolve database connection timeout issue
docs: update API reference for new functions
test: add unit tests for data loaders
```

### Pull Request Template
- Description of changes
- Testing performed
- Documentation updates
- Breaking changes (if any)

## Best Practices

### Performance
- Use pandas vectorized operations
- Minimize database queries
- Cache expensive computations
- Profile before optimizing

### Maintainability
- Write clear, self-documenting code
- Use consistent naming conventions
- Keep functions focused and small
- Add comprehensive tests

### User Experience
- Provide helpful error messages
- Include usage examples
- Maintain backward compatibility
- Document breaking changes