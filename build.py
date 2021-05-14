#!/usr/bin/python3

from os import getenv, makedirs, path
import requests
import shutil
import json
from typing import Dict
from subprocess import STDOUT, run, PIPE

DIST_FOLDER = getenv("DIST_FOLDER", "./dist")
BUILD_CONFIG = getenv("BUILD_CONFIG", "./build_config.json")
EXTENSION_CONFIG = getenv("EXTENSION_CONFIG", "./config.json")

# for runtime publishing
PUBLISH=getenv("PUBLISH", "True") == "True"
URL=getenv("URL", "http://localhost")
USERNAME=getenv("USERNAME", "admin")
PASSWORD=getenv("PASSWORD", "admin123123")


def main():
    with open(BUILD_CONFIG, "r") as fp:
        config = json.load(fp)

    shutil.rmtree(DIST_FOLDER, ignore_errors=True)
    makedirs(DIST_FOLDER, exist_ok=True)
    for module in config.get("modules", []):
        print(f"Building module {module['file']}", flush=True)

        # Build
        result = run([module["cmd"]], shell=True, stdout=PIPE, stderr=PIPE, cwd=module["context"], text=True)
        if (result.returncode != 0):
            print("Build failed")
            print(result.stdout, result.stderr)
            return 1

        # Copy artifacts
        shutil.copyfile(path.join(module["context"], module["artifact"]), path.join(DIST_FOLDER, module['file']))

    #Copy config
    shutil.copyfile(EXTENSION_CONFIG, path.join(DIST_FOLDER, "config.json"))

    print("Creating tar file")
    shutil.make_archive("extension", "gztar", DIST_FOLDER)
    shutil.move("extension.tar.gz", path.join(DIST_FOLDER, "extension.tar.gz"))

    if not PUBLISH:
        print("Done")
        return 0

    print(f"Publishing to the {URL}")
    with requests.session() as session:
        print("Requesting authorization")
        response = session.post(f"{URL}/usermanager/api/v1/auth/token", data={"username": USERNAME, "password": PASSWORD})
        
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            print(response.text)
            return 2

        token = response.json()["access_token"]
        session.headers = {"Authorization": f"Bearer {token}"}

        print("Sending extension update")
        with open(path.join(DIST_FOLDER, "extension.tar.gz"), "rb") as file:
            response = session.post(f"{URL}/modules/native/moduleloader/api/v1/extensionTar", files={"file": file})
            if (response.status_code == 200):
                print("Done")
            else:
                print(f"Bad status code on pushing extension {response.status_code}")
                print(response.text)
                return 3

if __name__ == "__main__":
    main()