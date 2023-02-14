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
        #office["Address"] = office["Address"].replace("\n",'')


with open("cleaned_idhs.json", "w") as fj2:
    json.dump(data, fj2, indent=1)