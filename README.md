# Ethopy Analysis

A comprehensive Python package for analyzing and visualizing behavioral data from Ethopy experiments.

## Overview

Ethopy Analysis provides a modern, modular approach to behavioral data analysis with the following key features:

- **DataFrame-based**: Most of plotting functions work with pandas DataFrames, making them independent of data source
- **Modular Design**: Composable functions for different analysis levels (animal, session, comparison)
- **Database Agnostic**: Works with DataJoint databases, CSV files, or any pandas-compatible data source
- **Extensible**: Plugin system for custom plots and analysis functions
- **Production Ready**: Command-line interface, proper packaging, and configuration management

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
from ethopy_analysis.data.loaders import get_sessions, get_trial_states
from ethopy_analysis.data.analysis import get_performance

# Load data directly from database
sessions_df = get_sessions(animal_id=123, from_date="2023-01-01", to_date="2023-12-31")
trial_states_df = get_trial_states(animal_id=123, session=1)
performance = get_performance(animal_id=123, session=1)

# Or use convenience imports
from ethopy_analysis import get_sessions, get_trial_states, get_performance
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
│   ├── data/                   # Data loading and processing
│   │   ├── loaders.py          # Main data loading functions
│   │   ├── analysis.py         # Data analysis functions
│   │   └── utils.py            # Data processing utilities
│   ├── plots/                  # Plotting functions (DataFrame-based)
│   │   ├── animal.py           # Animal-level plots
│   │   ├── session.py          # Session-level plots
│   │   ├── comparison.py       # Multi-animal/condition comparisons
│   │   └── utils.py            # Plotting utilities and plugin system
│   ├── db/                     # Database connectivity
│   │   ├── schemas.py          # Database schema management
│   │   ├── queries.py          # Complex database operations
│   │   └── utils.py            # Database utility functions
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
      "stimulus": "lab_stimuli",
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

## Examples and Tutorials

Check out the `examples/` directory for comprehensive notebooks:

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
