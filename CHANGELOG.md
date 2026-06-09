# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.3] - 2026-06-09

### Added
- **EthoPy `local_conf.json` compatibility**: auto-detect and convert EthoPy's
  `~/.ethopy/local_conf.json` format (dot-notation `dj_local_conf` keys + `SCHEMATA`)
  to the internal config format, so existing EthoPy users need zero extra setup.
  Added as the lowest-priority config fallback in `find_config_file()`.
- **New data loaders** (`data/loaders.py`): `get_state_windows`, `get_licks_per_state`,
  `get_first_lick_after_state`, `get_first_port_exit_after_state`,
  `get_licks_during_proximity`, `get_proximity_on_off_pairs`,
  `get_trial_proximity_timings`, `get_session_proximity_data`.
- **New analysis function** (`data/analysis.py`): `get_port_exit_to_lick_latency`.
- **New utilities** (`data/utils.py`): `find_consecutive_runs`, `add_column_by_key`.
- **New plot** (`plots/session.py`): `plot_trial_events_raster` — per-trial raster of
  proximity ON-OFF pairs, licks, and states with flexible alignment and sorting.

### Changed
- Updated documentation: configuration discovery priority table, side-by-side format
  docs, quickstart simplification, project logo, and GitHub Pages documentation link.
- Updated `session_analysis_example.ipynb` with usage examples for the new functions.

### Fixed
- Pin `datajoint` to `<2.0.0` to avoid breaking API changes in the 2.x release.
- `generate-report`: fix `datetime.now` usage and handle sessions without behavior data.
- Config: fix shallow-copy bug (`DEFAULT_CONFIG.copy()` → `copy.deepcopy()`) that let
  nested-dict mutations leak into the global default; deduplicate
  `load_config`/`load_config_with_source`.

## [0.1.0] - 2024-01-XX

### Added
- Initial release of ethopy-analysis package
- **Data Loading System**: Comprehensive data loading functions for Ethopy experiments
  - `get_sessions()` - Load session data with date filtering
  - `get_trials()` - Load trial data with optional abort removal
  - `get_trial_states()` - Load trial state onset data
  - `get_trial_experiment()` - Load experiment condition data
  - `get_trial_behavior()` - Load behavior condition data
  - `get_trial_stimulus()` - Load stimulus condition data
  - `get_trial_licks()` - Load lick event data
  - `get_trial_proximities()` - Load proximity sensor data
- **Analysis Functions**: Performance and session analysis
  - `get_performance()` - Calculate performance metrics
  - `session_summary()` - Generate session summaries
  - `trials_per_session()` - Count trials per session
- **Visualization System**: DataFrame-based plotting functions
  - **Animal-level plots**: `plot_session_performance()`, `plot_performance_liquid()`, `plot_session_date()`, `plot_trial_per_session()`
  - **Session-level plots**: `difficultyPlot()`, `LickPlot()`, `plot_licks_state()`, `plot_first_lick_after()`, `plot_valid_proximity_state()`, `plot_proximities_dur()`, `plot_trial_time()`, `liquidsPlot()`, `plot_states_in_time()`, `plot_licks_time()`
  - **Comparison plots**: Multi-animal analysis functions
- **Database Integration**: DataJoint ORM support
  - Schema management with `get_schema()` and `get_all_schemas()`
  - Flexible data format support (DataFrame/DataJoint)
  - Database connection testing utilities
- **Configuration System**: Unified configuration management
  - Support for JSON config files and environment variables
  - Hierarchical configuration loading (env vars > config files > defaults)
  - Database credential management
  - Configuration validation and security checks
- **Command Line Interface**: Full-featured CLI
  - `ethopy-analysis analyze-animal` - Animal-level analysis
  - `ethopy-analysis compare-animals` - Multi-animal comparisons
  - `ethopy-analysis generate-report` - Comprehensive reporting
  - `ethopy-analysis test-db-connection` - Database connectivity testing
- **Documentation**: Comprehensive documentation system
  - MkDocs-based documentation with Material theme
  - API reference documentation
  - Example notebooks for common workflows
  - Developer guide with contribution guidelines
- **Example Notebooks**: 
  - `animal_analysis_example.ipynb` - Animal-level analysis examples
  - `session_analysis_example.ipynb` - Session-level analysis examples
  - `load_example.ipynb` - Data loading function examples
- **Package Infrastructure**:
  - Modern Python packaging with `pyproject.toml`
  - Automated version management with setuptools_scm
  - Code quality tools (ruff, black, isort, mypy)
  - GitHub Actions for automated releases
  - PyPI publishing workflow

### Technical Details
- **Python Support**: Python 3.8+
- **Key Dependencies**: pandas, matplotlib, seaborn, datajoint, click, numpy, plotly
- **Architecture**: Modular design with DataFrame-first approach
- **Database**: DataJoint ORM with MySQL/MariaDB support
- **Visualization**: Matplotlib/Seaborn-based with optional Plotly support

### Dependencies
- datajoint>=0.13.0
- matplotlib>=3.5.0
- networkx>=2.6.0
- numpy>=1.20.0
- pandas>=1.3.0
- plotly>=5.0.0
- seaborn>=0.11.0
- click>=8.0.0
- tqdm>=4.60.0
- ipykernel>=6.0.0

## Release Notes Template

For future releases, use this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features and functionality

### Changed
- Changes to existing functionality

### Deprecated
- Features that will be removed in future versions

### Removed
- Features that have been removed

### Fixed
- Bug fixes

### Security
- Security improvements and fixes
```

## Development Guidelines

### Version Numbering
- **Major** (X.0.0): Breaking changes, major new features
- **Minor** (X.Y.0): New features, backward compatible
- **Patch** (X.Y.Z): Bug fixes, backward compatible

### Changelog Maintenance
- Update CHANGELOG.md with every release
- Follow Keep a Changelog format
- Include migration notes for breaking changes
- Link to relevant issues and pull requests where applicable

### Release Process
1. Update CHANGELOG.md with new version section
2. Move items from [Unreleased] to new version section
3. Add release date
4. Create and push version tag
5. GitHub Actions will automatically create release with changelog excerpt

[Unreleased]: https://github.com/ef-lab/ethopy_analysis/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/ef-lab/ethopy_analysis/compare/v0.1.2...v0.1.3
[0.1.0]: https://github.com/ef-lab/ethopy_analysis/releases/tag/v0.1.0