'''
Author: Betty
Date: 2/08/23
'''

import json
import re

def clean():
    """
    This function cleans the idhs.json file and saves the output into a file
    named cleaned_idhs.json
    """

with open("../webscraping/idhs.json", "r") as fj:
    data = json.load(fj)
    for office in data:
        office["Name"] = re.sub(r"[\s]$","", office["Name"])
        office["Address"] = office["Address"].strip()
        office["Address"] = re.sub(r"(\s{2,})", " ", office["Address"])
        office["Contact"] = office["Contact"].strip()
        office["Contact"] = re.sub(r"[\t]", "", office["Contact"])
        office["Contact"] = re.sub(r"[\n+]", " ", office["Contact"])


with open("cleaned_idhs.json", "w") as fj2:
    json.dump(data, fj2, indent=1)