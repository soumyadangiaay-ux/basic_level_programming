# BFS and DFS on a Simple Graph

from collections import deque

# The graph (each node points to its neighbours)
graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": []
}

# ----- Breadth First Search (uses a Queue) -----
def bfs(graph, start):
    visited = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            for neighbour in graph[node]:
                if neighbour not in visited:
                    queue.append(neighbour)
    return visited

# ----- Depth First Search (uses recursion) -----
def dfs(graph, start, visited=None):
    if visited is None:
        visited = []
    visited.append(start)
    for neighbour in graph[start]:
        if neighbour not in visited:
            dfs(graph, neighbour, visited)
    return visited

# Starting node from the user
start = input("Enter the starting node (A/B/C/D/E/F): ").upper()

print("\n--- Graph Traversal Started ---")
print("BFS Traversal (level by level):", bfs(graph, start))
print("DFS Traversal (deep first)   :", dfs(graph, start))

print("\nTask Completed!")
