import requests
import json


def Nexeedpost(payload):
    # sending post request and saving response as response object
    url = "https://demo.bosch-nexeed.com/cpm/ppm/v3/measurement"

    headers = {
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(url, data=json.dumps(payload), headers=headers)

        pastebin_url = r.content

        # Response from Bosch URL
        if pastebin_url == "{}":
            print("Successfully Posted to Nexeed")
        else:
            print("URL Response: %s" % pastebin_url)

    except:
        print("Nexeed unreachable")

