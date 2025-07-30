# Quick Start

Get started with Ethopy Analysis in just a few steps.

## Basic Usage

### 1. Loading from Database

```python
from ethopy_analysis.data.loaders import get_sessions
from ethopy_analysis.data.analysis import get_performance
from ethopy_analysis.plots.animal import plot_session_performance

# Load data from database
sessions = get_sessions(animal_id=123, min_trials=20)

# Create visualization
fig, ax = plot_session_performance(123, sessions['session'].values, perf_func=get_performance)
```

### 2. Command Line Interface

```bash
# Analyze specific animal
ethopy-analysis analyze-animal --animal-id 123 --save-plots

# Generate comprehensive report
ethopy-analysis generate-report --animal-id 123

# Test database connection
ethopy-analysis test-db-connection
```

## Example Notebooks

The `examples/` directory contains comprehensive Jupyter notebooks demonstrating real analysis workflows:

### Animal Analysis Example
**File**: `examples/animal_analysis_example.ipynb`

This notebook demonstrates comprehensive animal-level analysis including:

- **Session Performance Analysis**: Track performance across sessions
- **Liquid Consumption Plots**: Monitor reward consumption patterns
- **Session Date Visualization**: View session scheduling over time
- **Trials per Session**: Analyze session composition

**Key functions demonstrated**:
```python
# Load sessions with minimum trial threshold
sessions = get_sessions(animal_id, min_trials=20)

# Plot session performance over time
plot_session_performance(animal_id, sessions['session'].values, perf_func=get_performance)

# Visualize liquid consumption
plot_performance_liquid(animal_id, sessions, xaxis='session')

# Check session dates
plot_session_date(animal_id, min_trials=1)

# Analyze trials per session
plot_trial_per_session(animal_id, min_trials=30)
```

### Session Analysis Example
**File**: `examples/session_analysis_example.ipynb`

This notebook focuses on detailed session-level analysis including:

- **Trial-by-Trial Analysis**: Examine individual trial performance
- **Behavioral State Analysis**: Track animal behavior states
- **Lick Pattern Analysis**: Analyze licking behavior
- **Proximity Sensor Data**: Monitor animal position
- **Temporal Analysis**: View behavior over time

**Key functions demonstrated**:
```python
# Get latest session info
animal_id, session = get_setup("ef-rp13")

# Print comprehensive session summary
session_summary(animal_id, session)

# Difficulty analysis
difficultyPlot(animal_id, session)

# Lick behavior analysis
LickPlot(animal_id, session, state_start='Trial')
plot_licks_state(animal_id, session, bins=30)

# Proximity and timing analysis
plot_valid_proximity_state(animal_id, session, state="Trial")
plot_trial_time(animal_id, session, trials=[10, 11])
```

### Data loading Example
**File**: `examples/load_example.ipynb`

This notebook demonstrates all the data loading functions available in the ethopy_analysis package including:

- **Configuration and Setup Functions**: Load configuration and database setup
- **Database Schema Functions**: Access the DataJoint database schemas
- **Session-Level Data Loading**: Load session-level information and metadata
- **Trial-Level Data Loading**: Load detailed trial-level data for analysis
- **Behavioral Event Data Loading**: Load specific behavioral events like licks and proximity sensor data
- **Analysis and Performance Functions**: Compute performance metrics and provide session analysis
- **Complete Data Loading Example**: Load all available data for a comprehensive analysis
- **Data Format Options**: Support both DataFrame and DataJoint formats for flexibility
- **Error Handling and Edge Cases**: How functions handle common edge cases

**Key functions demonstrated**:
```python
# Load configuration from file
config = load_config(display_path=True)
print("Configuration loaded:")

# Retrieve animal_id and session for a given setup
animal_id, session = get_setup("ef-rp13") ## "ef-rp13" is the name of the setup
print(f"Setup 'ef-rp13' current animal_id: {animal_id}, session: {session}")

# Filter sessions by date range
sessions_filtered = get_sessions(animal_id, from_date="2025-01-01", to_date="2025-12-31")
print(f"Sessions for animal {animal_id} in 2025:")
print(sessions_filtered.head())

# Remove aborted trials from the dataset
trials_no_abort = get_trials(animal_id, session, remove_abort=True)
print(f"Trials without aborts: {len(trials_no_abort)} (vs {len(trials)} with aborts)")

# Retrieve all licks of a session
trial_licks = get_trial_licks(animal_id, session)
print(f"Total lick events for animal {animal_id}, session {session}:: {len(trial_licks)}")
print(f"Licks per port: {trial_licks['port'].value_counts()}")

# Print comprehensive summary of a session
print(f"Comprehensive session summary for animal {animal_id}, session {session}:")
print("=" * 60)
session_summary(animal_id, session)
```

## Running the Examples

1. **Start Jupyter**:
   ```bash
   jupyter notebook examples/
   ```

2. **Open a notebook**:
   - `animal_analysis_example.ipynb` for animal-level analysis
   - `session_analysis_example.ipynb` for session-level analysis
   - `load_example.ipynb` for data loading analysis

3. **Configure your data**:
   - Update `animal_id` variables to match your data
   - Ensure database connection is configured (see [Configuration](configuration.md))

4. **Run the cells** to see analysis results

## Configuration

Before running database-dependent examples:

1. **Set up database connection** (see [Configuration Guide](configuration.md))
2. **Test connection**:
   ```bash
   ethopy-analysis test-db-connection
   ```

## Next Steps

- **[CLI Reference](cli.md)**: Explore command-line tools
- **[API Reference](api-reference.md)**: Detailed function documentation
- **[Configuration](configuration.md)**: Database and system setup
- **[Troubleshooting](troubleshooting.md)**: Common issues and solutions

## Need Help?

- Check the [Troubleshooting Guide](troubleshooting.md)
- Review function docstrings: `help(function_name)`
- Examine the example notebooks for usage patterns