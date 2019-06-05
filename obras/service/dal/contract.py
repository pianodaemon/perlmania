from datetime import datetime

from .entity import count_entities, delete_entity, find_entity, page_entities
from .helper import run_store_procedure


def _marshall(entity):
    """ Gets a contract from the database and marshalls the it's data"""
    contract = {}
    attributes = set(
        [
            "id",
            "number",
            "title",
            "description",
            "provider",
            "delivery_stage",
            "initial_contracted_amount",
            "kickoff",
            "ending",
            "down_payment",
            "down_payment_amount",
            "ext_agreement",
            "ext_agreement_amount",
            "final_contracted_amount",
            "total_amount_paid",
            "outstanding_down_payment",
            "inceptor_uuid",
        ]
    )

    for attr in attributes:
        if type(entity[attr]) == datetime:
            contract[attr] = entity[attr].strftime("%Y-%m-%d")
        else:
            contract[attr] = entity[attr]

    return contract


def _alter_contract(**kwargs):
    """Calls sp in charge of create and edit a contract"""
    sql = """select * from alter_contract(
        {}::integer,
        '{}'::character varying,
        '{}'::character varying,
        '{}'::text,
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


def _setup_criteria(**kwsearch):
    """Incepts filters as per search requirement"""
    for k in ('title', 'contract', 'description'):
        v = kwsearch.get(k, None)
        if v is None:
            continue
        yield SlackFilterTxt(v)

    interval_buffer = (None, None)
    for idx, k in enumerate('kickoff', 'ending'):
        interval_buffer[idx] = kwsearch.get(k, None)
        if all(interval_buffer):
            yield SlackFilterInterval(*interval_buffer)


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

    return _marshall(entity)


def page(page_number, page_size, order_by, asc, **kwsearch):
    search_criteria = set([for k in _setup_criteria(**kwsearch)])
    rows = page_entities("contracts", page_number, page_size,
                         order_by, asc, search_criteria)

    return [_marshall(entity) for entity in rows]


def count(**kwsearch):
    """Number of non logical deleted contracts"""
    search_criteria = set([for k in _setup_criteria(**kwsearch)])
    return count_entities("contracts", search_criteria)
