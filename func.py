import paramiko
import json
from fdk import response

SFTP_HOST = "test.rebex.net"
SFTP_PORT = 22
SFTP_USERNAME = "demo"
SFTP_PASSWORD = "password"

def handler(ctx, data=None):
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # List files in home directory
        files = sftp.listdir()

        sftp.close()
        transport.close()

        return response.Response(
            ctx, response_data=json.dumps({"files": files}),
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        return response.Response(
            ctx, response_data=json.dumps({"error": str(e)}),
            headers={"Content-Type": "application/json"}
        )