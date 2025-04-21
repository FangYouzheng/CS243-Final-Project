from collections import defaultdict

# 1. 网络结构（有向）
neighbors = {
    's': ['A', 'B'],
    'A': ['H'],
    'B': ['C'],
    'C': ['D'],
    'D': ['E', 'I'],
    'E': [],
    'H': [],
    'I': []
}

# 2. 真实估值
vals = {
    'A': 3,
    'B': 1,
    'C': 2,
    'D': 100,
    'E': 5,
    'H': 2,
    'I': 4
}

# 3. 参数
m = 3  # 商品数量（同质）
m_remaining = m

# 4. 初始化
explored = set(neighbors['s'])  # 初始可见买家 A
winners = []
payments = {b: 0 for b in vals}  # 给所有买家预设 0 支付

def priority(b):
    """优先级：邻居数目；同级时按估值再按姓名字母序"""
    return (len(neighbors[b]), vals[b], b)

# 5. 迭代分配
while len(winners) < m_remaining + len(winners) and len(winners) < m:
    m_prime = m - len(winners)
    # 5.1 候选集 P
    avail = explored - set(winners)
    if len(avail) <= m_prime:
        P = explored.copy()
    else:
        # 按估值降序选出前 m' 名
        top_m = sorted(avail, key=lambda x: vals[x], reverse=True)[:m_prime]
        P = set(winners) | set(top_m)
    # 5.2 选择赢家 w
    # P \ winners 中按优先级排序，取第一
    candidates = list(P - set(winners))
    candidates.sort(key=priority, reverse=True)
    w = candidates[0]
    # 5.3 计算 p̂_w
    remain_vals = sorted([vals[b] for b in explored - set(winners)], reverse=True)
    if len(remain_vals) >= m_prime + 1:
        p_hat = remain_vals[m_prime]
    else:
        p_hat = 0
    payments[w] = p_hat

    # 5.4 更新状态
    winners.append(w)
    # 把 w 的邻居加入 explored
    for nb in neighbors[w]:
        explored.add(nb)

# 6. 结果统计
SW = sum(vals[w] for w in winners)
Rev = sum(payments[w] for w in winners)

# 7. 输出
print("=== MUDAN Mechanism Simulation ===")
print("Social Welfare (SW):", SW)
print("Revenue  (Rev):", Rev)
print("Winners :", winners)
print("Payments:")
for b in sorted(payments):
    print(f"  {b}: {payments[b]}")
