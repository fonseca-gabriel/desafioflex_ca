from subprocess import PIPE, Popen


class CertInfra:

    openvpn_path = "/etc/openvpn"

    def cmd_exec(self, cmd):
        with Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
            stdout, stderr = proc.communicate()
            cmd_stdout = stdout.decode().rstrip()

        if proc.returncode != 0:
            stderr = stderr.decode()
            error = f"Error running command '{cmd}'\n{stderr}"

            return False, proc.returncode, error

        return True, None, cmd_stdout

    def create_cert(self, server_name, cert_name, cert_expiration):
        # ./easyrsa --pki-dir=/etc/openvpn/server/easy-rsa/pki --days=60 --batch --req-cn=usuario15 build-client-full usuario15 nopass
        cmd = f"{self.openvpn_path}/{server_name}/easy-rsa/easyrsa --pki-dir={self.openvpn_path}/{server_name}/easy-rsa/pki --days={cert_expiration} --batch --req-cn={cert_name} build-client-full {cert_name} nopass"
        status, codereturn, message = self.cmd_exec(cmd)
        return status, codereturn, message

        # with Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
        #     stdout, stderr = proc.communicate()
        #     cmd_stdout = stdout.decode().rstrip()
        #
        # if proc.returncode != 0:
        #     stderr = stderr.decode()
        #     error = f"Error running command '{cmd}'\n{stderr}"
        #
        #     return False, proc.returncode, error
        #
        # return True, None, cmd_stdout

    def revoke_cert(self, server_name, cert_name):
        # ./easyrsa --batch revoke vpn_server
        cmd = f"{self.openvpn_path}/{server_name}/easy-rsa/easyrsa --pki-dir={self.openvpn_path}/{server_name}/easy-rsa/pki --batch revoke {cert_name}"
        with Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
            stdout, stderr = proc.communicate()
            cmd_stdout = stdout.decode().rstrip()

        if proc.returncode != 0:
            stderr = stderr.decode()
            error = f"Error running command '{cmd}'\n{stderr}"

            return False, proc.returncode, error

        return True, None, cmd_stdout
