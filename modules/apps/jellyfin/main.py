import os

from modules.apps import docker
from modules.core import Host, operation
from modules.fs import DirectoryState, directory
from modules.template import template


@operation
def setup(
    host: Host,
    base_dir: str,
    webui_addr: str = "8096",
    config_dir: str = None,
    media_dir: str = None,
    container_name: str = "jellyfin",
):
    directory(path=base_dir, state=DirectoryState.EXISTS)

    this_dir = os.path.dirname(__file__)
    template(
        local_template_path=os.path.join(this_dir, "docker-compose.yml"),
        remote_dest_path=base_dir,
        template_vars={
            "webui_addr": webui_addr,
            "dir_config": config_dir,
            "dir_media": media_dir,
            "container_name": container_name,
        },
    )
    docker.compose_up(path=base_dir)
