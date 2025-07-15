from collections import defaultdict

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from ethopy_analysis.data.loaders import get_sessions
from ethopy_analysis.data.analysis import get_performance, trials_per_session
from ethopy_analysis.db.schemas import get_schema


def plot_session_date(animal_id, min_trials=0):
    experiment = get_schema("experiment")
    animal_sessions_tc = get_sessions(
        animal_id, min_trials=min_trials, format="dj"
    ).proj(setup_="setup")
    tmst, session = (
        animal_sessions_tc
        * (experiment.Session & {"animal_id": animal_id} & "session>0")
    ).fetch("session_tmst", "session")
    session_same_date = defaultdict(list)
    # tmst[0].date()
    for i, _ in enumerate(tmst):
        if tmst[i].date() not in session_same_date:
            session_same_date[tmst[i].date()] = [session[i]]
        else:
            session_same_date[tmst[i].date()].append(session[i])
    dates_sess, sess_c = [], []
    for date_sess in session_same_date:
        dates_sess.append(date_sess)
        sess_c.append(len(session_same_date[date_sess]))

    plt.figure(figsize=(20, 7))
    plt.bar(dates_sess, sess_c)
    plt.xticks(dates_sess, rotation=90)
    plt.xlabel("dates")
    plt.ylabel("# sessions")
    plt.title(f"Animal id : {animal_id}")
    plt.grid()
    return session_same_date


def plot_performance_liquid(animal_id, animal_sessions, xaxis="session"):
    behavior = get_schema("behavior")
    sessions = animal_sessions["session"].values
    if len(sessions) == 0:
        print("No session available")
    perfs = [get_performance(animal_id, sess) for sess in sessions]
    liquid = []
    for sess in sessions:
        reward_animal = behavior.Rewards & {"animal_id": animal_id, "session": sess}
        reward_animal_df = reward_animal.fetch(format="frame").reset_index()
        liquid.append(
            np.sum(
                reward_animal_df.drop_duplicates(subset=["trial_idx"])["reward_amount"]
            )
        )

    assert len(liquid) == len(perfs)

    # Style of plots
    mpl.rcParams["axes.spines.right"] = True
    fig, ax1 = plt.subplots(figsize=(20, 7))

    color = "tab:red"
    ax1.set_xlabel("session id")
    ax1.set_ylabel("performace", color=color)
    ax1.plot(
        range(1, len(sessions) + 1, 1), perfs, color=color, linestyle="--", marker="o"
    )
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = "tab:blue"
    ax2.set_ylabel(
        "liquid (μL)", color=color
    )  # we already handled the x-label with ax1
    ax2.plot(
        range(1, len(sessions) + 1, 1), liquid, color=color, linestyle="--", marker="o"
    )
    ax2.tick_params(axis="y", labelcolor=color)

    if xaxis == "session":
        ax1.set_xticks(range(1, len(sessions) + 1, 1), sessions, rotation=90)
    elif xaxis == "date":
        ax1.set_xticks(
            range(1, len(sessions) + 1, 1), animal_sessions["session_tmst"], rotation=90
        )

    plt.grid()

    fig.tight_layout()  # otherwise the right y-label is slightly clipped


def find_uniq_pos(arr):
    uniq_starts = []
    uniq_value = []
    for i in range(len(arr)):
        if len(uniq_value) == 0:
            uniq_value.append(arr[i])
            uniq_starts.append(i)
        else:
            if arr[i] != arr[uniq_starts[-1]]:
                uniq_value.append(arr[i])
                uniq_starts.append(i)

    return uniq_value, uniq_starts


def plot_session_performance(animal_id, sessions, perf_func):
    experiment = get_schema("experiment")
    protocols, color_layer = [], [0]
    task_session_dj = (
        experiment.Session.Task()
        & [f"session={session}" for session in sessions]
        & f"animal_id={animal_id}"
    )
    prtcls = task_session_dj.fetch("task_name")
    prtcls = [prtcl.split("/")[-1] for prtcl in prtcls]
    sessions = task_session_dj.fetch("session")
    if len(sessions) == 0:
        print("No session available")
    perfs = [perf_func(animal_id, sess) for sess in sessions]

    protocols, color_layer = find_uniq_pos(prtcls)
    color_layer.append(sessions[-1])
    plt.figure(figsize=(20, 5))
    plt.plot(range(1, len(perfs) + 1, 1), perfs, marker=11)
    plt.xticks(range(1, len(perfs) + 1, 1), sessions, rotation=45)
    color = plt.cm.Pastel1(np.linspace(0, 1, len(color_layer)))
    for i in range(0, len(color_layer) - 1):
        plt.axvspan(
            color_layer[i] + 0.5,
            color_layer[i + 1] + 0.5,
            facecolor=color[i],
            label=protocols[i],
        )
    plt.xlim(0, len(perfs) + 1)
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    plt.title(f"Animal_id: {animal_id}")
    plt.xlabel("Session _ids")
    plt.ylabel("Performace")
    plt.grid()
    return perfs


def plot_trial_per_session(animal_id, min_trials=2):
    animal_sessions_tc = trials_per_session(animal_id, min_trials)
    animal_id = animal_sessions_tc["animal_id"].iloc[0]
    plt.figure(figsize=(15, 5))
    sess = animal_sessions_tc["session"].values
    trials_c = animal_sessions_tc["trials_count"].values
    plt.bar(list(range(len(sess))), trials_c)
    plt.xticks(list(range(len(sess))), sess)
    plt.title(f"Animal id: {animal_id}")
    plt.ylabel("# trials")
    plt.xlabel("session id")
    plt.grid()
