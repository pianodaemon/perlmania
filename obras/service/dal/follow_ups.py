from flask_restplus import fields

from genl.restplus import api
from misc.helperpg import EmptySetError

from .entity import (MultipleResultsFound, NoResultFound, delete_entity,
                     find_entity)
from .helper import exec_steady, run_store_procedure

model = api.model(
    "Follow Up Model",
    {
        "id": fields.Integer(description="The unique db identifier"),
        "project": fields.Integer(required=True, description="Id of project"),
        "verified_progress": fields.Integer(),
        "financial_advance": fields.Integer(),
        "img_paths": fields.String(),
        "check_stage": fields.Integer(),
        "check_date": fields.Date(),
        "inceptor_uuid": fields.String(required=True, description="UUID of creator"),
    },
)

project_follow_ups_model = api.model(
    "Projects with follow ups model",
    {
        "project_id": fields.Integer(),
        "project_title": fields.String(),
        "city_id": fields.Integer(),
        "contract_id": fields.Integer(),
        "contract_number": fields.String(),
        "contract_title": fields.String(),
        "contract_description": fields.String(),
        "program_id": fields.Integer(),
        "initial_contracted_amount": fields.Float(),
        "contract_kickoff": fields.Date(),
        "contract_ending": fields.Date(),
        "down_payment": fields.Date(),  # Check
        "down_payment_amount": fields.Float(),
        "ext_agreement": fields.Date(),  # Check
        "ext_agreement_amount": fields.Float(),
        "final_contracted_amount": fields.Float(),
        "total_amount_paid": fields.Float(),
        "outstanding_down_payment": fields.Float(),
        "provider_id": fields.Integer(),
        "provider": fields.String(),
        "department_id": fields.Integer(),
        "department": fields.String(),
        "category_id": fields.Integer(),
        "category": fields.String(),
        "adjudication_id": fields.Integer(),
        "adjudication": fields.String(),
        "funding_id": fields.Integer(),
        "funding": fields.String(),
        "delivery_stage_id": fields.Integer(),
        "delivery_stage": fields.String(),
        "verified_progress": fields.Integer(),
        "financial_advance": fields.Integer(),
        "follow_up": fields.Integer(),
        "check_stage": fields.Integer(),
        "check_date": fields.Date(),
        "img_paths": fields.String(),
    },
)


def _setup_search_criteria(search_params):
    criteria = []
    for field, value in search_params.items():
        criteria.append(f"follow_ups.{field} = {value}")

    return " AND ".join(criteria)


def _alter_follow_ups(**kwargs):
    """Calls a store procedure to create or edit a follow up record"""
    sql = """SELECT * FROM alter_follow_ups(
    {}::integer,
    {}::integer,
    {}::smallint,
    {}::smallint,
    '{}'::text,
    {}::integer,
    '{}'::date,
    '{}'::character varying
    )
    AS result(rc integer, msg text)""".format(
        kwargs["id"],
        kwargs["project"],
        kwargs["verified_progress"],
        kwargs["financial_advance"],
        kwargs["img_paths"],
        kwargs["check_stage"],
        kwargs["check_date"],
        kwargs["inceptor_uuid"],
    )

    return run_store_procedure(sql)


def create(**kwargs):
    """Creates follow up entity"""
    kwargs["id"] = 0
    return _alter_follow_ups(**kwargs)


def edit(**kwargs):
    return _alter_follow_ups(**kwargs)


def block(follow_up_id):
    """Logical deletion of a follow up"""
    delete_entity("follow_ups", follow_up_id)


def find(follow_up_id):
    return find_entity("follow_ups", follow_up_id)


def count(search_params=None):
    """Returns the number of non-logically deleted follow-ups"""
    """Counts the entities non blocked"""
    query = """SELECT count(id)::int as total
           FROM follow_ups
           WHERE blocked = false"""

    if search_params is not None:
        query += " AND " + _setup_search_criteria(search_params)

    rows = exec_steady(query)

    # For this case we are just expecting one row
    if len(rows) == 0:
        raise NoResultFound("Just expecting one total as a result")
    elif len(rows) > 1:
        raise MultipleResultsFound("Just expecting one row as a result")

    return rows.pop()["total"]


def paged(offset, limit, order_by, order, search_params=None):
    query = """SELECT *
           FROM follow_ups
           WHERE blocked = false"""

    if search_params is not None:
        query += " AND " + _setup_search_criteria(search_params)

    query += f" ORDER BY {order_by} {order} LIMIT {limit} OFFSET {offset}"

    try:
        rows = exec_steady(query)
    except EmptySetError:
        return []

    entities = []
    for row in rows:
        entities.append(dict(row))

    return entities
