import networkx as nx
from typing import Dict, List, Tuple

# ----------------------------------------------------------------------
# 1. Global parameters
# ----------------------------------------------------------------------
K: int = 3  # number of homogeneous goods the seller wants to sell

valuations: Dict[str, int] = {         # private values of each bidder
    'A': 3,
    'B': 1,
    'C': 2,
    'D': 100,
    'E': 5,
    'H': 2,
    'I': 4,
}

# ----------------------------------------------------------------------
# 2. Build the directed social network  (seller node = 's')
# ----------------------------------------------------------------------
G = nx.DiGraph()

G.add_edges_from([
    ('s', 'A'), ('s', 'B'),  # seller invites A and B
    ('A', 'H'),              # invitation chain
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'), ('D', 'I')
])

# ----------------------------------------------------------------------
# 3. Helpers
# ----------------------------------------------------------------------
def invite_subtree(graph: nx.DiGraph, source: str) -> set:
    """
    Return {source} all nodes reachable from `source`
    (i.e. the set that enters the auction only if `source` invites truthfully).
    This is exactly the “domination” removal used in the diffusion‑VCG payment.
    """
    seen, stack = set(), [source]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph.successors(node))
    return seen


# ----------------------------------------------------------------------
# 4. VCG allocation & payment
# ----------------------------------------------------------------------
def vcg_allocation() -> List[str]:
    """Choose the top-K bidders by value (ties broken arbitrarily)."""
    bidders = list(valuations)
    return sorted(bidders, key=lambda x: -valuations[x])[:K]


def vcg_payment() -> Tuple[List[str], int, Dict[str, int]]:
    """
    Compute diffusion-VCG payments.

    For each bidder i:
        1) Remove i and everyone who can only be reached via i (its subtree).
        2) Re-compute the efficient SW without those nodes.
        3) Payment = Externality = SW_without_i - (SW_with_all - v_i·1{i is winner})
    """
    bidders        = list(valuations)
    winners        = vcg_allocation()
    sw_total       = sum(valuations[x] for x in winners)          # baseline SW
    payments: Dict[str, int] = {}

    for i in bidders:
        removed        = invite_subtree(G, i)
        remaining_bids = [valuations[b] for b in bidders if b not in removed]
        sw_without_i   = sum(sorted(remaining_bids, reverse=True)[:K]) if remaining_bids else 0

        # Externality formula
        payments[i] = sw_without_i - (sw_total - (valuations[i] if i in winners else 0))

    return winners, sw_total, payments


# ----------------------------------------------------------------------
# 5. Run and pretty‑print
# ----------------------------------------------------------------------
if __name__ == "__main__":
    winners, sw, pay = vcg_payment()
    revenue = sum(pay.values())

    print("=== VCG Mechanism Simulation ===")
    print(f"Social Welfare (SW): {sw}")
    print(f"Revenue  (Rev): {revenue}")
    print(f"Winners: {winners}")
    print("Payments:")
    for bidder, p in pay.items():
        print(f"  {bidder}: {p}")