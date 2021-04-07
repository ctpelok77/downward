#! /usr/bin/env python3

import pygraphviz as pgv

import networkx as nx
import sys

def is_directed_bipartite(G):
    if not nx.algorithms.bipartite.basic.is_bipartite(G):
        return False
    X, Y = nx.algorithms.bipartite.sets(G)
    for f,t in G.edges:
        if f not in X or t not in Y:
            return False
    return True

def is_bipartite(G):
    return nx.algorithms.bipartite.basic.is_bipartite(G)    

def is_directed_chain(G):
    # Starting with the 0-indegree node, tour the graph
    zero_indegree = [n for n in G.nodes if G.in_degree(n) == 0]
    if len(zero_indegree) != 1:
        return False
    curr = zero_indegree[0]
    all_nodes = set()
    all_nodes.add(curr)
    while True:
        edges = G.edges(curr)
        if len(edges) > 1:
            return False
        if len(edges) == 1:
            for edge in edges:
                curr = edge[1]
                break
        else:
            break
        all_nodes.add(curr)
    return len(all_nodes) == len(G.nodes)
    

def is_chain(G):
    # All nodes have degree 2, except the start and end nodes that have degree 1
    one_degree = [n for n in G.nodes if G.degree(n) == 1]
    two_degree = [n for n in G.nodes if G.degree(n) == 2]
    return len(one_degree) == 2 and len(two_degree) == len(G.nodes) - 2

def is_tree(G):
    # Starting with the 0-indegree node, 
    zero_indegree = [n for n in G.nodes if G.in_degree(n) == 0]
    if len(zero_indegree) != 1:
        return False
    root = zero_indegree[0]
    visited = set()
    visited.add(root)
    queue = set()
    queue.add(root)
    while len(queue) > 0:
        s = queue.pop()
        for edge in G.edges(s):
            n = edge[1]
            if G.in_degree(n) != 1:
                return False
            if edge in visited:
                return False
            visited.add(n)
            queue.add(n)
    return len(visited) == len(G.nodes)

def is_polytree(G):
    return nx.algorithms.tree.recognition.is_tree(G)

def is_DAG(G):
    return nx.algorithms.dag.is_directed_acyclic_graph(G)


def is_fork(G):
    zero_indegree = [n for n in G.nodes if G.in_degree(n) == 0]
    if len(zero_indegree) != 1:
        return False
    root = zero_indegree[0]
    return len(G.edges(root)) == len(G.edges())


def is_inverted_fork(G):
    zero_outdegree = [n for n in G.nodes if G.out_degree(n) == 0]
    if len(zero_outdegree) != 1:
        return False
    root = zero_outdegree[0]
    return len(G.in_edges(root)) == len(G.edges())


def is_star(G):
    one_degree = [n for n in G.nodes if G.degree(n) == 1]
    root = [n for n in G.nodes if G.degree(n) > 1]
    if len(root) != 1:
        return False

    if G.degree(root[0]) != len(one_degree):
        return False

    return len(one_degree) == len(G.nodes) - 1

def is_complete(G):
    num_nodes = len(G.nodes)
    for n in G.nodes:
        if G.in_degree(n) < num_nodes - 1:
            return False
    return True

if __name__ == "__main__":
    gv = pgv.AGraph(sys.argv[1], strict=False, directed=True)
    G = nx.DiGraph(gv)

    print("Directed Bipartite:", is_directed_bipartite(G))
    print("Bipartite:", is_bipartite(G))
    print("Directed Chain:", is_directed_chain(G))
    print("Chain:", is_chain(G))
    print("Tree:", is_tree(G))
    print("Polytree:", is_polytree(G))
    print("Directed Acyclic Graph:", is_DAG(G))
    print("Fork:", is_fork(G))
    print("Inverted Fork:", is_inverted_fork(G))
    print("Star:", is_star(G))
    print("Complete:", is_complete(G))
