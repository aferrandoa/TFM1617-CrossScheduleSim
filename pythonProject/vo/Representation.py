"""Representation class"""
class Representation(object):
    """Contains the transaction weight matrix, the initial nodes """

    def __init__(self, i_vertex_list, i_edge_list, i_weight_matrix):
        self.vertex_list = i_vertex_list
        self.edge_list = i_edge_list
        self.weight_matrix = i_weight_matrix
