from misc.helperpg import EmptySetError

from .helper import exec_steady, update_steady


class NoResultFound(Exception):
    pass


class MultipleResultsFound(Exception):
    pass


def count_entities(entity_table):
    """Counts the entities non blocked"""
    query = f"""SELECT count(id)::int as total
           FROM {entity_table}
           WHERE blocked = false"""
    rows = exec_steady(query)

    # For this case we are just expecting one row
    if len(rows) == 0:
        raise NoResultFound("Just expecting one total as a result")
    elif len(rows) > 1:
        raise MultipleResultsFound("Just expecting one row as a result")

    return rows.pop()["total"]


def delete_entity(entity_table, entity_id):
    """Logical deletion of whichever entity"""
    q = """UPDATE {}
           SET blocked = true,
           touch_latter_time = now()
           WHERE id = {}""".format(
        entity_table, entity_id
    )
    hits = update_steady(q)

    # Expecting just one hit
    if hits > 1:
        msg = "Why did this update hit {} entities !!".format(hits)
        raise Exception(msg)


def find_entity(entity_table, entity_id):
    """Finds an entity non blocked by id"""
    query = f"""SELECT *
           FROM {entity_table}
           WHERE id = {entity_id} and blocked = false"""

    rows = exec_steady(query)

    # For this case we are just expecting one row
    if len(rows) == 0:
        raise NoResultFound("Just expecting one total as a result")
    elif len(rows) > 1:
        raise MultipleResultsFound("Just expecting one row as a result")

    return rows.pop()


def page_entities(entity_table, offset, limit, order_by, order):
    """Returns a paginated set of entities"""
    query = f"""SELECT *
           FROM {entity_table}
           WHERE blocked = false
           ORDER BY {order_by} {order}
           LIMIT {limit} OFFSET {offset}"""

    try:
        rows = exec_steady(query)
    except EmptySetError:
        return []

    entities = []
    for row in rows:
        entities.append(dict(row))

    return entities
