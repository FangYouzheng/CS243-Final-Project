import networkx as nx
from typing import Dict, List, Set

# ------------------ 1. parameters ------------------
K = 3  # number of identical items

vals: Dict[str, int] = {          # bidders' true valuations
    'A': 3, 'B': 1, 'C': 2,
    'D': 100, 'E': 5,
    'H': 2,  'I': 4,
}

# directed social network (seller is node 's')
G = nx.DiGraph()
G.add_edges_from([
    ('s', 'A'), ('s', 'B'),
    ('A', 'H'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'), ('D', 'I')
])

bidders = list(vals)  # convenience list

# ------------------ 2. helpers ---------------------
def bfs_order(root: str = 's') -> List[str]:
    """BFS traversal order excluding the root (seller)."""
    return [n for n in nx.bfs_tree(G, root) if n != root]

def domination_subtree(node: str) -> Set[str]:
    """Invitation-domination subtree rooted at `node`."""
    return nx.descendants(G, node) | {node}

def kth_bid(cands: List[str], k: int) -> int:
    """
    Return k-th highest bid among `cands`.
    If fewer than k candidates, return −∞ so the inequality fails.
    """
    if len(cands) < k:
        return float("-inf")
    return sorted((vals[b] for b in cands), reverse=True)[k - 1]

# ------------------ 3. allocation ------------------
def dna_mu_r_allocation() -> List[str]:
    """Implement Algorithm 2 - return winner list."""
    left = K
    winners: List[str] = []
    for i in bfs_order():                # step through BFS order
        Ti      = domination_subtree(i)  # bidders dominated by i
        others  = [b for b in bidders if b not in Ti]
        thresh  = kth_bid(others, left)  # v_k(N \ Ti)
        if vals[i] >= thresh and left > 0:
            winners.append(i)
            left -= 1
        if left == 0:
            break
    return winners

# ------------------ 4. critical bids ---------------
def wins_with_bid(bidder: str, bid: int) -> bool:
    """Check if `bidder` would still win when bidding `bid`."""
    original = vals[bidder]
    vals[bidder] = bid
    res = bidder in dna_mu_r_allocation()
    vals[bidder] = original
    return res

def critical_bid(bidder: str) -> int:
    """
    Smallest integer b ∈ [0, v_i] making bidder win.
    Range is tiny in the example, linear scan is fine.
    """
    for b in range(vals[bidder] + 1):
        if wins_with_bid(bidder, b):
            return b
    return vals[bidder]  # fallback (should not be reached)

# ------------------ 5. execute mechanism -----------
winners  = dna_mu_r_allocation()
payments = {b: (critical_bid(b) if b in winners else 0) for b in bidders}
sw       = sum(vals[w] for w in winners)
revenue  = sum(payments.values())

# ------------------ 6. output ----------------------
print("=== DNA-MU-R Mechanism Simulation ===")
print("Social Welfare (SW):", sw)
print("Revenue  (Rev):", revenue)
print("Winners :", winners)
print("Payments:")
for b in sorted(payments):
    print(f"  {b}: {payments[b]}")