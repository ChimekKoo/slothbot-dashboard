DEBUG = True  # It must be False in production environment.

BASE_URL = "http://localhost:5000"  # Base url without ending slash

CRED_FILE_NAME = "cred.json"  # Credentials file name

# Get credentials from CRED_FILE_NAME file or from environment variables.
# CRED_OR_ENVIRON = "cred"  # Get from file
# CRED_OR_ENVIRON = "environ"  # Get from environment variables
CRED_OR_ENVIRON = "cred"
