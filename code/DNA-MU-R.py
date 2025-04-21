from collections import deque

def build_idt(parent):
    # 构建邀约支配树(subtree)
    children = {}
    for i, p in parent.items():
        children.setdefault(p, []).append(i)
    def dfs(u):
        s = {u}
        for v in children.get(u, []):
            s |= dfs(v)
        return s
    return {i: dfs(i) for i in parent}

def bfs_order(adj, seller='s'):
    # BFS 顺序
    q = deque([seller]); seen = {seller}; order = []
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in seen:
                seen.add(v)
                order.append(v)
                q.append(v)
    return order

def dna_mu_r_alloc(adj, parent, vals, K):
    """
    Allocation 阶段：按 BFS 顺序，用动态阈值分配，剩余 k 递减
    """
    O = bfs_order(adj, seller='s')
    subtree = build_idt(parent)
    f = {i: 0 for i in vals}
    winners = []
    remaining = K
    for i in O:
        if remaining <= 0:
            break
        outside = sorted([vals[j] for j in vals if j not in subtree[i]], reverse=True)
        thresh = outside[remaining-1] if len(outside) >= remaining else 0
        if vals[i] >= thresh:
            f[i] = 1
            winners.append(i)
            remaining -= 1
    return f, winners

def compute_payments(adj, parent, vals, K):
    """
    分别计算静态门槛与动态门槛：
      - p_static[i]：外部第 K 高
      - p_dynamic[i]：每步剩余 k 时的外部第 k 高
    """
    subtree = build_idt(parent)
    p_static = {}
    for i in vals:
        outside = sorted([vals[j] for j in vals if j not in subtree[i]], reverse=True)
        p_static[i] = outside[K-1] if len(outside) >= K else 0

    p_dynamic = {}
    O = bfs_order(adj, seller='s')
    remaining = K
    for i in O:
        outside = sorted([vals[j] for j in vals if j not in subtree[i]], reverse=True)
        if remaining > 0:
            p_dynamic[i] = outside[remaining-1] if len(outside) >= remaining else 0
            if vals[i] >= p_dynamic[i]:
                remaining -= 1
        else:
            p_dynamic[i] = 0
    return p_static, p_dynamic

if __name__ == "__main__":
    # 图 4 示例
    adj = {'s': ['A', 'B'], 'A': ['H'], 'B': ['C'], 'C': ['D'], 'D': ['I', 'E']}
    parent = {'A': 's', 'B': 's', 'H': 'A', 'C': 'B', 'D': 'C', 'I': 'D', 'E': 'D'}
    vals = {'A':3, 'B':1, 'H':2, 'C':2, 'D':100, 'I':4, 'E':5}
    K = 3

    # 1. Allocation
    f, winners = dna_mu_r_alloc(adj, parent, vals, K)
    # 2. 计算静态&动态门槛
    p_stat, p_dyn = compute_payments(adj, parent, vals, K)
    # 3. 支付：前 K−1 位赢家用静态门槛，最后一位赢家用动态门槛
    p = {i: 0 for i in vals}
    for idx, i in enumerate(winners):
        if idx < K-1:
            p[i] = p_stat[i]
        else:
            p[i] = p_dyn[i]

    SW = sum(vals[i] for i in vals if f[i] == 1)
    Rev = sum(p[i] for i in winners)

    print("=== DNA-MU-R Mechanism Simulation ===")
    print("Social Welfare (SW):", SW)
    print("Revenue  (Rev):", Rev)
    print("Winners :", winners)
    print("Payments:")
    for b in sorted(p):
        print(f"  {b}: {p[b]}")
