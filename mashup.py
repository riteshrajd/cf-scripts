import requests
import random
import webbrowser
import sys
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

HANDLE = "sergue_026"

TAG_BUCKETS = [
    ["math", "constructive algorithms", "number theory", "geometry"],
    ["dp", "greedy", "games", "two pointers"],
    ["graphs", "trees", "dfs and similar", "shortest paths"],
    ["data structures", "sortings", "binary search", "strings"]
]

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

def start_simulated_contest():
    print("\n--- Initiating 2-Hour Mashup Generator ---")
    ratings = [1200, 1300, random.choices([1400, 1500], weights=[0.8, 0.2])[0], random.choices([1500, 1600], weights=[0.8, 0.2])[0]]
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

    random.shuffle(TAG_BUCKETS)
    selected = []

    print(f"Target Ratings for this session: {ratings}")

    for i, rating in enumerate(ratings):
        domain_tags = TAG_BUCKETS[i]
        valid_problems = []
        weights = []
        
        for p in problems:
            cid = p.get('contestId', 0)
            min_solves = 800 if cid > 1900 else (1200 if cid > 1800 else 2000)
            p_id = f"{cid}{p.get('index')}"
            p_name = p.get('name', '')
            
            if (p.get('rating') == rating and 
                cid >= 1600 and 
                stats.get((cid, p.get('index')), 0) > min_solves and 
                p_id not in attempted_ids and 
                p_name not in attempted_names):
                
                if any(tag in p.get('tags', []) for tag in domain_tags):
                    valid_problems.append(p)
                    weights.append((cid - 1500) ** 2)
                    
        if valid_problems:
            chosen = random.choices(valid_problems, weights=weights, k=1)[0]
            selected.append(chosen)

    if len(selected) < 4:
        print("Warning: Could not find enough valid problems to fill the 4 slots. Try running again.")

    html = """
    <html><head><style>
        body { font-family: -apple-system, sans-serif; background: #1e1e1e; color: #fff; max-width: 600px; margin: 50px auto; }
        h2 { border-bottom: 2px solid #333; padding-bottom: 10px; }
        a { display: block; background: #2d2d2d; padding: 15px; margin: 10px 0; border-radius: 8px; color: #61afef; text-decoration: none; font-weight: bold; font-size: 18px; transition: 0.2s;}
        a:hover { background: #3d3d3d; }
    </style></head><body>
    <h2>Codeforces Mashup (2 Hours)</h2>
    """
    
    labels = ['A', 'B', 'C', 'D']
    for i, p in enumerate(selected):
        link = f"https://codeforces.com/contest/{p['contestId']}/problem/{p['index']}"
        html += f"<a href='{link}' target='_blank'>Problem {labels[i]}</a>"
    
    html += "</body></html>"

    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contest.html")
    try:
        with open(html_path, "w") as f:
            f.write(html)
        print(f"Mashup generated successfully. Opening {html_path}...")
        webbrowser.open(f"file://{html_path}")
    except Exception as e:
        print(f"Error saving HTML file. Check your folder path: {e}")

if __name__ == "__main__":
    start_simulated_contest()