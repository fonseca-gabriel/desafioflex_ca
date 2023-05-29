from flask import request, jsonify, make_response
from app import app
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
    print("### group / apis / create_certificate")
    status, cert_ent = cert_uc.create(request.json)
    if status == 200:
        return jsonify(cert_ent.json()), status
    elif status == 400:
        return jsonify(cert_ent.json()), status

    return jsonify({'message': 'username already exists.'}), status


@app.route('/certificados/<int:cert_id>', methods=['GET'])
def get_certificate_by_id(cert_id):
    print("### group / apis / get_certificate_by_id")
    status, cert_ent = cert_uc.get_by_id(cert_id)

    if status == 200:
        return jsonify(cert_ent.json()), status

    return jsonify({'message': 'certificate not found'}), status


@app.route('/certificados/<int:cert_id>', methods=['DELETE'])
def delete_certificate(cert_id):
    status, cert = cert_uc.delete(cert_id)
    if status == 200:
        return make_response(jsonify({'message': 'certificate deleted'}), 200)

    return make_response(jsonify({'message': 'certificate not found'}), 404)


@app.route('/certificados/<int:cert_id>', methods=['PUT'])
def update_certificate(cert_id):
    print("### cert / apis / update")
    status, cert_ent = cert_uc.update(cert_id, request.json)
    if status == 200:
        return jsonify(cert_ent.json()), status
    elif status == 404:
        return cert_ent, 404

    return jsonify({'message': 'username already exists.'}), status


