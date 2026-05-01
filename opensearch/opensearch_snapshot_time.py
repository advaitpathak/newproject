import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

with open("automated_snapshots.json") as f:
    data = json.load(f)

durations = []

for snap in data.get("snapshots", []):
    start = datetime.fromisoformat(snap["start_time"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(snap["end_time"].replace("Z", "+00:00"))
    duration = (end - start).total_seconds()
    durations.append(duration)

if durations:
    durations = np.array(durations)
    print(f"Count: {len(durations)} snapshots")
    print(f"Min: {durations.min():.2f} sec")
    print(f"25th percentile: {np.percentile(durations, 25):.2f} sec")
    print(f"Median (50th): {np.median(durations):.2f} sec")
    print(f"75th percentile: {np.percentile(durations, 75):.2f} sec")
    print(f"Mean: {durations.mean():.2f} sec")
    print(f"Max: {durations.max():.2f} sec")

    plt.figure(figsize=(10, 6))
    plt.hist(durations, bins=20, edgecolor='black', alpha=0.7)
    plt.title("Snapshot Duration Distribution")
    plt.xlabel("Duration (seconds)")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

    plt.figure(figsize=(6, 4))
    plt.boxplot(durations, vert=False, patch_artist=True)
    plt.title("Snapshot Duration Boxplot")
    plt.xlabel("Duration (seconds)")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()
