from argparse import ArgumentParser
import sys
sys.path.append('/home/gabriel/PycharmProjects/desafioflex_ca_2')
from setup import cert_uc

parser = ArgumentParser(description='Gerenciamento dos certificados de VPN', epilog='Text at the bottom of help')
subparsers = parser.add_subparsers(dest='command')

create = subparsers.add_parser('create', help='create help')
create.add_argument('--server', '-s', dest='server', required=True, help='nome do servidor')
create.add_argument('--username', '-u', dest='username', required=True, help='usuario do certificado')
create.add_argument('--expiration', '-e', dest='expiration', required=True, type=int, help='tempo de expiração, em dias')

list_all = subparsers.add_parser('list-all', help='list-all help')
list_all.add_argument('--server', '-s', dest='server', required=True, help='nome do servidor')

args = parser.parse_args()


def list_all_certs(server):
    print(f"args.server: {server}")
    status, certs = cert_uc.get_all(None)

    if status == 200:
        for cert in certs:
            print(cert.json())
    else:
        print("Erro", status)


def create_cert(server, username, expiration):
    print(server, username, expiration)


if args.command == 'create':
    create_cert(args.server, args.username, args.expiration)
elif args.command == 'list-all':
    if args.server:
        list_all_certs(args.server)



