import os
import json
import base64
import logging
import firebase_admin
from firebase_admin import credentials, storage
from typing import Optional

logger = logging.getLogger(__name__)

class FirebaseClient:
    """
    Firebase Storage client with resilient fallback for local/offline environments.
    Reads dynamic credentials from Base64 environment variable if present.
    """
    
    _initialized = False
    _bucket = None

    @classmethod
    def initialize(cls):
        """Lazy initialization logic for the singleton client."""
        if cls._initialized:
            return

        b64_creds = os.getenv("FIREBASE_CREDENTIALS_B64")
        bucket_name = os.getenv("FIREBASE_BUCKET", "powershoring-analytics.appspot.com")

        if not b64_creds:
            logger.warning("⚠️ FIREBASE_CREDENTIALS_B64 not set. Operating in Mock Mode.")
            cls._initialized = True
            return

        try:
            # Decode the service account JSON
            cred_dict = json.loads(base64.b64decode(b64_creds).decode('utf-8'))
            cred = credentials.Certificate(cred_dict)
            
            # Initialize app only if not already initialized
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred, {
                    'storageBucket': bucket_name
                })
            
            cls._bucket = storage.bucket()
            logger.info(f"✅ Firebase Client initialized with bucket: {bucket_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Firebase client: {str(e)}")
            # Fallback ensures initialization flag is true so we don't loop retry crashes
        
        cls._initialized = True

    @classmethod
    def upload_bytes(cls, file_bytes: bytes, destination_blob_name: str) -> Optional[str]:
        """
        Uploads bytes to the bucket storage.
        Returns the public/access URI or None if failed/mock.
        """
        cls.initialize()
        
        if not cls._bucket:
            logger.warning(f"[MOCK] Skipping cloud upload for {destination_blob_name} (No Bucket)")
            return f"mock-gcs://{destination_blob_name}"

        try:
            blob = cls._bucket.blob(destination_blob_name)
            blob.upload_from_string(file_bytes)
            # Make viewable/downloadable
            blob.make_public()
            logger.info(f"✨ Successfully uploaded {destination_blob_name} to Firebase Storage.")
            return blob.public_url
        except Exception as e:
            logger.error(f"❌ Firebase Upload Error: {str(e)}")
            return None

def get_firebase_client() -> FirebaseClient:
    return FirebaseClient
