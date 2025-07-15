"""
Ethopy Analysis: Data analysis and visualization package for Ethopy behavioral experiments.

This package provides tools for:
- Loading and processing behavioral data from Ethopy experiments
- Creating visualizations for animal and session-level analysis
- Exporting data to various formats
- Database connectivity with DataJoint

Key modules:
- data: Data loading and transformation functions
- plots: Plotting functions that work with pandas DataFrames
- db: Database connection and query utilities
- config: Configuration management
"""

__version__ = "0.1.0"
__author__ = "Ethopy Analysis Contributors"


from ethopy_analysis.db.schemas import (
    get_schema,
    get_all_schemas,
    test_connection,
)

from ethopy_analysis.config.settings import (
    load_config,
    get_config_summary,
)

# Also import modules for advanced users
from ethopy_analysis.data import loaders
from ethopy_analysis.plots import animal
from ethopy_analysis.db import schemas
from temp_old_files import session_olf

__all__ = [
    # High-level data loading functions
    "load_session_data",
    "load_animal_data",
    "load_complete_session_data",
    # Database schema access
    "get_experiment_tables",
    "get_behavior_tables",
    "get_stimulus_tables",
    "get_schema",
    "get_all_schemas",
    # Utility functions
    "test_connection",
    "clear_database_cache",
    "load_config",
    "get_config_summary",
    # Modules for advanced users
    "loaders",
    "animal",
    "session_olf",
    "schemas",
]
