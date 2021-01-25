DEBUG = True  # It must be False in production environment!

BASE_URL = "http://localhost:5000"  # Base url without ending slash

# Get credentials from CRED_FILE_NAME file or from environment variables.
CRED_FILE_OR_ENVIRON = "cred"  # "cred" for file or "environ" for environment variables.
CRED_FILE_NAME = "cred.json"  # Credentials file name
CRED_FILE_TYPE = "json"  # "json" or "yaml"
