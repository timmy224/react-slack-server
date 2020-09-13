from flask import request, jsonify
import json
from .. import main
from ... import db
from ...models.OrgMember import OrgMember, org_member_schema


# EXAMPLES
@main.route("/org/member/", methods=["GET"])
def get_org_members():
    """
    [GET] - grabs a org's org members from the DB and returns it as a JSON response (note that the OrgMember is a join of multiple tables - see OrgMember schema)
    Path: /org/member/?org_id
    Response Body: "org_members"
    DB tables: "users", "org_members", "roles"
    """
    org_id = request.args.get("org_id")
    response = {}
    if org_id is None:
        response["ERROR"] = "Missing org_id in route"
        return response
    org_members = db.session.query(OrgMember).filter_by(org_id=org_id).all()
    response["org_members"] = org_member_schema.dumps(org_members, many=True)
    return response

