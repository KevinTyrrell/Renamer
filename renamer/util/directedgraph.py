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
from typing import TypeVar, Dict, Tuple, Callable, Deque, List
from collections import deque

from util.util import require_non_none

T = TypeVar("T")


class DAG:
    def __init__(self, vertexes_edges: Dict[T, Tuple[T, ...]], ignore_unknown_vertices: bool=True):
        # Construct all vertices
        data_map = {v: DAG.__DAGNode(v) for v in vertexes_edges.keys()}
        # Setup all edges
        for v, t in vertexes_edges.items():
            v = data_map[v]
            for e in require_non_none(t):
                # Ignore edges to nodes outside of the vertex set
                if require_non_none(e) in data_map:
                    e = data_map[e]
                    v.edges.add(e)
                    e.degree += 1
                elif not require_non_none(ignore_unknown_vertices):
                    raise ValueError("DAG found edge not present in the vertex set: " + str(e))
        self.__vertices = set(data_map.values())

    def topological_sort(self, cycle_break_cb: Callable[[T, T], None] = None):
        output = []
        if len(self.__vertices) > 0:
            if cycle_break_cb is None:  # No breaker provided, cycles are not tolerated
                cycle_break_cb = DAG.__cyclic_no_tolerance
            order = deque(filter(lambda x: x.degree == 0, self.__vertices))
            while True:
                if len(order) > 0:
                    self.__eval_acyclic(order, output)
                if len(output) >= len(self.__vertices):
                    break
                # Cycles are present -- Handle appropriately
                v = next(iter(self.__vertices))
                for e in v.edges:
                    e.degree -= 1
                    if e.degree <= 0:
                        order.append(e)
                    cycle_break_cb(v.data, e.data)
        return output

    # Evaluates an acyclic set of nodes, sorting them topologically.
    def __eval_acyclic(self, order: Deque[DAG.__DAGNode], output: List[DAG.__DAGNode]) -> None:
        while True:
            v = order.pop()
            for e in v.edges:
                e.degree -= 1
                if e.degree <= 0:
                    order.append(e)
            output.append(v.data)
            self.__vertices.remove(v)
            if len(order) <= 0:
                return

    @staticmethod
    def __cyclic_no_tolerance(_, __) -> None:
        raise Exception("Direct graph contains cycles and cannot be topologically sorted")

    def __break_cycle(self, order: Deque[DAG.__DAGNode]) -> DAG.__DAGNode:
        pass

    class __DAGNode:
        def __init__(self, data: T):
            self.data = data
            self.edges = set()
            self.degree = 0
