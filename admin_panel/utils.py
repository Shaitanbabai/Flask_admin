import os
from pathlib import Path

def create_instance_folder(app):
    instance_path = Path(app.root_path) / 'instance'
    instance_path.mkdir(parents=True, exist_ok=True)