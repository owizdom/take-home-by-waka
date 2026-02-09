"""
Runs an algorithm at multiple values of n and produces a matplotlib graph
returned as a base-64 encoded PNG string.
"""
import base64
import io
import time

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

from algorithms import generate_data, ALGORITHMS


def run_analysis(algo_key: str, max_n: int, steps: int):
    """
    Run *algo_key* for `steps` evenly-spaced values of n up to `max_n`.

    Returns
    -------
    dict  – analysis results including base-64 graph image.
    """
    if algo_key not in ALGORITHMS:
        raise ValueError(
            f"Unknown algorithm '{algo_key}'. "
            f"Choose from: {', '.join(ALGORITHMS.keys())}"
        )

    func, complexity = ALGORITHMS[algo_key]

    sizes = np.linspace(10, max_n, steps, dtype=int).tolist()
    times_ms = []

    overall_start = time.time()

    for n in sizes:
        data = generate_data(n)
        t0 = time.perf_counter()
        func(data)
        t1 = time.perf_counter()
        times_ms.append((t1 - t0) * 1000)  # ms

    overall_end = time.time()
    total_time_ms = round((overall_end - overall_start) * 1000, 3)

    # ---- Build the graph ----
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sizes, times_ms, marker="o", linewidth=2, color="#4A90D9")
    ax.set_title(f"Performance: {algo_key}  —  {complexity}", fontsize=14)
    ax.set_xlabel("n (number of elements)")
    ax.set_ylabel("Time (ms)")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    b64_image = base64.b64encode(buf.read()).decode("utf-8")

    return {
        "algo": algo_key,
        "items": max_n,
        "steps": steps,
        "start_time": overall_start,
        "end_time": overall_end,
        "total_time_ms": total_time_ms,
        "time_complexity": complexity,
        "graph_base64": b64_image,
        "sizes": sizes,
        "times_ms": [round(t, 4) for t in times_ms],
    }
