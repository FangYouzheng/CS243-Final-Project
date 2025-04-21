import networkx as nx
from typing import Dict, List

# 1. Global parameters
K = 3
vals: Dict[str, int] = {
    'A': 3, 'B': 1, 'C': 2,
    'D': 100, 'E': 5,
    'H': 2,  'I': 4,
}

G = nx.DiGraph()
G.add_edges_from([
    ('s','A'), ('s','B'),
    ('A','H'),
    ('B','C'),
    ('C','D'),
    ('D','E'), ('D','I')
])

depth = dict(nx.single_source_shortest_path_length(G,'s'))

# 2. build blocks
blocks = {}                                   # root -> list of members
for root in G.successors('s'):                # only depth‑1 neighbours
    members = [root]                          # include the root itself
    # include its direct children (depth 2), exclude deeper descendants
    members += [c for c in G.successors(root) if depth[c] == 2]
    blocks[root] = members

# 3. allocation
left = K
winners: List[str] = []

while left > 0:
    # pick highest current top bid among all non‑empty blocks
    best_bid = -1
    best_block = None
    best_node = None
    for root, members in blocks.items():
        if not members:                        # block empty
            continue
        # local highest bid in this block
        node = max(members, key=lambda x: vals[x])
        if vals[node] > best_bid:
            best_bid, best_block, best_node = vals[node], root, node

    if best_block is None:
        break  # no candidates left

    # allocate item
    winners.append(best_node)
    left -= 1

    # update block after allocation
    if best_node == best_block:               # root wins → block closed
        blocks[best_block] = []
    else:                                     # depth‑2 node wins → remove node
        blocks[best_block].remove(best_node)

# 4. payments 
payments = {b: 0 for b in vals}
for w in winners:
    if depth[w] == 2:
        payments[w] = vals[w]                # critical price = own bid

# 5. output
SW       = sum(vals[w] for w in winners)
revenue  = sum(payments.values())

print("=== MUDAN Mechanism Simulation ===")
print("Social Welfare (SW):", SW)
print("Revenue  (Rev):", revenue)
print("Winners :", winners)
print("Payments:")
for b in sorted(payments):
    print(f"  {b}: {payments[b]}")
