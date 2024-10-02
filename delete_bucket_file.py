from google.cloud import storage
import os

class GCSHandler1:
    """A class to handle Google Cloud Storage operations."""

    def __init__(self):
        """Initialize the GCSHandler and check for credentials."""
        self.cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not self.cred_path:
            raise EnvironmentError("Environment variable for credentials (GOOGLE_APPLICATION_CREDENTIALS) is not set.")
        print(f"Using credentials from: {self.cred_path}")

    def delete_blob(self, bucket_name, blob_name):
        """Deletes a blob (file) from the specified bucket."""
        try:
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()  # Delete the specified blob
            print(f"Blob '{blob_name}' deleted from bucket '{bucket_name}'.")
        
        except Exception as e:
            print(f"An error occurred while deleting the blob: {e}")

    def delete_bucket(self, bucket_name):
        """Deletes the specified bucket."""
        try:
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            bucket.delete(force=True)  # Force delete to remove non-empty bucket
            print(f"Bucket '{bucket_name}' deleted successfully.")
        
        except Exception as e:
            print(f"An error occurred while deleting the bucket: {e}")
