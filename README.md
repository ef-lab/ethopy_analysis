# Ethopy Analysis

A comprehensive Python package for analyzing and visualizing behavioral data from Ethopy experiments.

## Overview

Ethopy Analysis provides a modern, modular approach to behavioral data analysis with the following key features:

- **DataFrame-based**: All plotting functions work with pandas DataFrames, making them independent of data source
- **Modular Design**: Composable functions for different analysis levels (animal, session, comparison)
- **Database Agnostic**: Works with DataJoint databases, CSV files, or any pandas-compatible data source
- **Extensible**: Plugin system for custom plots and analysis functions
- **Production Ready**: Command-line interface, proper packaging, and configuration management

## Key Improvements

This package represents a major refactoring of the original Ethopy visualization code:

### ✅ **Decoupled from Database**
- **Before**: Plotting functions required DataJoint database connections
- **Now**: Plotting functions accept pandas DataFrames from any source

### ✅ **Modular Architecture**
- **Before**: Monolithic scripts mixing data access and plotting
- **Now**: Separate modules for data loading, plotting, and configuration

### ✅ **Easy Extension**
- **Before**: Adding new plots required modifying existing files
- **Now**: Plugin system allows easy addition of custom analysis functions

### ✅ **Professional Package**
- **Before**: Collection of scripts and notebooks
- **Now**: Pip-installable package with CLI, documentation, and examples

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone <repository-url>
cd Visualisations

# Install in development mode
pip install -e .

# Or install dependencies manually
pip install -r Session/requirements.txt
pip install click seaborn opencv-python
```

### Dependencies

- pandas >= 1.3.0
- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- numpy >= 1.20.0
- plotly >= 5.0.0
- datajoint >= 0.13.0 (for database access)
- click >= 8.0.0 (for CLI)
- opencv-python >= 4.5.0 (for video analysis)

## Quick Start

### 1. Basic Usage with Your Data

```python
import pandas as pd
from ethopy_analysis.plots.animal import plot_animal_performance

# Your data (any pandas DataFrame with the right columns)
performance_data = pd.DataFrame({
    'animal_id': [101, 101, 101],
    'session': [1, 2, 3],
    'correct_rate': [0.4, 0.6, 0.8],
    'total_trials': [50, 60, 55]
})

# Create plot with one function call
fig, ax = plot_animal_performance(performance_data, animal_id=101)
```

### 2. Loading from Ethopy Database

```python
from ethopy_analysis.data.loaders import load_animal_data

# Load data directly from database
animal_data = load_animal_data(
    animal_id=123,
    from_date="2023-01-01",
    to_date="2023-12-31"
)

# animal_data contains DataFrames: 'sessions', 'performance'
```

### 3. Command Line Interface

```bash
# Analyze a specific animal
ethopy-analysis analyze-animal --animal-id 123 --save-plots

# Compare multiple animals  
ethopy-analysis compare-animals --animal-ids "123,124,125"

# Generate comprehensive report
ethopy-analysis generate-report --animal-id 123

# Test database connection
ethopy-analysis test-db-connection
```

## Package Structure

```
ethopy-analysis/
├── src/ethopy_analysis/
│   ├── data/                   # Data loading and transformation
│   │   ├── loaders.py          # High-level data loading functions
│   │   └── transforms.py       # Data processing utilities
│   ├── plots/                  # Plotting functions (DataFrame-based)
│   │   ├── animal.py           # Animal-level plots
│   │   ├── session.py          # Session-level plots
│   │   ├── comparison.py       # Multi-animal/condition comparisons
│   │   └── utils.py            # Plotting utilities and plugin system
│   ├── db/                     # Database connectivity
│   │   ├── connection.py       # Database connection management
│   │   └── queries.py          # Database query functions
│   ├── config/                 # Configuration management
│   │   └── settings.py         # Configuration loading and validation
│   └── cli.py                  # Command-line interface
├── examples/                   # Example notebooks and scripts
│   ├── quickstart_example.ipynb
│   ├── animal_analysis_example.ipynb
│   └── session_analysis_example.ipynb
├── pyproject.toml              # Package configuration
└── README.md
```

## Core Concepts

### Data Flow

```
Database/Files → DataFrames → Plotting Functions → Visualizations
```

The package separates data loading from visualization, making it easy to:
- Use different data sources
- Cache and preprocess data
- Apply custom transformations
- Create reproducible analysis pipelines

### Analysis Levels

1. **Animal Level**: Performance across sessions
   - Learning curves
   - Session activity patterns
   - Long-term trends

2. **Session Level**: Detailed within-session analysis
   - Trial-by-trial performance
   - Behavioral patterns (licking, states)
   - Event correlations

3. **Comparison**: Cross-animal/condition analysis
   - Performance comparisons
   - Protocol effectiveness
   - Group statistics

## Examples

### Animal Performance Analysis

```python
from ethopy_analysis.plots.animal import plot_animal_performance

# Plot learning curve with trend analysis
fig, ax = plot_animal_performance(
    performance_df=data,
    animal_id=123,
    metric='correct_rate',
    rolling_window=5,
    show_trend=True
)
```

### Session Trial Analysis

```python
from ethopy_analysis.plots.session import plot_trial_performance

# Visualize trial outcomes with difficulty levels
fig, ax = plot_trial_performance(
    trials_df=session_data,
    session_id="20231101_001",
    difficulty_column='difficulty'
)
```

### Multi-Animal Comparison

```python
from ethopy_analysis.plots.comparison import plot_animals_comparison

# Compare performance across animals
fig, ax = plot_animals_comparison(
    performance_df=multi_animal_data,
    metric='correct_rate',
    comparison_type='boxplot'
)
```

### Custom Analysis Extension

```python
def my_custom_analysis(df, **kwargs):
    # Your custom analysis logic
    fig, ax = plt.subplots()
    # ... plotting code ...
    return fig, ax

# Your function is now available to others!
```

## Configuration

### Database Setup

Create a configuration file for database access:

```bash
ethopy-analysis create-config --output-path config.json
```

Edit the configuration file:

```json
{
  "database": {
    "host": "your-database.org:3306",
    "user": "your_username",
    "password": "your_password",
    "schemas": {
      "experiment": "lab_experiments",
      "behavior": "lab_behavior"
    }
  }
}
```

### Environment Variables

Alternatively, use environment variables:

```bash
export DJ_HOST="database.example.org:3306"
export DJ_USER="your_username"
export DJ_PASSWORD="your_password"
```

## Working with Your Data

The package is designed to work with any data format. You just need to ensure your DataFrames have the expected column names:

### Animal Performance Data
- `animal_id`: Animal identifier
- `session`: Session number or identifier
- `correct_rate`: Success rate (0-1)
- `session_tmst`: Session timestamp (optional)

### Trial Data
- `trial_idx`: Trial number
- `outcome`: Trial outcome ('correct', 'incorrect', 'timeout')
- `difficulty`: Difficulty level (optional)
- `reaction_time`: Response time in ms (optional)

### Behavioral Events
- `timestamp`: Event timestamp
- `animal_id`, `session`, `trial_idx`: Identifiers
- Additional columns as needed (port, state, etc.)

### Data Conversion Example

```python
# Convert your data format
your_data = your_data.rename(columns={
    'mouse_id': 'animal_id',
    'day': 'session',
    'success_percentage': 'correct_rate'
})

# Now use with plotting functions
plot_animal_performance(your_data)
```

## Migration from Original Code

If you're migrating from the original Animal/Session plotting scripts:

### Before (Old Way)
```python
# Required database connection and DataJoint queries
animal_session_tmt = experiment.Session & {"animal_id": animal_id}
trials_cond = ((experiment.Trial & key) * experiment.Condition).fetch(format="frame")
# Plotting mixed with data access
plt.scatter(difficulties, trial_idxs)
```

### After (New Way)
```python
# Load data once, use anywhere
animal_data = load_animal_data(animal_id=animal_id)

# Clean, focused plotting functions
plot_animal_performance(animal_data['performance'])
plot_difficulty_analysis(animal_data['trials'])
```

## Advanced Usage

### Batch Processing

```python
# Process multiple animals
animals = [101, 102, 103, 104]
for animal_id in animals:
    data = load_animal_data(animal_id)
    plot_animal_performance(data['performance'], save_path=f'animal_{animal_id}')
```

### Custom Data Pipeline

```python
from ethopy_analysis.data.transforms import calculate_performance_metrics

# Load raw data
raw_data = load_your_custom_data()

# Apply transformations
performance_data = calculate_performance_metrics(raw_data)

# Create visualizations
plot_animal_performance(performance_data)
```

### Plugin Development

```python
# Create reusable analysis functions
def plot_learning_efficiency(performance_df, **kwargs):
    # Calculate learning rate
    # Create custom visualization
    return fig, ax

# Use directly
from my_analysis_tools import plot_learning_efficiency
fig, ax = plot_learning_efficiency(performance_df)
```

## CLI Reference

```bash
# Animal analysis
ethopy-analysis analyze-animal --animal-id 123 [options]

# Session analysis  
ethopy-analysis analyze-session --animal-id 123 --session-id "session_001" [options]

# Comparison analysis
ethopy-analysis compare-animals --animal-ids "123,124,125" [options]

# Report generation
ethopy-analysis generate-report --animal-id 123 [options]

# Utilities
ethopy-analysis list-animals
ethopy-analysis test-db-connection
ethopy-analysis config-info
```

## Examples and Tutorials

Check out the `examples/` directory for comprehensive notebooks:

- **`quickstart_example.ipynb`**: Get started in 5 minutes
- **`animal_analysis_example.ipynb`**: Comprehensive animal-level analysis
- **`session_analysis_example.ipynb`**: Detailed session-level analysis

## Contributing

### Adding New Plot Functions

1. Create your plotting function in the appropriate module
2. Follow the DataFrame-based input convention
3. Return `(fig, ax)` or `(fig, axes)` tuple
4. Import and use directly in your analysis

### Code Style

- Functions over classes where possible
- Clear, descriptive function names
- Pandas DataFrames for data exchange
- Matplotlib for plotting (with optional Plotly support)

### Testing

```bash
# Run tests (when available)
pytest tests/

# Check code style
black src/
isort src/
```

## License

[Add your license information here]

## Support

- **Documentation**: See example notebooks and function docstrings
- **Issues**: [Create an issue](your-repo-url/issues) for bugs or feature requests
- **Discussions**: [Start a discussion](your-repo-url/discussions) for questions

## Changelog

### v0.1.0 (Current)
- Complete refactoring of original Ethopy visualization code
- DataFrame-based plotting functions
- Modular package structure
- Command-line interface
- Plugin system for extensibility
- Comprehensive examples and documentation

---

*This package builds upon the original Ethopy visualization scripts, providing a modern, extensible framework for behavioral data analysis.*