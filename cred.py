from os import environ
from json import loads as json_load
from yaml import load as yaml_load

from constants import CRED_FILE_OR_ENVIRON, CRED_FILE_NAME, CRED_FILE_TYPE


def get_cred():

    if CRED_FILE_OR_ENVIRON == "cred":

        with open(CRED_FILE_NAME, "r") as cred_file_obj:
            cred_raw = cred_file_obj.read()
            cred_file_obj.close()

        if CRED_FILE_TYPE == "json":
            cred = json_load(cred_raw)
            return cred
        elif CRED_FILE_TYPE == "yaml":
            cred = yaml_load(cred_raw)
            return cred
        else:
            raise ValueError("constants.CRED_FILE_TYPE is not 'json' or 'yaml'.")

    elif CRED_FILE_OR_ENVIRON == "environ":

        cred = {
            "smtp": {
                "host": environ.get("SMTP_HOST"),
                "port": environ.get("SMTP_PORT"),
                "login": environ.get("SMTP_LOGIN"),
                "password": environ.get("SMTP_PASSWORD")
            },
            "mongodb_url": environ.get("MONGODB_URL"),
            "secret_key": environ.get("SECRET_KEY")
        }
        return cred

    else:
        raise ValueError("constants.CRED_FILE_OR_ENVIRON is not 'cred' or 'environ'.")
