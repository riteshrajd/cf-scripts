# Codeforces Automation Scripts

This folder contains the Python scripts used to automate my Codeforces practice sessions. The goal of these scripts is to remove choice paralysis, enforce topic diversity, and prioritize the modern competitive programming meta.

## The Scripts

### 1. `opener.py` (The Solo Grind)
Fetches a single, high-quality, unsolved problem for a specific rating. 
* **Usage:** `python3 opener.py [rating]` (e.g., `python3 opener.py 1500`)
* **Logic:** * Randomly selects one of four primary domains (Math, DP/Greedy, Graphs, Data Structures) to prevent topic-rust.
  * Filters out ancient problems (Contest ID > 1600).
  * Uses a quadratic probability weight to prioritize newer contests.
  * Adjusts the minimum solve-count requirement dynamically (newer problems need fewer solves to qualify).

### 2. `mashup.py` (The 2-Hour Simulation)
Generates a local HTML dashboard (`contest.html`) containing 4 blind problems to simulate a standard Div. 2/3 contest.
* **Usage:** `python3 mashup.py`
* **Structure:**
  * Problem A: 1200
  * Problem B: 1300
  * Problem C: 1400 (80%) / 1500 (20%)
  * Problem D: 1500 (80%) / 1600 (20%)
* **Logic:** Guarantees that the 4 problems cover all 4 major tag domains with zero overlap. Ratings are hidden on the generated HTML page to prevent rating bias during the simulation.

## Setup & Dependencies

1. Requires `requests` (`pip3 install requests`).
2. Inside both scripts, the `HANDLE` variable must be updated to the active Codeforces username so it can filter out already solved problems.

## macOS Automator Integration

These scripts are designed to be run entirely via global macOS hotkeys using **Automator Quick Actions**. 

**Automator Setup:**
1. Create a Quick Action -> Workflow receives `no input` in `any application`.
2. Add `Run Shell Script` (Shell: `/bin/zsh`).
3. Command: `/usr/bin/python3 /path/to/script.py [args]`
4. Bind in System Settings -> Keyboard -> Keyboard Shortcuts -> Services.

*Note: Timers are handled separately via macOS Spotlight (`Cmd + Space` -> "timer 120 min") to allow flexible time adjustments.*

## Problme Selection System

### 1. The Universal Rules (Applies to both scripts)
Every single problem must pass this gauntlet before it is even considered:
* **The "Freshness" Check:** It hits the Codeforces API. If you have an `OK` verdict on it, it is instantly thrown out.
* **The Modern Meta Filter:** Hard cutoff at Contest ID `1600`. No ancient, poorly-translated problems from 10 years ago.
* **Dynamic Quality Control (Solve Counts):** * If it's a very new contest (>1900), it only needs **800** solves to prove it's a standard, good problem.
    * If it's somewhat new (>1800), it needs **1200** solves.
    * If it's older (<1800), it needs **2000** solves to ensure it's a high-quality classic.
* **The Recency Multiplier:** It does *not* pick randomly from the valid pool. It uses a quadratic weight `(Contest ID - 1500)^2`. This means a problem from Contest 2000 is mathematically **~6 times more likely** to be selected than a problem from Contest 1600.

### 2. The Solo Opener (`opener.py`) Logic
When you press the hotkey for a specific rating (e.g., 1500):
1. It looks at the four main buckets: **Math/Constructive**, **DP/Greedy**, **Graphs/Trees**, and **Data Structures**.
2. It randomly selects **one** of those buckets.
3. It filters the 1500-rated problems to match that bucket, applies the Universal Rules, rolls the weighted dice, and opens the tab.

### 3. The Mashup (`mashup.py`) Logic
When you trigger a 2-hour simulation:
1. **The Difficulty Curve:** It hardcodes Problem A (1200) and B (1300). It rolls a probability check for C (80% chance of 1400, 20% chance of 1500) and D (80% chance of 1500, 20% chance of 1600).
2. **The Perfect Spread:** It takes the four main buckets, shuffles them, and deals exactly **one bucket to each problem**. 
    * *Result:* You will **never** get a contest with three Greedy problems. You are guaranteed exactly 1 Math, 1 DP, 1 Graph, and 1 DS problem every single time, forcing you to practice a balanced skillset.
    