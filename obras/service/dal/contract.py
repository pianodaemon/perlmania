from flask_restplus import fields

from genl.restplus import api

from .entity import count_entities, delete_entity, find_entity, page_entities
from .helper import run_store_procedure

model = api.model(
    "Contract Model",
    {
        "id": fields.Integer(description="The unique identifier"),
        "number": fields.String(required=True, description="Number of contract"),
        "title": fields.String(required=True, description="Name of contract"),
        "description": fields.String(required=True, description="Desc of contract"),
        "provider": fields.Integer(required=True, description="Id of privider"),
        "delivery_stage": fields.Integer(
            required=True, description="Delivery stage of contract"
        ),
        "adjudication": fields.Integer(
            required=True, description="Type of the process of adjudication"
        ),
        "funding": fields.Integer(
            required=True, description="Type of funding used for the project"
        ),
        "program": fields.Integer(
            required=True, description="Program to which the project belongs to"
        ),
        "initial_contracted_amount": fields.Float(
            required=True, description="Initial contracted amount of contract"
        ),
        "kickoff": fields.Date(
            required=True, description="Start date of project according to contract"
        ),
        "ending": fields.Date(
            required=True, description="End date of project according to contract"
        ),
        "down_payment": fields.DateTime(required=True, description="Down payment date"),
        "down_payment_amount": fields.Float(
            required=True, description="Down payment amount"
        ),
        "ext_agreement": fields.Date(
            required=True, description="Date of the economic expansion agreement"
        ),
        "ext_agreement_amount": fields.Float(
            required=True, description="Amount of the economic expansion agreement"
        ),
        "final_contracted_amount": fields.Float(
            required=True, description="Final contracted amount"
        ),
        "total_amount_paid": fields.Float(
            required=True, description="Total amount paid"
        ),
        "outstanding_down_payment": fields.Float(
            required=True, description="Outstanding down payment"
        ),
        "inceptor_uuid": fields.String(required=True, description="uuid creator"),
    },
)


def _alter_contract(**kwargs):
    """Calls sp in charge of create and edit a contract"""
    sql = """select * from alter_contract(
        {}::integer,
        '{}'::character varying,
        '{}'::character varying,
        '{}'::text,
        {}::integer,
        {}::integer,
        {}::integer,
        {}::integer,
        {}::integer,
        {}::double precision,
        '{}'::date,
        '{}'::date,
        '{}'::date,
        {}::double precision,
        '{}'::date,
        {}::double precision,
        {}::double precision,
        {}::double precision,
        {}::double precision,
        '{}'::character varying)
        AS result( rc integer, msg text )""".format(
        kwargs["id"],
        kwargs["number"],
        kwargs["title"],
        kwargs["description"],
        kwargs["provider"],
        kwargs["delivery_stage"],
        kwargs["adjudication"],
        kwargs["funding"],
        kwargs["program"],
        kwargs["initial_contracted_amount"],
        kwargs["kickoff"],
        kwargs["ending"],
        kwargs["down_payment"],
        kwargs["down_payment_amount"],
        kwargs["ext_agreement"],
        kwargs["ext_agreement_amount"],
        kwargs["final_contracted_amount"],
        kwargs["total_amount_paid"],
        kwargs["outstanding_down_payment"],
        kwargs["inceptor_uuid"],
    )
    return run_store_procedure(sql)


def create(**kwargs):
    """Creates a contract entity"""
    kwargs["id"] = 0
    return _alter_contract(**kwargs)


def edit(**kwargs):
    """Edits the allowed properties of a contract entity"""
    return _alter_contract(**kwargs)


def block(contract_id):
    """Logical deletion of a contract entity"""
    delete_entity("contracts", contract_id)


def find(contract_id):
    """Find a contract as per id"""
    entity = find_entity("contracts", contract_id)

    return entity


def count(search_params):
    """Number of non logical deleted contracts"""
    return count_entities("contracts", search_params)


def page(page_number, page_size, order_by, asc, search_params):
    return page_entities(
        "contracts", page_number, page_size, order_by, asc, search_params
    )
