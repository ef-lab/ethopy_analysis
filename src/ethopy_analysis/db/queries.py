from typing import List, Optional, Union, Tuple, Any
import numpy as np
from ethopy_analysis.db.schemas import get_schema
import os
import pandas as pd
from .utils import (
    combine_children_tables,
    convert_ms_to_time,
)


def get_sessions(
    animal_id,
    from_date: str = "",
    to_date: str = "",
    format: str = "df",
    min_trials: Optional[int] = None,
):
    """
    Get sessions for an animal within a specified date range.

    Args:
        animal_id (int): The animal identifier
        from_date (str, optional): Start date in format 'YYYY-MM-DD'. Defaults to ''.
        to_date (str, optional): End date in format 'YYYY-MM-DD'. Defaults to ''.
        format(str, optional): if format equals 'dj' return datajoint expression.
        min_trials(int, optional): minimum number of trials per session.

    Returns:
        Union[pd.DataFrame, Any]: Session DataFrame if format="df",
                                 Session expression if format="dj"
    """
    experiment = get_schema("experiment")

    animal_session_tmt = experiment.Session & {"animal_id": animal_id}
    if from_date != "":
        animal_session_tmt = animal_session_tmt & f'session_tmst > "{from_date}"'

    if to_date != "":
        animal_session_tmt = animal_session_tmt & f'session_tmst < "{to_date}"'

    sessions_dj = animal_session_tmt - experiment.Session.Excluded
    if min_trials:
        trials_session = trials_per_session(animal_id, min_trials=2, format="dj")
        sessions_dj = trials_session * sessions_dj

    if format == "dj":
        return sessions_dj
    return sessions_dj.fetch(format="frame").reset_index()


def trials_per_session(animal_id: int, min_trials=2, format="df"):
    """Returns the number of trials per session

    Args:
        animal_id (int)
        experiment (datajoint.schemas.VirtualModule)

    Returns:
        datajoint.expression.Aggregation: a dj table with the number of trial
        per session as trials_count
    """
    experiment = get_schema("experiment")

    session_trials_dj = (experiment.Session & {"animal_id": animal_id}).aggr(
        experiment.Trial & {"animal_id": animal_id}, trials_count="count(trial_idx)"
    ) - experiment.Session.Excluded & f"trials_count>{min_trials}"
    if format == "dj":
        return session_trials_dj
    return session_trials_dj.fetch(format="frame").reset_index()


def get_setup(setup: str) -> Tuple[int, int]:
    """
    Retrieve animal_id and session for a given setup.

    Args:
        setup (str): The setup identifier

    Returns:
        Tuple[int, int]: A tuple containing (animal_id, session)

    Raises:
        IndexError: If no setup found with the given identifier
    """
    experiment = get_schema("experiment")
    setup_data = (
        (experiment.Control & f'setup="{setup}"').fetch(format="frame").reset_index()
    )
    return int(setup_data["animal_id"].values[0]), int(setup_data["session"].values[0])


def find_combination(states_df: pd.DataFrame, state: str = "PreTrial") -> str:
    """
    Find the next state after the specified state in a trial sequence.

    Args:
        states_df (pd.DataFrame): DataFrame containing trial states with 'state' column
        state (str, optional): The state to find the next state after. Defaults to "PreTrial".

    Returns:
        str: The state that follows the specified state, or "None" if:
            - The specified state is not found in the trial
            - "Offtime" is present in the trial states
            - The specified state is the last state in the sequence

    Raises:
        IndexError: If the specified state is the last state in the sequence
    """
    trial_states = states_df["state"].values
    if state not in trial_states:
        return "None"
    if "Offtime" in trial_states:
        return "None"
    idx = np.where(trial_states == state)[0][0]
    if idx + 1 >= len(trial_states):
        return "None"
    return trial_states[idx + 1]


def get_session_classes(animal_id: int, session: int) -> pd.DataFrame:
    """
    Retrieve session information and experimental classes for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number

    Returns:
        pd.DataFrame: Combined DataFrame containing session information and unique
                     combinations of stimulus_class, behavior_class, and experiment_class

    Raises:
        Exception: If no session found for the given animal_id and session
    """
    experiment = get_schema("experiment")
    key_animal_session = {"animal_id": animal_id, "session": session}
    session_info_df = (
        (experiment.Session & key_animal_session).fetch(format="frame").reset_index()
    )

    conditions_dj = (experiment.Trial & key_animal_session) * experiment.Condition
    conditions_df = conditions_dj.fetch(format="frame").reset_index()

    # Get unique combinations
    unique_combinations = conditions_df[
        ["stimulus_class", "behavior_class", "experiment_class"]
    ].drop_duplicates()

    # Combine session_info_df and unique_combinations side by side
    combined_df = pd.concat(
        [session_info_df, unique_combinations.reset_index(drop=True)], axis=1
    )
    return combined_df


def get_session_duration(animal_id: int, session: int) -> Optional[str]:
    """
    Calculate the duration of a session based on the last state onset time.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number

    Returns:
        Optional[str]: Formatted duration string (e.g., "1.2 hours (4320.0 seconds)")
                      or None if no state times found
    """
    experiment = get_schema("experiment")
    state_times = (
        experiment.Trial.StateOnset & {"animal_id": animal_id, "session": session}
    ).fetch("time")
    if len(state_times) < 1:
        return None
    return convert_ms_to_time(state_times[-1])["formatted"]


def session_summary(animal_id: int, session: int) -> None:
    """
    Print a comprehensive summary of a session including metadata and performance.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number

    Prints:
        - Animal ID and session number
        - User name and setup information
        - Session start time and duration
        - Experiment, stimulus, and behavior classes
        - Task filename and git hash
        - Session performance and number of trials
    """
    session_classes = get_session_classes(animal_id, session)
    print(f"Animal id: {animal_id}, session: {session}")
    print(f"User name: {session_classes['user_name'].values[0]}")
    print(f"Setup: {session_classes['setup'].values[0]}")
    print(f"Session start: {pd.to_datetime(session_classes['session_tmst'].values[0])}")
    print(f"Session duration: {get_session_duration(animal_id, session)}")

    print()
    print("Experiment: ", session_classes["experiment_class"].values[0])
    print("Stimulus: ", session_classes["stimulus_class"].values[0])
    print("Behavior: ", session_classes["behavior_class"].values[0])

    filename, git_hash = get_session_task(animal_id, session, save_file=False)
    print()
    print(f"Task filename: {filename}")
    print(f"Git hash: {git_hash}")

    df = get_trial_states(animal_id, session)
    print()
    print(f"Session performance: {get_performance(df)}")
    print(f"Number of trials: {max(df['trial_idx'])}")


def get_session_task(
    animal_id: int, session: int, save_file: bool = True
) -> Tuple[str, str]:
    """
    Retrieve and optionally save the task configuration file for a specific session.

    Args:
        animal_id (int): Animal identifier
        session (int): Session identifier
        save_file (bool, optional): Whether to save the file to disk. Defaults to True.

    Returns:
        Tuple[str, str]: A tuple containing (filename, git_hash)

    Note:
        If save_file is True, the file is saved with a modified name including
        animal_id and session for uniqueness.
    """
    key_animal_session = {"animal_id": animal_id, "session": session}
    experiment = get_schema("experiment")
    file, git_hash, task_name = (experiment.Session.Task & key_animal_session).fetch1(
        "task_file", "git_hash", "task_name"
    )
    filename = task_name.split("/")[-1]

    if save_file:
        filename = f"{filename[:-3]}_animal_id_{animal_id}_session_{session}.py"
        print(f"Save task at path: {os.getcwd()}/{filename}")
        file.tofile(filename)
    return filename, git_hash


def get_performance(
    animal_id, session, trials: Optional[List[int]] = None
) -> Optional[float]:
    """
    Calculate performance as the ratio of reward trials to total decisive trials.

    Args:
        animal_id (int): Animal identifier
        session (int): Session identifier
        trials (Optional[List[int]], optional): List of trial indices to filter by.
                                              Defaults to None.

    Returns:
        Optional[float]: Performance ratio (0-1), or None if no decisive trials found

    Note:
        Decisive trials are those with state 'Reward' or 'Punish'.
        Performance is calculated as: count_reward_trials / (count_reward_trials + count_punish_trials)
    """
    df = get_trial_states(animal_id, session)
    if df is None or df.empty:
        print("Warning: DataFrame is empty or None - cannot calculate performance")
        return None

    # Filter by trials if provided
    if trials is not None:
        df = df[df["trial_idx"].isin(trials)]
        if df.empty:
            print(
                "Warning: No trials found matching the provided trial list - cannot calculate performance"
            )
            return None

    # Filter to only decisive trials (Reward or Punish) - vectorized operation
    decisive_trials = df[df["state"].isin(["Reward", "Punish"])]

    if decisive_trials.empty:
        available_states = df["state"].unique()
        print(
            f"Warning: No Reward or Punish states found. Available states: {available_states}"
        )
        return None

    # Count using vectorized operations for speed
    state_counts = decisive_trials["state"].value_counts()
    count_reward_trials = state_counts.get("Reward", 0)
    count_punish_trials = state_counts.get("Punish", 0)

    # Handle division by zero edge case
    total_decisive = count_reward_trials + count_punish_trials
    if total_decisive == 0:
        print("Warning: Total decisive trials is zero - cannot calculate performance")
        return None

    return count_reward_trials / total_decisive


def get_trial_states(
    animal_id: int, session: int, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial state onset data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial states DataFrame if format="df",
                                 DataJoint expression if format="dj"
    """
    experiment = get_schema("experiment")
    key_animal_session = {"animal_id": animal_id, "session": session}

    trial_states_dj = experiment.Trial.StateOnset & key_animal_session

    if format == "dj":
        return trial_states_dj

    trial_states_df = trial_states_dj.fetch(format="frame").reset_index()
    return trial_states_df


def get_trials(
    animal_id: int, session: int, format: str = "df", remove_abort: bool = False
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".
        remove_abort (bool): remove abort trials

    Returns:
        Union[pd.DataFrame, Any]: Trial DataFrame if format="df",
                                 DataJoint expression if format="dj"
    """
    experiment = get_schema("experiment")
    trials_dj = experiment.Trial & {"animal_id": animal_id, "session": session}
    if remove_abort:
        trials_dj = trials_dj - experiment.Trial.Aborted()
    if format == "dj":
        return trials_dj
    return trials_dj.fetch(format="frame").reset_index()


def get_trial_experiment(
    animal_id: int, session: int, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial experiment condition data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial experiment conditions DataFrame if format="df",
                                 DataJoint expression if format="dj"

    Note:
        This function combines trial data with experiment conditions based on the
        experiment_type from the session classes.
    """
    experiment = get_schema("experiment")
    key_animal_session = {"animal_id": animal_id, "session": session}
    combined_df = get_session_classes(animal_id, session)
    exp_conds = getattr(experiment.Condition, combined_df["experiment_type"].values[0])
    conditions_dj = (experiment.Trial & key_animal_session) * experiment.Condition
    trial_exp_conditions_dj = conditions_dj * exp_conds

    if format == "dj":
        return trial_exp_conditions_dj

    trial_exp_conditions_df = trial_exp_conditions_dj.fetch(
        format="frame"
    ).reset_index()
    return trial_exp_conditions_df


def get_trial_behavior(
    animal_id: int, session: int, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial behavior condition data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial behavior conditions DataFrame if format="df",
                                 DataJoint expression if format="dj"

    Note:
        This function combines trial data with behavior conditions, handling cases
        where multiple behavior child tables need to be combined.
    """
    behavior = get_schema("behavior")
    key_animal_session = {"animal_id": animal_id, "session": session}
    combined_df = get_session_classes(animal_id, session)
    beh_conds = getattr(behavior, combined_df["behavior_class"].values[0])
    children = beh_conds.children(as_objects=True)

    if len(children) > 1:
        comb_tables = combine_children_tables(children)
    elif len(children) == 1:
        comb_tables = children[0]
    else:
        comb_tables = beh_conds

    trial_beh_conditions_dj = (
        behavior.BehCondition.Trial() & key_animal_session
    ) * comb_tables

    if format == "dj":
        return trial_beh_conditions_dj

    trial_beh_conditions_df = trial_beh_conditions_dj.fetch(
        format="frame"
    ).reset_index()
    return trial_beh_conditions_df


def get_trial_stimulus(
    animal_id: int, session: int, stim_class: Optional[str] = None, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve trial stimulus condition data for a specific animal session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        stim_class (Optional[str], optional): Specific stimulus class to use.
                                            If None, uses the stimulus class from session data.
                                            Defaults to None.
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial behavior conditions DataFrame if format="df",
                                 DataJoint expression if format="dj"
    Raises:
        Exception: If the specified stimulus class table is not found in the stimulus schema

    Note:
        This function combines trial data with stimulus conditions and all related
        child tables that contain data for the session.
    """
    stimulus = get_schema("stimulus")
    combined_df = get_session_classes(animal_id, session)
    key_animal_session = {"animal_id": animal_id, "session": session}

    if stim_class is None:
        stim_class_name = combined_df["stimulus_class"].values[0]
        try:
            stim_conds = getattr(stimulus, stim_class_name)
        except AttributeError as e:
            raise Exception(
                f"Cannot find {stim_class_name} table in stimulus schema"
            ) from e
    else:
        try:
            stim_conds = getattr(stimulus, stim_class)
        except AttributeError as e:
            raise Exception(f"Cannot find {stim_class} table in stimulus schema") from e

    children = stim_conds.children(as_objects=True)
    base_dj = (stimulus.StimCondition.Trial & key_animal_session) * stim_conds
    all_stims = base_dj

    for child in children:
        comb_stims = base_dj * child
        if len(comb_stims) > 0:
            all_stims = all_stims * child

    trial_stim_conditions_dj = all_stims
    if format == "dj":
        return trial_stim_conditions_dj
    trial_stim_conditions_df = trial_stim_conditions_dj.fetch(
        format="frame"
    ).reset_index()
    return trial_stim_conditions_df


def get_trial_proximities(animal_id, session, ports: Optional[List] = None, format="df"):
    behavior = get_schema("behavior")
    if ports:
        proximity_dj = (
            behavior.Activity.Proximity
            & {"animal_id": animal_id, "session": session}
            & [f"port={p}" for p in ports]
        )
    else:
        proximity_dj = behavior.Activity.Proximity & {
            "animal_id": animal_id,
            "session": session,
        }
    if format == "dj":
        return proximity_dj
    return proximity_dj.fetch(format="frame").reset_index()


def get_trial_licks(
    animal_id: int, session: int, format: str = "df"
) -> Union[pd.DataFrame, Any]:
    """
    Retrieve all licks of a session.

    Args:
        animal_id (int): The animal identifier
        session (int): The session number
        stim_class (Optional[str], optional): Specific stimulus class to use.
                                            If None, uses the stimulus class from session data.
                                            Defaults to None.
        format (str, optional): Return format, either "df" for DataFrame or "dj" for DataJoint expression.
                               Defaults to "df".

    Returns:
        Union[pd.DataFrame, Any]: Trial behavior conditions DataFrame if format="df",
                                 DataJoint expression if format="dj"
    """
    behavior = get_schema("behavior")
    key = {"animal_id": animal_id, "session": session}
    lick_dj = behavior.Activity.Lick & key
    if format == "dj":
        return lick_dj
    return lick_dj.fetch(format="frame").reset_index()
