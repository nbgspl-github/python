import typing as t
from ..custom_base_schemas import CustomBaseModel, CustomIdModel
from pydantic import BaseModel

to = t.Optional


class GraphBase(CustomBaseModel):
    name: str
    description: to[str]
    vis_id: to[str]


class GraphEdit(BaseModel):
    name: to[str]
    description: to[str]


class Graph(GraphBase, CustomIdModel):
    pass


class NodeBase(CustomBaseModel):
    graph_id: str
    label: str
    description: to[str]
    vis_id: to[str]
    x: to[float]
    y: to[float]


class NodeEdit(BaseModel):
    label: to[str]
    description: to[str]
    x: to[float]
    y: to[float]


class Node(NodeBase, CustomIdModel):
    pass


class EdgeBase(CustomBaseModel):
    vis_id: to[str]
    label: to[str]
    source_id: str
    destination_id: str


class Edge(EdgeBase, CustomIdModel):
    pass


class NodeDescriptionBase(CustomBaseModel):
    node_id: str
    user_name: str
    user_recommended: bool
    description: to[str]


class NodeDescription(NodeDescriptionBase, CustomIdModel):
    pass


class NodeEdgeList(BaseModel):
    nodes: list
    edges: list
