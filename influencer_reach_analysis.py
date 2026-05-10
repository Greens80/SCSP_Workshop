import json

with open('data.js', 'r') as f:
    content = f.read()

json_str = content[len('window.GRAPH_DATA = '):].rstrip().rstrip(';')
data = json.loads(json_str)

nodes = data['nodes']
edges = data['edges']

# Build adjacency list
adj = {}
for node in nodes:
    adj[node['id']] = set()

for edge in edges:
    s, t = edge['s'], edge['t']
    adj[s].add(t)
    adj[t].add(s)

# Get top influencers sorted by rank
influencers = sorted([n for n in nodes if n['influencer']], key=lambda x: x['influencerRank'])

print("=== Influencer 2-Step Reach Analysis ===")
print(f"Network: {len(nodes):,} people, {len(edges):,} connections\n")

print("Top Influencers (by degree):")
for inf in influencers:
    print(f"  Rank {inf['influencerRank']}: Person {inf['id']} — {inf['degree']} direct friends")

print("\n2-Step Reach per Influencer:")
all_reachable = set()
for inf in influencers:
    nid = inf['id']
    step1 = adj[nid]
    step2 = set()
    for neighbor in step1:
        step2.update(adj[neighbor])
    reachable = (step1 | step2) - {nid}
    all_reachable.update(reachable)
    print(f"  Person {nid} (rank {inf['influencerRank']}, {inf['degree']} friends): {len(reachable):,} people within 2 steps")

print(f"\n{'='*45}")
print(f"Combined unique reach (all top influencers): {len(all_reachable):,} / {len(nodes):,} people")
print(f"Network coverage: {100*len(all_reachable)/len(nodes):.1f}%")
