import io
import json
import logging
import paramiko
import oci

def handler(ctx, data):
    logging.getLogger().setLevel(logging.INFO)
    
    try:
        # Parse input data
        body = json.loads(data.getvalue()) if data else {}
        sftp_host = body.get("sftp_host", "test.rebex.net")
        sftp_port = body.get("sftp_port", 22)
        sftp_username = body.get("sftp_username", "demo")
        sftp_password = body.get("sftp_password", "password")
        remote_file = body.get("remote_file", "readme.txt")
        oci_namespace = body.get("oci_namespace", "idnienhx4e48")
        oci_bucket_name = body.get("oci_bucket_name", "bucket-shivalingam")
        oci_config_file = "~/.oci/config"
        oci_profile = "DEFAULT"

        # Step 1: Connect to SFTP and download file into memory
        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(username=sftp_username, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        with sftp.file(remote_file, 'rb') as f:
            file_data = f.read()
        
        sftp.close()
        transport.close()
        logging.info(f"File '{remote_file}' downloaded successfully from SFTP.")

        # Step 2: Upload to OCI Object Storage
        config = oci.config.from_file(oci_config_file, oci_profile)
        object_storage_client = oci.object_storage.ObjectStorageClient(config)
        
        object_storage_client.put_object(
            oci_namespace,
            oci_bucket_name,
            remote_file,
            io.BytesIO(file_data)
        )
        logging.info(f"File '{remote_file}' uploaded successfully to OCI Object Storage!")

        return {"status": "Success", "message": f"File '{remote_file}' processed."}
    
    except Exception as e:
        logging.error(f"Error: {e}")
        return {"status": "Error", "message": str(e)}