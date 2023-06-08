from argparse import ArgumentParser
from infra import CertInfra
import re

parser = ArgumentParser(description='Gerenciamento dos certificados de VPN', epilog='Text at the bottom of help')
subparsers = parser.add_subparsers(dest='command')

create = subparsers.add_parser('create', help='create help')
create.add_argument('--server', '-s', dest='server', required=True, help='nome do servidor')
create.add_argument('--username', '-u', dest='username', required=True, help='usuario do certificado')
create.add_argument('--expiration', '-e', dest='expiration', required=True, type=int, help='tempo de expiração, em dias')

show = subparsers.add_parser('show', help='show help')
show.add_argument('--server', '-s', dest='server', required=True, help='nome do servidor')
show.add_argument('--all', '-a', dest='all', required=True, help='todos')
show.add_argument('--valids', '-v', dest='valids', required=True, help='válidos')
show.add_argument('--revokeds', '-r', dest='revokeds', required=True, help='revogados')

revoke = subparsers.add_parser('revoke', help='revoke help')
revoke.add_argument('--server', '-s', dest='server', required=True, help='nome do servidor')
revoke.add_argument('--username', '-u', dest='username', required=True, help='usuario do certificado')

args = parser.parse_args()


# def list_all_certs(server):
#     print(f"args.server: {server}")
#     status, certs = cert_uc.get_all(None)
#
#     if status == 200:
#         for cert in certs:
#             print(cert.json())
#     else:
#         print("Erro", status)


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


if args.command == 'create':
    create_cert(args.server, args.username, args.expiration)
elif args.command == 'revoke':
    revoke_cert(args.server, args.username)
# elif args.command == 'list-all':
#     if args.server:
#         list_all_certs(args.server)



