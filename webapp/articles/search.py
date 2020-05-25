from flask import current_app
from sqlalchemy.orm.collections import InstrumentedList


def add_to_index(index, model) -> None:
    """
    Add data to index
    """
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        _attr_value = getattr(model, field)
        if isinstance(_attr_value, InstrumentedList):
            payload[field] = [
                getattr(attr_value_item, attr_value_item.__indexable__)
                for attr_value_item in _attr_value
            ]
        else:
            payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model) -> None:
    """
    Remove data from index
    """
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)
