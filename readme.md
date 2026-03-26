# Codeforces Automation Scripts

This folder contains the Python scripts used to automate my Codeforces practice sessions. The goal of these scripts is to remove choice paralysis, enforce topic diversity, and prioritize the modern competitive programming meta.

## The Scripts

### 1. `opener.py` (The Solo Grind)
Fetches a single, high-quality, pure-unsolved problem for a specific rating. 
* **Usage:** `python3 opener.py [rating]` (e.g., `python3 opener.py 1500`)
* **Logic:** * Randomly selects one of four primary domains (Math, DP/Greedy, Graphs, Data Structures) to prevent topic-rust.
  * Filters out ancient problems (Contest ID < 1600).
  * Uses a quadratic probability weight to heavily prioritize newer contests.
  * Adjusts the minimum solve-count requirement dynamically (newer problems need fewer solves to qualify).

### 2. `mashup.py` (The 3-Problem Simulation)
Generates a local HTML dashboard (`contest.html`) containing 3 problems to simulate an intense, focused practice session.
* **Usage:** `python3 mashup.py`
* **Structure:**
  * Problem A: 1100 or 1200
  * Problem B: 1200 or 1300
  * Problem C: 1400 or 1500
* **Logic:** Randomly selects 3 of the 4 major tag domains with zero overlap. The generated HTML dashboard displays the Problem Name and ID (e.g., *Sorting Arrays (1500A)*) but hides the rating to prevent psychological bias during the simulation. 
* **File Output:** Dynamically saves `contest.html` to the exact directory the script is run from.

## Setup & Dependencies

1. Requires `requests` (`pip3 install requests`).
2. Inside both scripts, the `HANDLE` variable **must** be updated to your active Codeforces username so it can properly generate your blacklist.

## macOS Integration (Apple Shortcuts)

macOS global hotkeys and Automator are notoriously buggy for background scripts. The most reliable way to run these is via the native **Apple Shortcuts** app.

**Setup:**
1. Open the **Shortcuts** app and create a new Shortcut.
2. Add the **Run Shell Script** action.
3. Command: `/usr/bin/python3 /absolute/path/to/your/script.py`
4. **Execution Methods (Zero-Hotkey Friction):**
   * **Spotlight:** Press `Cmd + Space`, type the Shortcut name (e.g., "CF Mashup"), and hit `Enter`.
   * **Menu Bar:** Click the "i" in the Shortcuts app and check "Pin in Menu Bar".
   * **Dock:** Right-click the Shortcut -> "Add to Dock".

*Note: Timers are handled separately via macOS Spotlight (`Cmd + Space` -> "timer 20 min") to allow flexible scaling per problem difficulty.*

## Problem Selection System

### 1. The Universal Rules (Applies to both scripts)
Every single problem must pass this gauntlet before it is even considered:
* **The "Scorched-Earth" Blacklist:** The script downloads your entire submission history. If you have **ever** submitted code for a problem (even a Wrong Answer or TLE), it is blacklisted. It aggressively filters by **both** Problem ID and Problem Name to prevent Div 1 / Div 2 duplicate overlaps.
* **The Modern Meta Filter:** Hard cutoff at Contest ID `1600`. No ancient, poorly-translated problems.
* **Dynamic Quality Control (Solve Counts):** * If it's a very new contest (>1900), it only needs **800** solves to prove it's a standard, good problem.
    * If it's somewhat new (>1800), it needs **1200** solves.
    * If it's older (<1800), it needs **2000** solves to ensure it's a high-quality classic.
* **The Recency Multiplier:** It does *not* pick randomly from the valid pool. It uses a quadratic weight `(Contest ID - 1500)^2`. This means a problem from Contest 2000 is mathematically **~6 times more likely** to be selected than a problem from Contest 1600.

### 2. The Solo Opener (`opener.py`) Logic
When you request a specific rating (e.g., 1500):
1. It looks at the four main buckets: **Math/Constructive**, **DP/Greedy**, **Graphs/Trees**, and **Data Structures**.
2. It randomly selects **one** of those buckets.
3. It filters the 1500-rated problems to match that bucket, applies the Universal Rules, rolls the weighted dice, and opens the tab.

### 3. The Mashup (`mashup.py`) Logic
When you trigger a simulation:
1. **The Difficulty Curve:** It rolls a probability check for all 3 slots to keep the difficulty unpredictable within a defined range.
2. **The Spread:** It takes the four main buckets, shuffles them, and deals exactly **one bucket to each problem slot**. 
    * *Result:* You will **never** get a contest with two Greedy problems. You are guaranteed 3 distinct concepts every single time, forcing you to practice a balanced skillset.
