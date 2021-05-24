import typing as t
from fastapi import APIRouter, Depends, Request, Response
from . import schemas
from paradigmatic.app.v1.core.auth import get_current_active_superuser, get_current_active_user

from .controller import (create_node, update_node, delete_node, list_nodes, get_node, delete_edge, create_edge,
                         create_graph, list_graphs, get_graph)

graphs_router = r = APIRouter()


@r.post("/graph", response_model=schemas.Graph)
async def create_graph_api(
        graph: schemas.GraphBase,
        current_user=Depends(get_current_active_user)
):
    """
    Create Graph
    """
    return create_graph(graph)


@r.get("/graph", response_model=t.List[schemas.Graph])
async def get_all_graph_api(
        response: Response,
        current_user=Depends(get_current_active_user),
):
    """
    Get all Graphs
    """
    all_graphs = list_graphs()
    response.headers["Content-Range"] = f"0-9/{len(all_graphs)}"

    return all_graphs


@r.get("/graph/{graph_id}", response_model=schemas.Graph)
async def get_graph_api(
        response: Response,
        graph_id: str,
        current_user=Depends(get_current_active_user),
):
    """
    Get Graph by Id
    """
    return get_graph(graph_id)


@r.post("/graphs/{graph_id}/node", response_model=schemas.Node)
async def create_node_api(
        graph_id: str,
        node: schemas.NodeBase,
        current_user=Depends(get_current_active_user)
):
    """
    Create Node
    """
    return create_node(node)


@r.get("/graph/{graph_id}/nodes", response_model=schemas.NodeEdgeList)
async def get_graph_with_nodes(
        response: Response,
        graph_id: str,
        current_user=Depends(get_current_active_user),
):
    """
    Get Graph with Nodes and Edges
    """
    all_nodes_edges = list_nodes(graph_id)
    return all_nodes_edges


@r.get("/graph/{graph_id}/node/{node_id}", response_model=schemas.Node)
async def get(
        graph_id: str,
        node_vis_id: str,
        current_user=Depends(get_current_active_user),
):
    """
    Get single Node with descriptions
    """
    node = get_node(node_vis_id)
    return node


@r.put("/graph/{graph_id}/node/edit", response_model=schemas.Node)
async def edit(
        graph_id: str,
        node: schemas.NodeEdit,
        node_vis_id: str,
        current_user=Depends(get_current_active_user),
):
    """
    Update Node
    """
    updated_node = update_node(node, node_vis_id)
    return updated_node.to_mongo().to_dict()


@r.delete("/graph/{graph_id}/nodes/{node_vis_id}", response_model=dict)
async def delete_node_api(
        response: Response,
        graph_id: str,
        node_vis_id: str,
        current_user=Depends(get_current_active_user),
):
    """
    Delete Node
    """
    return delete_node(node_vis_id)


@r.post("/graph/{graph_id}/edge", response_model=dict)
async def create_edge_api(
        graph_id: str,
        edge: dict,
        current_user=Depends(get_current_active_user)
):
    """
    Create Edge
    """
    return create_edge(edge)


@r.delete("/graph_id/{graph_id}/edges/{edge_vis_id}", response_model=dict)
async def delete_edge_api(
        response: Response,
        graph_id: str,
        edge_vis_id: str,
        current_user=Depends(get_current_active_user),
):
    """
    Delete Edge
    """
    return delete_edge(edge_vis_id)