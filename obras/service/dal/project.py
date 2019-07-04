from flask_restplus import fields

from genl.restplus import api
from misc.helperpg import EmptySetError

from .entity import (MultipleResultsFound, NoResultFound, count_entities,
                     delete_entity, find_entity, page_entities)
from .helper import exec_steady, run_store_procedure

model = api.model(
    "Project Model",
    {
        "id": fields.Integer(required=True, description="Unique identifier"),
        "title": fields.String(required=True, description="Project name"),
        "description": fields.String(
            required=True, description="Short description of the project"
        ),
        "city": fields.Integer(required=True, description="DB id of the city"),
        "category": fields.Integer(required=True, description="DB id of the category"),
        "department": fields.Integer(
            required=True, description="DB id of the department"
        ),
        "budget": fields.Integer(required=True, description="DB id of the budget"),
        "contract": fields.Integer(required=True, description="DB id of the contract"),
        "planed_kickoff": fields.Date(
            required=True, description="When the project is planned to start"
        ),
        "planed_ending": fields.Date(
            required=True, description="When the project is planned to end"
        ),
        "inceptor_uuid": fields.String(
            required=True, description="UUID of the user who created the project"
        ),
    },
)


def _alter_project(**kwargs):
    """Calls sp in charge of create and edit a project"""
    sql = """select * from alter_project(
        {}::integer,
        '{}'::character varying,
        '{}'::text,
        {}::integer,
        {}::integer,
        {}::integer,
        {}::integer,
        {}::double precision,
        '{}'::date,
        '{}'::date,
        '{}'::character varying)
    AS result( rc integer, msg text )""".format(
        kwargs["id"],
        kwargs["title"],
        kwargs["description"],
        kwargs["city"],
        kwargs["category"],
        kwargs["department"],
        kwargs["contract"],
        kwargs["budget"],
        kwargs["planed_kickoff"],
        kwargs["planed_ending"],
        kwargs["inceptor_uuid"],
    )
    return run_store_procedure(sql)


def _setup_search_criteria(search_params, joint=True):
    # TODO: add checks to avoid SQL injections
    criteria = []
    if joint:
        filters = {
            "project": "project_id",
            "contract_number": "contract_number",
            "contract": "contract_id",
            "category": "category_id",
            "department": "department_id",
            "city": "city_id",
            "check_stage": "check_stage",
            "adjudication": "adjudication",
            "funding": "funding",
            "program": "program",
            "provider": "provider_id",
        }

        if search_params and search_params.get("start_date"):
            criteria.append(f"inception_time >= '{search_params['start_date']}'")

        if search_params and search_params.get("end_date"):
            criteria.append(f"inception_time <= '{search_params['end_date']}'")

        if search_params and search_params.get("contract_start_date"):
            criteria.append(f"contract_kickoff >= '{search_params['start_date']}'")

        if search_params and search_params.get("contract_end_date"):
            criteria.append(f"contract_kickoff <= '{search_params['end_date']}'")
    else:
        filters = {
            "project": "projects.id",
            "category": "projects.category",
            "contract": "projects.contract",
            "department": "projects.department",
            "city": "projects.city",
            "check_stage": "follow_ups.check_stage",
            "adjudication": "contracts.adjudication",
            "funding": "contracts.funding",
            "program": "contracts.funding",
            "provider": "contracts.provider",
        }

        if search_params and search_params.get("start_date"):
            criteria.append(
                f"follow_ups.inception_time >= '{search_params['start_date']}'"
            )

        if search_params and search_params.get("end_date"):
            criteria.append(
                f"follow_ups.inception_time <= '{search_params['end_date']}'"
            )

        if search_params and search_params.get("contract_start_date"):
            criteria.append(f"contracts.kickoff >= '{search_params['start_date']}'")

        if search_params and search_params.get("contract_end_date"):
            criteria.append(f"contracts.kickoff <= '{search_params['end_date']}'")

    if search_params is not None:
        for field, value in search_params.items():
            if filters.get(field):
                criteria.append(f"{filters[field]} = {value}")

    return " AND ".join(criteria)


def paged_with_follow_ups(
    offset=0, limit=10, search_params=None, empty_follow_ups=True
):
    """Paginated results that include the latest status
    using the follow up to calculate them
    """
    sql = """
    SELECT * FROM (
        SELECT DISTINCT ON (projects.id)
            projects.id AS project_id,
            projects.title AS project_title,
            projects.city AS city_id,
            contracts.id AS contract_id,
            contracts.number AS contract_number,
            contracts.adjudication AS adjudication,
            contracts.funding AS funding,
            contracts.program AS program,
            contracts.provider AS provider_id,
            contracts.kickoff AS contract_kickoff,
            providers.title AS provider,
            departments.id AS department_id,
            departments.title AS department,
            categories.id AS category_id,
            categories.title AS category,
            follow_ups.id AS follow_up,
            follow_ups.verified_progress,
            follow_ups.financial_advance,
            follow_ups.check_stage,
            follow_ups.check_date,
            follow_ups.img_paths,
            follow_ups.inception_time
        FROM projects
        JOIN contracts ON contracts.id = projects.contract
        JOIN categories ON categories.id = projects.category
        JOIN departments ON departments.id = projects.department
        JOIN providers ON providers.id = contracts.provider
        {} follow_ups ON follow_ups.project = projects.id
             AND follow_ups.blocked = false
        WHERE projects.blocked = false
        ORDER BY projects.id, follow_ups.check_date DESC)
    AS temp
    {}
    OFFSET {} LIMIT {};
    """

    search = _setup_search_criteria(search_params)
    if len(search) > 0:
        search = " WHERE " + search

    if empty_follow_ups:
        follow_ups_join = "LEFT JOIN"
    else:
        follow_ups_join = "JOIN"

    sql = sql.format(follow_ups_join, search, offset, limit)

    try:
        rows = exec_steady(sql)
    except EmptySetError:
        return []

    entities = []
    for row in rows:
        entities.append(dict(row))

    return entities


def paged_with_follow_ups_count(search_params=None, empty_follow_ups=True):
    """Returns the number of records, for use with the pagination"""
    sql = """
    SELECT count(DISTINCT projects.id)::int AS total
    FROM projects
    JOIN contracts ON contracts.id = projects.contract
    {} follow_ups ON follow_ups.project = projects.id
         AND follow_ups.blocked = false
    WHERE projects.blocked = false {}
    """

    search = _setup_search_criteria(search_params, joint=False)
    if len(search) > 0:
        search = " AND " + search

    if empty_follow_ups:
        follow_ups_join = "LEFT JOIN"
    else:
        follow_ups_join = "JOIN"

    sql = sql.format(follow_ups_join, search)

    try:
        rows = exec_steady(sql)
    except EmptySetError:
        return 0

    # For this case we are just expecting one row
    if len(rows) == 0:
        raise NoResultFound("Just expecting one total as a result")
    elif len(rows) > 1:
        raise MultipleResultsFound("Just expecting one row as a result")

    return rows.pop()["total"]


def create(**kwargs):
    """Creates a project entity"""
    kwargs["id"] = 0
    return _alter_project(**kwargs)


def edit(**kwargs):
    """Edits the allowed properties of a project entity"""
    return _alter_project(**kwargs)


def block(project_id):
    """Logical deletion of a project entity"""
    delete_entity("projects", project_id)


def find(project_id):
    """Find a project as per id"""
    return find_entity("projects", project_id)


def count(search_params=None):
    """Number of non logical deleted projects"""
    return count_entities("projects", search_params)


def paged(offset, limit=10, order_by="id", order="asc", search_params=None):
    return page_entities("projects", offset, limit, order_by, order, search_params)


def count_by_status(department_id=None):
    sql = """
    SELECT stage_id as id, stage, count(*) FROM (
        SELECT DISTINCT ON (projects.id)
          projects.id AS Project,
          projects.department,
          check_stages.id AS stage_id,
          check_stages.title AS stage,
          follow_ups.check_date
        FROM projects
        JOIN follow_ups ON follow_ups.project = projects.id
             AND follow_ups.blocked = false
        JOIN check_stages on follow_ups.check_stage = check_stages.id
        WHERE projects.blocked = false
        ORDER BY projects.id, follow_ups.check_date DESC
    ) AS tmp
    {}
    GROUP BY stage_id, stage
    """

    if department_id:
        sql = sql.format(f"WHERE department = {department_id}")
    else:
        sql = sql.format("")

    try:
        rows = exec_steady(sql)
    except EmptySetError:
        return []

    entities = []
    for row in rows:
        entities.append(dict(row))

    return entities
