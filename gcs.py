from google.cloud import storage
import os

class GCSHandler:
    """A class to handle Google Cloud Storage operations."""

    def __init__(self):
        """Initialize the GCSHandler and check for credentials."""
        self.cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not self.cred_path:
            raise EnvironmentError("Environment variable for credentials (GOOGLE_APPLICATION_CREDENTIALS) is not set.")
        print(f"Using credentials from: {self.cred_path}")
        
    def upload_blob(self, bucket_name, source_file_name, destination_file_name):
        """Uploads a file to the specified bucket."""
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_file_name)

            # Upload the file to the specified destination
            blob.upload_from_filename(source_file_name)
            return f"{source_file_name} uploaded to {destination_file_name} in bucket {bucket_name}."
        
        except Exception as e:
            return f"An error occurred while uploading the file: {e}"

            
    def delete_blob(self, bucket_name, blob_name):
        """Deletes a blob (file) from the specified bucket."""
        try:
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            
            # Delete the specified blob
            blob.delete()  
            
            return f"Blob '{blob_name}' deleted from bucket '{bucket_name}'."  # Return a success message

        except Exception as e:
            return f"An error occurred while deleting the blob: {e}"  # Return the error message

    def create_bucket(self, bucket_name):
        """Creates a new bucket in the project."""
        try:
            # Initialize a storage client
            client = storage.Client()
            
            # Check if the bucket already exists
            if not client.lookup_bucket(bucket_name):
                # Create the bucket
                new_bucket = client.create_bucket(bucket_name)
                return f"Bucket {new_bucket.name} created successfully."
            else:
                return f"Bucket {bucket_name} already exists."
        
        except Exception as e:
            return f"An error occurred while creating the bucket: {e}"

    def delete_bucket(self, bucket_name):
        """Deletes an existing bucket in the project."""
        try:
            # Initialize a storage client
            client = storage.Client()
            
            # Get the bucket
            bucket = client.bucket(bucket_name)
            
            # Delete the bucket
            bucket.delete()
            return f"Bucket {bucket_name} deleted successfully."
        
        except Exception as e:
            return f"An error occurred while deleting the bucket: {e}"

    def list_buckets(self):
        """Lists all buckets in the project."""
        try:
            # Initialize a storage client
            client = storage.Client()
            
            # List all buckets
            buckets = client.list_buckets()
            bucket_list = [bucket.name for bucket in buckets]
            if bucket_list:
                return f"Buckets in the project: {', '.join(bucket_list)}"
            else:
                return "No buckets found in the project."
        
        except Exception as e:
            return f"An error occurred while listing the buckets: {e}"

    def list_files_in_bucket(self, bucket_name):
        """Lists all files in the specified bucket."""
        try:
            # Initialize a storage client
            client = storage.Client()
            
            # Get the bucket
            bucket = client.bucket(bucket_name)
            
            # List all blobs (files) in the bucket
            blobs = bucket.list_blobs()
            
            file_list = [blob.name for blob in blobs]
            if file_list:
                return f"Files in bucket '{bucket_name}': {', '.join(file_list)}"
            else:
                return f"No files found in bucket '{bucket_name}'."
        
        except Exception as e:
            return f"An error occurred while listing the files in the bucket: {e}"
        
    
