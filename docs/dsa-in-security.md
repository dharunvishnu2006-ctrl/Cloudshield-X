# DSA in Security Context — CloudShield X v2

| Structure | Feature here | Complexity | My one line |
|---|---|---|---|
| Hash table | IOC blocklist (F6) | O(1) avg | Quickly checks whether an IP or IOC is already blocklisted. |
| Trie | Malicious domains (F6) | O(len) | Stores domains by their characters so malicious domains can be searched efficiently. |
| Min-heap (k) | Top-10 threats (F7) | O(n log k) | Keeps only the most important threats while processing many events. |
| BST / AVL | Severity index (F7) | O(log n) | Keeps severity values ordered so threats can be searched quickly. |
| Doubly + dict | LRU cache (F8) | O(1) | Quickly stores and removes recently used data from the cache. |
| Queue | Alert order (F8) | O(1) | Processes security alerts in the same order they were received. |
| Stack | Payload parsing (F8) | O(n) | Processes nested payload data by handling the most recent item first. |
| Graph + BFS | Reachable hosts (F9) | O(V+E) | Finds which hosts can be reached from a starting host through connections. |
| Dijkstra | Cheapest route (F9) | O(E log V) | Finds the lowest-cost route between connected hosts. |
| Union-Find | Segments (F9) | ~O(1) | Groups connected hosts and quickly checks whether they belong to the same segment. |
| Topo sort | Patch order (F9) | O(V+E) | Finds an order for applying patches while respecting their dependencies. |
| Sliding window | Burst detection (F10) | O(n) | Detects too many security events occurring within a short time window. |
| Segment tree | Range max (F10) | O(log n) | Quickly finds the highest value within a selected range of events. |
| DP knapsack | Response plan (F11) | O(n×W) | Chooses the best set of security actions when resources are limited. |
| KMP | Signatures (F12) | O(n+m) | Finds known attack patterns inside payloads efficiently without unnecessary comparisons. |