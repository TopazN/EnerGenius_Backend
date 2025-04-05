import os
import json
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app

load_dotenv()

firebase_creds = os.getenv("FIREBASE_CREDENTIALS")

if firebase_creds:
    fixed_creds = firebase_creds.encode().decode("unicode_escape")
    cred_dict = json.loads(fixed_creds)
    cred = credentials.Certificate(cred_dict)
    default_app = initialize_app(cred)
    print("✅ Firebase initialized successfully!")
else:
    print("❌ FIREBASE_CREDENTIALS not found in .env")
