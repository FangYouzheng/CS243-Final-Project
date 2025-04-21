import networkx as nx
from typing import Dict, List, Set

# ---------------- 1. data ----------------
K = 3
vals: Dict[str, int] = {
    'A': 3, 'B': 1, 'C': 2,
    'D': 100, 'E': 5,
    'H': 2,  'I': 4,
}

G = nx.DiGraph()
G.add_edges_from([
    ('s', 'A'), ('s', 'B'),
    ('A', 'H'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'), ('D', 'I')
])

# ---------------- 2. helper ----------------
depth = dict(nx.single_source_shortest_path_length(G, 's'))   # BFS depth

def local_set() -> Set[str]:
    """Nodes allowed to compete (depth ≤ 2, excluding seller)."""
    return {v for v,d in depth.items() if d <= 2 and v != 's'}

# ---------------- 3. allocation -----------
winners: List[str] = []
candidates: Set[str] = set(local_set())
left = K

while left > 0 and candidates:
    # current highest bid among remaining candidates
    pick = max(candidates, key=lambda x: vals[x])
    winners.append(pick)
    left -= 1

    if depth[pick] == 1:                   # depth‑1 winner blocks its subtree
        candidates -= set(nx.descendants(G, pick))
    # remove the picked node itself from future consideration
    candidates.remove(pick)

# ---------------- 4. payments -------------
payments = {b: 0 for b in vals}           # losers & depth‑1 winners pay 0
for w in winners:
    if depth[w] == 2:                     # depth‑2 winners pay their own bid
        payments[w] = vals[w]

# ---------------- 5. stats ----------------
SW      = sum(vals[w] for w in winners)
revenue = sum(payments.values())

print("=== LDM-Tree Mechanism Simulation ===")
print("Social Welfare (SW):", SW)
print("Revenue  (Rev):", revenue)
print("Winners :", winners)
print("Payments:")
for b in sorted(payments):
    print(f"  {b}: {payments[b]}")