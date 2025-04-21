import networkx as nx
from typing import Dict, List, Set

#  VCG‑RM  (VCG Revenue‑Maximizing) – Figure 4 / Table 3 reproduction
#
#  Allocation  : give the K highest bids the items (efficient)
#  Payment rule:
#       • winner i  pays   v_k( N \ T_i )
#       • loser  j  pays   v_k( N \ T_j )  –  v_k( N )
#
#    T_i  = invitation‑domination subtree of i
#    v_k(·) = k‑th largest bid in that set  (return 0 if size < k)


# ----------------------------------------------------------------------
#  1. Input data 
# ----------------------------------------------------------------------
K = 3  # number of identical goods

valuations: Dict[str, int] = {
    'A': 3,  'B': 1,  'C': 2,
    'D': 100,'E': 5,  'H': 2, 'I': 4,
}

# Build the directed social network (seller is node 's')
G = nx.DiGraph()
G.add_edges_from([
    ('s', 'A'), ('s', 'B'),
    ('A', 'H'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'), ('D', 'I'),
])
# ----------------------------------------------------------------------
# 2. Helpers
# ----------------------------------------------------------------------
def invite_subtree(graph: nx.DiGraph, root: str) -> Set[str]:
    """
    Return the set of bidders whose presence requires `root`'s invitation.
    In the Figure-4 tree this equals {root} all its descendants.
    """
    seen, stack = set(), [root]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph.successors(node))
    return seen


def kth_bid(bidders: List[str], k: int) -> int:
    """k-th highest bid among bidders (1-indexed). 0 if < k bids exist."""
    bids = sorted((valuations[b] for b in bidders), reverse=True)
    return bids[k - 1] if len(bids) >= k else 0

# ----------------------------------------------------------------------
# 3. Allocation
# ----------------------------------------------------------------------
all_bidders           = list(valuations)
winners: List[str]    = sorted(all_bidders, key=lambda x: -valuations[x])[:K]
social_welfare: int   = sum(valuations[i] for i in winners)

# ----------------------------------------------------------------------
# 4. Payments (VCG‑RM)
# ----------------------------------------------------------------------
vk_N = kth_bid(all_bidders, K)         # global k‑th bid, used for losers
payments: Dict[str, int] = {}

for bidder in all_bidders:
    T_i     = invite_subtree(G, bidder)                     # domination subtree
    vk_sub  = kth_bid([b for b in all_bidders if b not in T_i], K)

    if bidder in winners:          # winner payment
        payments[bidder] = vk_sub
    else:                          # loser “compensation”
        payments[bidder] = vk_sub - vk_N

revenue = sum(payments.values())
# ----------------------------------------------------------------------
# 5. Report 
# ----------------------------------------------------------------------
print("=== VCG-RM Mechanism Simulation ===")
print("Social Welfare (SW):", social_welfare)
print("Revenue  (Rev):", revenue)
print("Winners:", winners)
print("Payments:")
for b in sorted(payments):
    print(f"  {b}: {payments[b]}")