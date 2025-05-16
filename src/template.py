import json

from typing import List
from pathlib import Path

class Route:
    """
    A route object.

    Args:
        name (str): the name of the route.
        path (str): the path of the route.
        controller_path (str): the path to the controller module.
        authed (bool): whether the route is authed.
    """
    def __init__(self, name: str, path: str, controller: str, authed: bool = True):
        self.name = name
        self.path = path
        self.controller = controller
        self.authed = authed

class Template:
    """
    A route object.

    Args:
        name (str): the name of the route.
        controller_path (str): the path to the controller module.
    """
    def __init__(self, origins: List[str], routes: List[Route]):
        self.origins = origins
        self.routes = routes

def load() -> Template:
    """
    Load template.json configuration file.
    
    Returns 
        Template: The entire template configuration.
    """
    template_file = Path(__file__).parent / "../template.json"
    with open(template_file) as f:
        template = json.load(f)

        routes = [Route(route["name"], route["path"], route["controller"], route["authed"]) for route in template["routes"]]
        origins = template["origins"]

        return Template(origins, routes)