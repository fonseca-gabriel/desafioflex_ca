from argparse import ArgumentParser
from infra import CertInfra
import re

parser = ArgumentParser(description='Gerenciamento dos certificados de VPN', epilog='Text at the bottom of help')
subparsers = parser.add_subparsers(dest='command')

create = subparsers.add_parser('create', help='create help')
create.add_argument('--server', '-s', dest='server', required=True, help='nome do servidor')
create.add_argument('--username', '-u', dest='username', required=True, help='usuario do certificado')
create.add_argument('--expiration', '-e', dest='expiration', required=True, type=int, help='tempo de expiração, em dias')

revoke = subparsers.add_parser('revoke', help='revoke help')
revoke.add_argument('--server', '-s', dest='server', required=True, help='nome do servidor')
revoke.add_argument('--username', '-u', dest='username', required=True, help='usuario do certificado')

show = subparsers.add_parser('show', help='show help')
show.add_argument('--server', '-s', dest='server', required=True, help='nome do servidor')
show.add_argument('--type', '-t', dest='type', choices=['all', 'valid', 'revoked'], required=True, help='tipo')

args = parser.parse_args()


def create_cert(server, username, expiration):

    pattern = r'^[a-zA-Z0-9]+$'
    if not re.match(pattern, username):
        return print("the username must only contain alphanumeric characters")

    if len(username) > 30:
        return print('the username must not exceed 30 characters')

    # existing_certificate = Certificate.query.filter_by(username=username).first()
    # if existing_certificate:
    #     return make_response(jsonify({'message': 'username already exists.'}), 400)

    if isinstance(expiration, int):
        if expiration > 3650 or expiration < 10:
            return print('the expiration field must be an integer between 10 and 3650')
    else:
        return print('the expiration field must be an integer')

    cert = CertInfra()
    status, returncode, cmd_stdout = cert.create_cert(server_name='server', cert_name=username, cert_expiration=expiration)
    if status:
        return print(f"Certificado {username} criado com sucesso.")
    return print(f"Erro ao criar o certificado (exit code: {returncode}):\n{cmd_stdout}")


def revoke_cert(server, username):
    cert = CertInfra()
    status, returncode, cmd_stdout = cert.revoke_cert(server_name='server', cert_name=username)

    if status:
        return print(f"Certificado {username} revogado com sucesso.")
    return print(f"Erro ao revogar o certificado (exit code: {returncode}):\n{cmd_stdout}")


def print_certs(certs):
    print("status\tdate_expiration\tdate_expirated\tserial\tname")
    for cert in certs:
        status = None
        if cert.get('status') == 'V':
            status = 'Válido'
        elif cert.get('status') == 'R':
            status = 'Revogado'
        print(status + '\t', end='')
        print(cert.get('date_expiration') + '\t', end='')
        print(cert.get('date_expirated') + '\t', end='')
        print(cert.get('serial') + '\t', end='')
        print(cert.get('name') + '\t', end='\n')


def show_certs(server, type):
    index_file = f"{CertInfra.openvpn_path}/{server}/easy-rsa/pki/index.txt"

    with open(index_file) as f:
        lines = f.readlines()

    valid_certs = []
    revoked_certs = []
    all_certs = []

    for line in lines:
        splited = line.split('\t')
        cert_dict = {
            "status": splited[0],
            "date_expiration": splited[1],
            "date_expirated": splited[2],
            "serial": splited[3],
            "name": splited[5][4:-1],
        }
        all_certs.append(cert_dict)
        if splited[0] == 'V':
            valid_certs.append(cert_dict)
        elif splited[0] == 'R':
            revoked_certs.append(cert_dict)

    if type == 'all':
        return print_certs(all_certs)
    elif type == 'valid':
        return print_certs(valid_certs)
    elif type == 'revoked':
        return print_certs(revoked_certs)


if args.command == 'create':
    create_cert(args.server, args.username, args.expiration)
elif args.command == 'revoke':
    revoke_cert(args.server, args.username)
elif args.command == 'show':
    show_certs(args.server, args.type)



