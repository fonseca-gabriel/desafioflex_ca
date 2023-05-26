from flask import request, jsonify, make_response
from app import app, db
from setup import group_uc


@app.route('/grupos', methods=['GET'])
def list_groups():
    status, groups = group_uc.get_all()
    return jsonify(groups), status


@app.route('/grupos', methods=['POST'])
def create_group():
    status, group = group_uc.create(request.json)
    if status == 200:
        return jsonify(group), status
    elif status == 400:
        return jsonify({"message": group}), status

    return jsonify({'message': 'username already exists.'}), status


@app.route('/grupos/<int:group_id>', methods=['GET'])
def get_group(group_id):
    status, group = group_uc.get_by_id(group_id)

    if status == 200:
        return jsonify({"id": group.id, "username": group.username}), status

    return jsonify({'message': 'group not found'}), status


@app.route('/grupos/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    status, group = group_uc.delete(group_id)
    if status == 200:
        return make_response(jsonify({'message': 'group deleted'}), 200)

    return make_response(jsonify({'message': 'group not found'}), 404)


@app.route('/grupos/<int:group_id>', methods=['PUT'])
def update_group(group_id):

    status, group = group_uc.update(group_id, request.json)
    if status == 200:
        return jsonify({"id": group["id"], "username": group["username"]}), status

    return jsonify({'message': 'username already exists.'}), status


