import os
import subprocess


def generate_ssl_certificate(click):
    path = "bin/server.pem"
    if os.path.exists(path):
        return

    try:
        subprocess.run(["openssl", "genrsa", "-out", "server.key", "2048"])
        subprocess.run(
            [
                "openssl",
                "req",
                "-new",
                "-key",
                "server.key",
                "-out",
                "server.csr",
                "-subj",
                "/CN=localhost",
            ]
        )
        subprocess.run(
            [
                "openssl",
                "x509",
                "-req",
                "-days",
                "365",
                "-in",
                "server.csr",
                "-signkey",
                "server.key",
                "-out",
                "server.crt",
            ]
        )

        click.echo("- Generating the SSL certificate ...")

        with open(path, "wb") as pem_file:
            key_content = open("server.key", "rb").read()
            crt_content = open("server.crt", "rb").read()
            pem_file.write(key_content)
            pem_file.write(crt_content)

    except Exception:
        raise
    finally:
        os.remove("server.key")
        os.remove("server.csr")
        os.remove("server.crt")

    click.echo("- SSL certificate generated successfully.")
