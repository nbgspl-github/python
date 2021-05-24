import datetime
import re
from collections import defaultdict
from fastapi import HTTPException, status
from starlette.responses import FileResponse


# first item contains labels, original key forms the first label
def dict_to_list(mydict, keyname, labels=True):
    new_list = []
    current_dict = {}
    for current_key in mydict.keys():
        current_dict = mydict[current_key]
        new_list.append([current_key] + list(current_dict.values()))
    if labels:
        labels = [keyname] + list(current_dict.keys())
        new_list.insert(0, labels)
    return new_list


def tuple_list_to_dict(tuple_list):
    res = defaultdict(list)
    for i, j in tuple_list:
        res[i].append(j)
    return dict(res)


def flatten_2level_list(listname):
    flat_list = [item for sublist in listname for item in sublist]
    return flat_list


def update_obj(object_id, object_schema, model_name, error_msg='Object_not_found'):
    object_query = model_name.objects(id=object_id)
    first_object = object_query.first()
    if first_object is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=error_msg)
    update_data = object_schema
    if not type(object_schema) == dict:
        update_data = update_data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.datetime.utcnow()
    object_query.update(**update_data)
    return object_query.first()


def rename_attribute(object_, old_attribute_name, new_attribute_name):
    setattr(object_, new_attribute_name, getattr(object_, old_attribute_name))
    delattr(object_, old_attribute_name)  # this is not working
    return object_


def rename_field(model_name, old_field_name, new_field_name):
    object_list = model_name.objects().all()
    all_objects = []
    for obj in object_list:
        renamed_obj = rename_attribute(obj, old_field_name, new_field_name)
        renamed_obj.save()
        all_objects.append(renamed_obj)
    return all_objects


def add_field(model_name, field_name, value):
    object_list = model_name.objects().all()
    for obj in object_list:
        setattr(obj, field_name, value)
        obj.save()
    return


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = FileResponse('statics/favicon.ico')
    await response(scope, receive, send)


def convert_username_to_ids(user_id_by_username, groups):
    new_groups = []
    for group in groups:
        new_groups.append([user_id_by_username[username] for username in group])
    return new_groups


def add_years_current_datetime(years):
    c = datetime.datetime.utcnow()
    n = c.replace(year=c.year + years)
    return n


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def natural_sort(my_list):
    return my_list.sort(key=natural_keys)
