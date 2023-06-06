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
        cmd = f"{self.openvpn_path}/{server_name}/easy-rsa/easyrsa --pki-dir={self.openvpn_path}/{server_name}/easy-rsa/pki --days={cert_expiration} --batch --req-cn={cert_name} build-client-full {cert_name} nopass"
        return self.cmd_exec(cmd)

    def revoke_cert(self, server_name, cert_name):
        cmd = f"{self.openvpn_path}/{server_name}/easy-rsa/easyrsa --pki-dir={self.openvpn_path}/{server_name}/easy-rsa/pki --batch revoke {cert_name}"
        return self.cmd_exec(cmd)
