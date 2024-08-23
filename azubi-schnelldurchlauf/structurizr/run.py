import base64
import re

import requests

pattern = (
    r"(?:systemLandscape|systemContext|container|component|filtered|dynamic|"
    r"deployment|custom|image|styles|theme|themes|branding|terminology|"
    r'properties)\s+\w+\s+"(\w+)"'
)

pattern1 = (
    r"^(.*(?:systemLandscape|systemContext|container|component|filtered|dynamic|"
    r"deployment|custom|image|styles|theme|themes|branding|terminology|"
    r'properties)\s+\w+\s+"(\w+)".*)$'
)


def render_structurizr_via_kroki(structurizr_code, return_type="svg"):
    skip: bool = False
    # Define the URL for the Kroki.io API
    # url = f"https://kroki.io/structurizr/{return_type}"
    url = "http://localhost:8000/structurizr/" + return_type

    views = structurizr_code.split("views {")
    views[0] = views[0] + "views {"
    view_keys = extract_view_keys(views[1])
    split = views[1].split("\n")

    i = 0
    for view_key in view_keys:
        txt = views[0]

        for entry in split:
            if view_key in entry:
                skip = False
            elif re.findall(pattern, entry):
                skip = True
            elif "}" in entry and skip:
                skip = False
                continue
            if skip:
                continue
            txt = txt + entry + "\n"

        # Prepare the payload
        payload = {"diagram_source": txt}

        # Send the request to Kroki.io
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            # Save the SVG content to a file
            with open(f"structurizr/diagram_{i}.{return_type}", "w") as file:
                file.write(response.text)
            print(f"Diagram saved as diagram_{i}.{return_type}")
            i = i + 1
        else:
            print(f"Failed to render diagram: {response.status_code} - {response.text}")


def extract_view_keys(structurizr_code):
    view_keys = re.findall(pattern1, structurizr_code, re.MULTILINE)

    ret = []
    for line in view_keys:
        ret.append(line[0])

    return ret


if __name__ == "__main__":
    # Read the Structurizr DSL code from the file
    with open("structurizr/structurizr.dsl") as file:
        structurizr_code = file.read()

    with open("structurizr/42clueLogo.png", "rb") as image_file:
        base64_logo_string = base64.b64encode(image_file.read()).decode("utf-8")

    structurizr_code_with_logo = structurizr_code.replace("42clue_logo", base64_logo_string)

    # Render diagrams for each view key
    render_structurizr_via_kroki(structurizr_code_with_logo)
