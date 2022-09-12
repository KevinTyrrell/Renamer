"""
    CLI tool written in Python 3 used to systemically rename files in a directory while adhering to a variety of criteria.
    Copyright (C) 2022  Kevin Tyrrell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations
from typing import TypeVar

from util.util import require_non_none

T = TypeVar("T")


class DAG:
    def __init__(self):
        """
        Constructs a directed acyclic graph instance
        """
        self.__nodes = {}  # Map[data] -> Node

    def add_vertex(self, data: T) -> bool:
        """
        :param data: Data of the vertex
        :return: False if the graph already contains the vertex
        """
        if require_non_none(data) in self.__nodes:
            return False
        self.__nodes[data] = DAG.__DAGNode(data)
        return True

    def add_edge(self, vertex: T, edge: T) -> bool:
        """
        :param vertex: Vertex in which to add an edge
        :param edge: Connected vertex from the specified vertex
        :return: False if the vertex already contains the specified edge
        """
        if require_non_none(vertex) not in self.__nodes:
            raise ValueError("Vertex is not present within the graph: {}".format(vertex))
        if require_non_none(edge) not in self.__nodes:
            raise ValueError("Vertex edge is not present within the graph: {}".format(edge))
        if vertex == require_non_none(edge):
            raise ValueError("Vertex is already a strongly connected component with itself: {}".format(vertex))
        v, e = self.__nodes[vertex], self.__nodes[edge]
        if e in v.edges:
            return False
        v.edges.add(e)
        e.degree += 1
        return True

    class __DAGNode:
        def __init__(self, data: T):
            self.data = data
            self.edges = set()
            self.degree = 0

