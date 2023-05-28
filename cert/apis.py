from flask import request, jsonify, make_response
from app import app, db
from setup import cert_uc


@app.route('/certificados', methods=['GET'])
def get_all_certs():
    print("### cert / apis / get_all_certs")
    modifiers = {}
    modifiers["sort_param"] = request.args.get('sort')
    modifiers["filter_name_param"] = request.args.get('name')
    modifiers["filter_username_param"] = request.args.get('username')

    status, certs = cert_uc.get_all(modifiers)

    if status == 200:
        certs_list = []
        for cert in certs:
            certs_list.append(cert.json())
        return jsonify(certs_list), status

    return "Erro", status


@app.route('/certificados', methods=['POST'])
def create_certificate():
    status, cert = cert_uc.create(request.json)
    if status == 200:
        return jsonify(cert), status
    elif status == 400:
        return jsonify({"message": cert}), status

    return jsonify({'message': 'username already exists.'}), status


@app.route('/certificados/<int:cert_id>', methods=['GET'])
def get_certificate(cert_id):
    status, cert = cert_uc.get_by_id(cert_id)

    if status == 200:
        return jsonify({"id": cert.id, "username": cert.username}), status

    return jsonify({'message': 'certificate not found'}), status


@app.route('/certificados/<int:cert_id>', methods=['DELETE'])
def delete_certificate(cert_id):
    status, cert = cert_uc.delete(cert_id)
    if status == 200:
        return make_response(jsonify({'message': 'certificate deleted'}), 200)

    return make_response(jsonify({'message': 'certificate not found'}), 404)


@app.route('/certificados/<int:cert_id>', methods=['PUT'])
def update_certificate(cert_id):

    status, cert = cert_uc.update(cert_id, request.json)
    if status == 200:
        return jsonify({"id": cert["id"], "username": cert["username"]}), status

    return jsonify({'message': 'username already exists.'}), status


