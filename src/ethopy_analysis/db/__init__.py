"""
Database utilities for Ethopy analysis.

This module provides database connection and query functionality
for Ethopy behavioral experiments using DataJoint.
"""

from .queries import (
    get_setup,
    find_combination,
    get_session_classes,
    get_session_duration,
    session_summary,
    get_session_task,
    get_performance,
    get_trial_states,
    get_trials,
    get_trial_experiment,
    get_trial_behavior,
    get_trial_stimulus,
    get_trial_licks,
    get_trial_proximities,
    get_sessions,
    trials_per_session,
)

from .utils import (
    check_hashable_columns,
    combine_children_tables,
    group_trials,
    group_by_conditions,
    group_trial_hash,
    convert_ms_to_time,
)

__all__ = [
    # Main query functions
    "get_setup",
    "select_sess_dates",
    "find_combination",
    "get_session_classes",
    "get_session_duration",
    "session_summary",
    "get_session_task",
    "get_performance",
    "get_trial_states",
    "get_trials",
    "get_trial_experiment",
    "get_trial_behavior",
    "get_trial_stimulus",
    "get_trial_licks",
    "get_trial_proximities",
    "get_sessions",
    "trials_per_session",
    # Utility functions
    "check_hashable_columns",
    "combine_children_tables",
    "group_trials",
    "group_by_conditions",
    "group_trial_hash",
    "convert_ms_to_time",
]
