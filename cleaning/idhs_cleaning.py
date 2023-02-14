import json
import re

def clean():
    """
    """

with open("../webscraping/idhs.json", "r") as fj:
    data = json.load(fj)
    for office in data:
        office["Address"] = office["Address"].strip()
        office["Contact"] = office["Contact"].strip()
        office["Contact"] = re.sub(r"[\t]", "", office["Contact"])
        office["Contact"] = re.sub(r"[\n+]", " ", office["Contact"])


with open("cleaned_idhs.json", "w") as fj2:
    json.dump(data, fj2, indent=1)