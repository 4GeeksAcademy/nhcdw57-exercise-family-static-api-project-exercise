"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_whole_family():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member_route(member_id):
    # This is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    if member == None:
        return f"Error: Could not find a family member with the id of: {member_id}", 400
    response_body = {"id": member["id"],
                     "first_name": member["first_name"],
                     "age": member["age"],
                     "lucky_numbers": member["lucky_numbers"]}
    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def post_member_route():
    # This is how you can use the Family datastructure by calling its methods
    response_body = request.json
    if (not "lucky_numbers" in response_body) or (not "age" in response_body) or (not "first_name" in response_body):
        return f"Error: invalid request body", 400
    new_member = {
        "id":jackson_family._generate_id(),
        "first_name":response_body["first_name"],
        "last_name":jackson_family.last_name,
        "age":response_body["age"],
        "lucky_numbers":response_body["lucky_numbers"]
    }
    member = jackson_family.add_member(new_member)
    return jsonify(member), 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member_route(member_id):
    # This is how you can use the Family datastructure by calling its methods
    member = jackson_family.delete_member(member_id)
    if member == None:
        return f"Error: Could not find a family member with the id of: {member_id}", 400
    response_body = {"done":True}
    return jsonify(response_body), 200

#added a put method cuz realistically, you'd probably want to be able to change family member information
@app.route('/members/<int:member_id>', methods=['PUT'])
def put_member_route(member_id):
    # This is how you can use the Family datastructure by calling its methods
    member = jackson_family.delete_member(member_id)
    if member == None:
        return f"Error: Could not find a family member with the id of: {member_id}", 400
    response_body = request.json
    if (not "lucky_numbers" in response_body) or (not "age" in response_body) or (not "first_name" in response_body):
        return f"Error: invalid request body", 400
    updated_member = {
        "id":member_id,
        "first_name":response_body["first_name"],
        "last_name":jackson_family.last_name,
        "age":response_body["age"],
        "lucky_numbers":response_body["lucky_numbers"]
    }
    member = jackson_family.add_member(updated_member)
    return jsonify(member), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
