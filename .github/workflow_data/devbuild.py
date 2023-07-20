#!/usr/bin/env python
import nextcloud_client
import datetime as dt
import requests
import json
import os

dev_share = os.environ["NC_HOST"] + "s/sGHsQB94a9x5CRs/download?path=/&files={files}"

if __name__ == "__main__":
    with open(os.environ["GITHUB_EVENT_PATH"], "r") as f:
        event = json.load(f)

    client = nextcloud_client.Client(os.environ["NC_HOST"])
    client.login(os.environ["NC_USER"], os.environ["NC_PASS"])

    for file in (
        os.environ["ARTIFACT_TGZ"],
        os.environ["ARTIFACT_SDK"],
    ):
        path = f"XFW-Dev/{file}"
        # try:
        #     client.delete(path)
        # except Exception:
        #     pass
        client.put_file(path, file)

    requests.post(
        os.environ["BUILD_WEBHOOK"],
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={
            "content": None,
            "embeds": [
                {
                    "title": "Devbuild infos:",
                    "description": "",
                    "url": "",
                    "color": 16734443,
                    "fields": [
                        {
                            "name": "Changes since last commit:",
                            "value": f"[Compare {event['before']} to {event['after']}]({event['compare']})"
                        },
                        {
                            "name": "Changes since last release:",
                            "value": f"[Compare release to {event['after']}]({event['compare'].replace(event['before'], 'main')})"
                        },
                        {
                            "name": "Firmware download:",
                            "value": f"- [Download SDK for development]({dev_share.format(files=os.environ['ARTIFACT_SDK'])})\n- [Download Firmware TGZ]({dev_share.format(files=os.environ['ARTIFACT_TGZ'])})"
                        }
                    ],
                    "author": {
                        "name": "Build Succeeded!",
                        "icon_url": "https://cdn.discordapp.com/emojis/1080005692485795930.png"
                    },
                    "footer": {
                        "text": "Build go brrrr",
                        "icon_url": "https://cdn.discordapp.com/emojis/1059798228725403719.png"
                    },
                    "timestamp": dt.datetime.utcnow().isoformat()
                }
            ],
        },
    )