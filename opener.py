import requests
import random
import webbrowser
import sys
import warnings
import os
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

load_dotenv()
HANDLE = os.getenv("CF_HANDLE")

TAG_BUCKETS = {
    "Math/Constructive": ["math", "constructive algorithms", "number theory", "geometry"],
    "DP/Greedy": ["dp", "greedy", "games", "two pointers"],
    "Graphs/Trees": ["graphs", "trees", "dfs and similar", "shortest paths"],
    "Data Structures/Sorting": ["data structures", "sortings", "binary search", "strings"]
}

def get_attempted(handle):
    try:
        url = f"https://codeforces.com/api/user.status?handle={handle}"
        print(f"Fetching user history for {handle}...")
        data = requests.get(url).json()
        
        status = data.get('status', 'UNKNOWN')
        print(f"API Status: {status}")
        
        if status != 'OK': 
            print("Failed to fetch user status. Aborting to prevent duplicate problems.")
            sys.exit(1)
        
        attempted_ids = set()
        attempted_names = set()
        
        for s in data['result']:
            if 'problem' in s:
                if 'contestId' in s['problem'] and 'index' in s['problem']:
                    attempted_ids.add(f"{s['problem']['contestId']}{s['problem']['index']}")
                if 'name' in s['problem']:
                    attempted_names.add(s['problem']['name'])
                    
        print(f"Blacklisted: {len(attempted_ids)} unique Problem IDs and {len(attempted_names)} unique Problem Names.")
        return attempted_ids, attempted_names
    except Exception as e:
        print(f"Network/API Error: {e}")
        sys.exit(1)

def open_problem(target_rating):
    print(f"\n--- Initiating Solo Fetch for Rating: {target_rating} ---")
    attempted_ids, attempted_names = get_attempted(HANDLE)
    
    try:
        print("Fetching global problemset...")
        data = requests.get("https://codeforces.com/api/problemset.problems").json()
        if data.get('status') != 'OK':
            print(f"Global Problemset API Status: {data.get('status')}")
            sys.exit(1)
            
        problems = data['result']['problems']
        stats = { (p['contestId'], p['index']): p['solvedCount'] for p in data['result']['problemStatistics'] }
    except Exception as e:
        print(f"Error fetching global problems: {e}")
        sys.exit(1)

    domain_name, domain_tags = random.choice(list(TAG_BUCKETS.items()))
    print(f"Domain Selected: {domain_name}")
    
    valid_problems = []
    weights = []
    
    for p in problems:
        cid = p.get('contestId', 0)
        min_solves = 800 if cid > 1900 else (1200 if cid > 1800 else 2000)
        p_id = f"{cid}{p.get('index')}"
        p_name = p.get('name', '')
        
        if (p.get('rating') == target_rating and 
            cid >= 1600 and 
            stats.get((cid, p.get('index')), 0) > min_solves and 
            p_id not in attempted_ids and 
            p_name not in attempted_names):
            
            if any(tag in p.get('tags', []) for tag in domain_tags):
                valid_problems.append(p)
                weights.append((cid - 1500) ** 2)

    if not valid_problems:
        print(f"No valid problems found for {target_rating} in {domain_name}. Run again.")
        return

    chosen = random.choices(valid_problems, weights=weights, k=1)[0]
    url = f"https://codeforces.com/contest/{chosen['contestId']}/problem/{chosen['index']}"
    print(f"Opening Problem: {chosen.get('name')} ({url})")
    webbrowser.open(url)

if __name__ == "__main__":
    rating = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    open_problem(rating)