import base64
import hashlib
import re
import os


# Generate code verifier (43 characters string of letters and numbers url-safe base64 encoded)
def create_code_verifier():
    return re.sub("[^a-zA-Z0-9]+", "", base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8"))


# Generate code challenge (url-safe base64 encoded SHA256 hash of code verifier)
def create_code_challenge(code_verifier):
    return base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).decode("utf-8").replace("=", "")