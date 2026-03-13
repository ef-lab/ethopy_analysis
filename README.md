# Ethopy Analysis
[![PyPI Version](https://img.shields.io/pypi/v/ethopy.svg)](https://pypi.python.org/pypi/ethopy-analysis/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ethopy.svg)](https://pypi.org/project/ethopy-analysis/)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://ef-lab.github.io/ethopy_analysis/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<img src="docs/Ethopy_analysis_logo.png" alt="Ethopy Analysis" width="200"/>

A comprehensive Python package for analyzing and visualizing behavioral data from Ethopy experiments.

👉 [Documentation](https://ef-lab.github.io/ethopy_analysis/)

## Overview

Ethopy Analysis provides a modern, modular approach to behavioral data analysis with the following key features:

- **DataFrame-based**: Most of plotting functions work with pandas DataFrames, making them independent of data source
- **Modular Design**: Composable functions for different analysis levels (animal, session, comparison)
- **DataJoint-based**: Works with DataJoint databases and provides DataFrame interfaces
- **Extensible**: Modular function-based architecture for easy extension
- **Production Ready**: Command-line interface, proper packaging, and configuration management

## Installation

### From Source (Development)

Setting Up a Virtual Environment¶

Before installing dependencies, it's recommended to use a virtual environment to keep your project isolated and manageable.
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
installing dependencies:
```bash
# Clone the repository
git clone <repository-url>
cd ethopy_analysis

# Install in development mode
pip install -e .
```

### Dependencies

- pandas >= 1.3.0
- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- numpy >= 1.20.0
- plotly >= 5.0.0
- datajoint >= 0.13.0 (for database access)
- click >= 8.0.0 (for CLI)

## Package Structure

```
ethopy-analysis/
├── src/ethopy_analysis/
│   ├── data/                        # Data loading and processing
│   │   ├── loaders.py               # DB loaders: sessions, trials, states,
│   │   │                            #   licks, proximity, state windows,
│   │   │                            #   ON-OFF pairs, per-trial raster data
│   │   ├── analysis.py              # Derived metrics: performance,
│   │   │                            #   port-exit-to-lick latency, summaries
│   │   └── utils.py                 # Utilities: consecutive runs,
│   │                                #   column mapping, group helpers
│   ├── plots/                       # Plotting functions (DataFrame-based)
│   │   ├── animal.py                # Animal-level plots across sessions
│   │   ├── session.py               # Session-level plots: licks, proximity,
│   │   │                            #   states, trial-events raster
│   │   ├── comparison.py            # Multi-animal/condition comparisons
│   │   └── utils.py                 # Plotting utilities
│   ├── db/                          # Database connectivity
│   │   └── schemas.py               # DataJoint schema management and caching
│   ├── config/                      # Configuration management
│   │   ├── settings.py              # Config loading: ethopy_config.json,
│   │   │                            #   dj_conf.json, EthoPy local_conf.json,
│   │   │                            #   and environment variables
│   │   ├── styles.py                # Plot style presets
│   │   └── interactive.py           # Interactive credential prompts
│   └── cli.py                       # Command-line interface
├── examples/                        # Example notebooks
│   ├── load_example.ipynb           # Data loading walkthrough
│   ├── animal_analysis_example.ipynb # Animal-level analysis
│   └── session_analysis_example.ipynb # Session-level analysis incl.
│                                    #   proximity, state windows, raster plot
├── docs/                            # Documentation
├── pyproject.toml                   # Package configuration
└── README.md
```

## Configuration

### Already using EthoPy?

If EthoPy is installed, ethopy-analysis automatically reads `~/.ethopy/local_conf.json` —
no extra setup needed.

### Other options

| Method | How |
|--------|-----|
| Config file | Create `ethopy_config.json` in the project root (see [docs/configuration.md](docs/configuration.md)) |
| Environment variables | `export DJ_HOST=… DJ_USER=… DJ_PASSWORD=…` |
| Interactive | Run any loader — credentials are prompted if nothing else is found |

See [docs/configuration.md](docs/configuration.md) for the full priority order and format reference.

## Examples and Tutorials

Check out the `examples/` directory for comprehensive notebooks:

- **`load_example.ipynb`**: Comprehensive animal-level analysis
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
