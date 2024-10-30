import json
import os.path

import requests

from src.consts import DOFUS_PATH


BASE_CONFIG_URL = "https://dofus2.cdn.ankama.com/config/beta_windows.json"

CUSTOM_CONFIG_PATH = os.path.join(DOFUS_PATH, "local_config.json")
CUSTOM_CONFIG_YML_PATH = f"file:///{CUSTOM_CONFIG_PATH}".replace("\\", "/")


def get_base_config():
    response = requests.get(BASE_CONFIG_URL)
    return response.json()


def put_custom_config_url():
    datas = get_base_config()
    datas["connectionHosts"] = ["Beta:localhost:5555"]

    with open(CUSTOM_CONFIG_PATH, "w+") as file:
        json.dump(datas, file)

    with open(os.path.join(DOFUS_PATH, "zaap.yml"), "r+") as file:
        content = file.read()
    with open(os.path.join(DOFUS_PATH, "zaap.yml"), "w+") as file:
        content = content.replace(BASE_CONFIG_URL, CUSTOM_CONFIG_YML_PATH)
        file.write(content)


def put_old_config_url():
    with open(os.path.join(DOFUS_PATH, "zaap.yml"), "r+") as file:
        content = file.read()
    with open(os.path.join(DOFUS_PATH, "zaap.yml"), "w+") as file:
        content = content.replace(CUSTOM_CONFIG_YML_PATH, BASE_CONFIG_URL)
        file.write(content)


if __name__ == "__main__":
    # This is not rly good bc it need to close & reopen ankama launcher
    put_custom_config_url()
