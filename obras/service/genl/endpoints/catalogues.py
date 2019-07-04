from flask_restplus import Resource

from dal.helper import exec_steady
from genl.restplus import api
from misc.helperpg import EmptySetError

ns = api.namespace("catalogues", description="Read-only catalogues of data")


def _get_100_entities(table_name):
    offset = 0
    limit = 100

    sql = """
    SELECT id, title, description
    FROM {}
    ORDER BY id ASC
    OFFSET {} LIMIT {};
    """.format(
        table_name, offset, limit
    )

    try:
        rows = exec_steady(sql)
    except EmptySetError:
        return []

    entities = []
    for row in rows:
        entities.append(dict(row))

    return entities


@ns.route("/delivery_stages")
class DeliveryStagesCollection(Resource):
    def get(self):
        return _get_100_entities("delivery_stages")


@ns.route("/categories")
class CategoriesCollection(Resource):
    def get(self):
        return _get_100_entities("categories")


@ns.route("/departments")
class DepartmentsCollection(Resource):
    def get(self):
        return _get_100_entities("departments")


@ns.route("/check_stages")
class CheckStagesCollection(Resource):
    def get(self):
        return _get_100_entities("check_stages")


@ns.route("/adjudications")
class AdjudicationsCollection(Resource):
    def get(self):
        return _get_100_entities("adjudications")


@ns.route("/fundings")
class FundingsCollection(Resource):
    def get(self):
        return _get_100_entities("fundings")
