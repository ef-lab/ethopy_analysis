# Quick Start

Get started with Ethopy Analysis in just a few steps.

## Basic Usage

### 1. Loading from Database

```python
from ethopy_analysis.data.loaders import get_sessions
from ethopy_analysis.plots.animal import plot_session_performance

# Load data from database
sessions = get_sessions(animal_id=123, min_trials=20)

# Create visualization
fig, ax = plot_session_performance(123, sessions['session'].values)
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
plot_session_performance(animal_id, sessions['session'].values)

# Visualize liquid consumption
plot_performance_liquid(animal_id, sessions)

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

## Running the Examples

1. **Start Jupyter**:
   ```bash
   jupyter notebook examples/
   ```

2. **Open a notebook**:
   - `animal_analysis_example.ipynb` for animal-level analysis
   - `session_analysis_example.ipynb` for session-level analysis

3. **Configure your data**:
   - Update `animal_id` variables to match your data
   - Ensure database connection is configured (see [Configuration](configuration.md))

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