#    Copyright (C) 2004-2018 by
#    All rights reserved.
#    MIT license.
#
# Author: Vadim Ivlev


# Some functions to show tree graphs.
# Can be used both in standalone programs
# and in `jupyther` nonebooks.

# Preconditions
# -------------
# The folowing libraries should be installed
# `matplotlib, networkx, graphviz, pygraphviz`

# Please use conda or pip.

# Usage
# -----

# from showtree import show_binary_tree, show_tree_graph


import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout


def uid_gen():
    '''node id generator'''
    n = 0
    while True:
        n += 1
        yield n


uid = uid_gen()


# ------------------------------------------------------

def show_tree_graph(G, file_name=None):
    """
    Shows a tree graph.

    Parameters
    ----------
    G : NetworkX tree graph
      A tree graph created with NetworkX

    file_name: if specified the picture will be saved instead of showing.

    Examples
    --------
    >>> gg = nx.balanced_tree(3, 2)
    >>> show_tree_graph(gg)
    """

    plt.rcParams["figure.figsize"] = [10., 7.]
    pos = graphviz_layout(G, prog='dot')

    # null_nodes = [x for x in G.nodes if G.node[x]['label'] == '']
    not_null_nodes = [
        x for x in G.nodes if G.node[x].get('label', str(x)) != '']
    # null_edges = [e for e in G.edges if G.node[e[1]]['label'] == '']
    # not_null_edges = [e for e in G.edges if G.node[e[1]]['label'] != '']

    node_lbls = nx.get_node_attributes(G, 'label')
    edge_lbls = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True,
            nodelist=not_null_nodes if len(not_null_nodes) > 0 else None,
            # edgelist=not_null_edges,
            labels=node_lbls if len(node_lbls) > 0 else None,

            width=1.0,
            linewidths=0.0,
            node_size=700,
            node_color="#1485CC",
            edge_color="#cccccc",
            font_size=12,
            label="BST",
            alpha=1.0
            )

    nx.draw_networkx_edge_labels(G, pos, font_size=8,
                                 edge_labels=edge_lbls
                                 )

    # nx.draw_networkx_nodes(G, pos, node_size=700, alpha=1.0,
    #     node_color="white", nodelist=null_nodes)
    # nx.draw_networkx_edges(G, pos, alpha=0.9, width=6, edge_color="orange", edgelist=[(1, 'Petya')])

    if not file_name:
        plt.show()
    else:
        plt.savefig(file_name)
        plt.clf()


# ------------------------------------------------------------
def build_binary_tree_graph(nx_graph, parent_node_id, tree_node, label_attr='data', edge_label=None):
    if not tree_node:
        node_id = next(uid)
        nx_graph.add_node(node_id, label='')
        if parent_node_id != None:
            nx_graph.add_edge(parent_node_id, node_id, label=edge_label)
        return

    node_id = next(uid)
    nx_graph.add_node(node_id, label=getattr(tree_node, label_attr, ''))

    if parent_node_id != None:
        nx_graph.add_edge(parent_node_id, node_id, label=edge_label)

    if tree_node.left or tree_node.right:
        build_binary_tree_graph(
            nx_graph, node_id, tree_node.left, label_attr, 'L')
        build_binary_tree_graph(
            nx_graph, node_id, tree_node.right, label_attr, 'R')


# -------------------------------------------------------
def show_binary_tree(root_node, label_attr='data', file_name=None):
    """
    Shows a tree of nodes similar to:
    ```
    class Node:
        def __init__(self, val=''):
            self.data = val
            self.left = None
            self.right = None

    ```
    The nodes on the chart will be labeled with `data` attribute.
    If you want to use a different attribute change `label_attr` parameter.

    Parameters
    ----------
    root_node : the root node of a tree. 
      A tree graph created with NetworkX

    label_attr: an attribute used for labeling nodes

    file_name: if specified the picture will be saved instead of showing.


    Examples
    --------
    >>> show_binary_tree(root)
    """

    G = nx.DiGraph()
    build_binary_tree_graph(G, None, root_node, label_attr)
    show_tree_graph(G, file_name=file_name)



# TESTING -----------------------------------------------
if __name__ == '__main__':
    from random import sample, seed

    class Node:
        def __init__(self, val=''):
            self.data = val
            self.left = None
            self.right = None

    def add_node(root, val):
        if not root:
            return Node(val)
        if val < root.data:
            root.left = add_node(root.left, val)
        elif val > root.data:
            root.right = add_node(root.right, val)

        return root

    def build_bst(lst):
        bst = None
        for v in lst:
            bst = add_node(bst, v)

        return bst

    seed(1)
    r = sample(range(11, 100), 20)
    show_binary_tree(build_bst(r))
    # show_binary_tree(build_bst(r), file_name='bst.png')

    gg = nx.balanced_tree(3, 2)
    show_tree_graph(gg)
    # show_tree_graph(gg, file_name='tree.png')
