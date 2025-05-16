import importlib

from fastapi import FastAPI
from typing import Any, List
from src.template import Route

def lazy_load_controller(module_path: str) -> Any:
    """
    Lazily load a controller from its module path.
    
    Args:
        module_path (str): the path to the controller module.
        
    Returns:
        Any: the controller object.
    """

    try:
        module = importlib.import_module(module_path)
        return getattr(module, "controller")
    except (ImportError, AttributeError) as e:
        print(f"Warning: Could not load controller for {module_path}: {e}")
        return None

def router(app: FastAPI, routes: List[Route]):
    """
    Register routes with lazy-loaded controllers.
    
    Args:
        app (FastAPI): the FastAPI app object.
    """
    print(routes)
    for route in routes:
        controller = lazy_load_controller('src.' + route.controller)
        if controller:
            controller(app, route)

