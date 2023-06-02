from flask import request, jsonify
from app import app
from setup import group_uc


@app.route('/grupos', methods=['GET'])
def get_all_groups():
    print("### group / apis / get_all_groups")
    status, groups = group_uc.get_all()

    if status == 200:
        groups_list = []
        for group in groups:
            groups_list.append(group.json())
        return jsonify(groups_list), status

    return jsonify({'message': 'unknown error'}), status


@app.route('/grupos', methods=['POST'])
def create_group():
    print("### group / apis / create_group")

    status, group_ent = group_uc.create(request.json)
    if status == 200:
        return jsonify(group_ent.json()), status
    elif status == 400:
        return jsonify(group_ent), status

    return jsonify({'message': 'username already exists.'}), status


@app.route('/grupos/<int:group_id>', methods=['GET'])
def get_group_by_id(group_id):
    print("### group / apis / get_group_by_id")
    status, group_ent = group_uc.get_by_id(group_id)

    if status == 200:
        return jsonify(group_ent.json()), status

    return jsonify({'message': 'group not found'}), status


@app.route('/grupos/<int:group_id>', methods=['DELETE'])
def delete(group_id):
    print("### group / apis / delete")
    status, group_ent = group_uc.delete(group_id)
    if status == 200:
        return jsonify({'message': 'group deleted'}), 200

    return jsonify({'message': 'group not found'}), 404


@app.route('/grupos/<int:group_id>', methods=['PUT'])
def update_group(group_id):
    print("### group / apis / update")
    status, group_ent = group_uc.update(group_id, request.json)
    if status == 200:
        return jsonify(group_ent.json()), status
    elif status == 400:
        return jsonify(group_ent), status
    elif status == 404:
        return jsonify({'message': group_ent}), status

    return jsonify({'message': 'unknown error'}), status
