from dataclasses import dataclass


class Container:
    id: str
    name: str
    status: str
    config_path: str
    container_id: str = None