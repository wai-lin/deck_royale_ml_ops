import firebase_admin
from firebase_admin import credentials, firestore
from ..get_envs import get_envs

envs = get_envs()
FIREBASE_SDK_JSON = envs["firebase_sdk_json"]

cred = credentials.Certificate(FIREBASE_SDK_JSON)
admin_app = firebase_admin.initialize_app(cred)
db = firestore.client()
