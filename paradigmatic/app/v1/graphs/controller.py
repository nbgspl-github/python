import copy
import datetime
import typing as t
from fastapi import HTTPException, status
from mongoengine import Q

from . import models, schemas

edge_rename_dict = {"to": "source_id", "from": "destination_id"}


def create_graph(graph: schemas.GraphBase) -> schemas.Graph:
    new_graph_dict = graph.dict(by_alias=True)
    new_graph = models.Graph(**new_graph_dict).save()
    graph_dict = new_graph.to_mongo().to_dict()
    return graph_dict


def list_graphs() -> t.List[schemas.Graph]:
    all_graphs = models.Graph.objects()
    return [graph.to_mongo().to_dict() for graph in all_graphs]


def get_graph(graph_id) -> schemas.Graph:
    return models.Graph.objects().filter(id=graph_id).first().to_mongo().to_dict()


def create_node(node: schemas.NodeBase) -> schemas.Node:
    new_node_dict = node.dict(by_alias=True)
    new_node = models.Node(**new_node_dict).save()
    node_dict = new_node.to_mongo().to_dict()
    return node_dict


def get_node(node_vis_id: str) -> schemas.Node:
    node = models.Node.objects.filter(vis_id=node_vis_id).first()
    if not node:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Object_not_found")
    node_dict = node.to_mongo().to_dict()
    return node_dict


def list_nodes(graph_id: str) -> schemas.NodeEdgeList:
    node_objects = models.Node.objects.filter(graph_id=graph_id).all()
    nodes = []
    for curr_node in node_objects:
        curr_dict = curr_node.to_mongo().to_dict()
        curr_dict.pop("description", None)
        curr_dict['_id'] = str(curr_dict['_id'])
        nodes.append(curr_dict)
    result = {"nodes": nodes, "edges": []}
    edges = []
    node_ids = [str(x["vis_id"]) for x in nodes]
    edge_objects = models.Edge.objects.filter(Q(source_id__in=node_ids) or Q(destination_id__in=node_ids)).all()
    for curr_edge in edge_objects:
        curr_dict = curr_edge.to_mongo().to_dict()
        curr_dict = bulk_rename_keys(curr_dict, reverse=True)
        curr_dict['_id'] = str(curr_dict['_id'])
        edges.append(curr_dict)
        result["edges"] = edges
    return schemas.NodeEdgeList(**result)


def update_node(node: schemas.NodeEdit, node_vis_id: str) -> schemas.Node:
    object_query = models.Node.objects(vis_id=node_vis_id)
    first_object = object_query.first()
    if first_object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='node_not_found')
    update_data = node.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.datetime.utcnow()
    object_query.update(**update_data)
    return object_query.first()


def delete_node(node_vis_id: str, with_subdata: bool = True):
    node_query = models.Node.objects(vis_id=node_vis_id)
    node_obj = node_query.first()
    if not node_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Object_not_found")
    if with_subdata:
        source_edges = models.Edge.objects.filter(source_id=node_vis_id)
        source_edges.delete()
        destination_edges = models.Edge.objects.filter(destination_id=node_vis_id)
        destination_edges.delete()
    node_obj.delete()
    return {"status": "success"}


def create_edge(new_edge_dict: dict) -> dict:
    new_edge_backend = bulk_rename_keys(copy.deepcopy(new_edge_dict), edge_rename_dict)
    new_edge = models.Edge(**new_edge_backend).save()
    new_edge_dict["_id"] = str(new_edge.id)
    return new_edge_dict


def bulk_rename_keys(user_dict, key_dict = edge_rename_dict, reverse = False):
    for current_key in key_dict:
        new_key = key_dict[current_key]
        if reverse:
            user_dict[current_key] = user_dict.pop(new_key)
        else:
            user_dict[new_key] = user_dict.pop(current_key)
    return user_dict


def delete_edge(edge_vis_id: str):
    edge_obj = models.Edge.objects(vis_id=edge_vis_id)
    if not edge_obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Edge_not_found")
    edge_obj.delete()
    return {"status": "success"}

