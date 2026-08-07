import json
import pathlib
import random


def gen(file, n, low, high):
    data = [{"duration": round(random.uniform(low, high), 2)} for _ in range(n)]
    pathlib.Path(file).write_text(json.dumps(data, indent=2))


gen("workloads/peak.json", 100, 0.3, 0.8)
gen("workloads/batch.json", 50, 10, 30)
# 混合：先短后长组合
mix = [{"duration": round(random.uniform(0.5, 1.5), 2)} for _ in range(100)] + [
    {"duration": round(random.uniform(8, 20), 2)} for _ in range(50)
]
pathlib.Path("workloads/mixed.json").write_text(json.dumps(mix, indent=2))
