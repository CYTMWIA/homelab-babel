import os

from modules import docker
from modules.core import Host, operation
from modules.fs import DirectoryState, directory
from modules.template import template


@operation
def setup(
    host: Host,
    base_dir: str,
    webui_addr: str = "8080",
    config_dir: str = None,
    download_dir: str = None,
    watch_dir: str = None,
    container_name: str = "qbittorrent",
):
    directory(path=base_dir, state=DirectoryState.EXISTS)

    this_dir = os.path.dirname(__file__)
    template(
        local_template_path=os.path.join(this_dir, "docker-compose.yml"),
        remote_dest_path=base_dir,
        template_vars={
            "webui_addr": webui_addr,
            "dir_config": config_dir,
            "dir_downloads": download_dir,
            "dir_watch": watch_dir,
            "container_name": container_name,
        },
    )
    docker.compose_up(path=base_dir)

    logs: str = docker.logs(container=container_name)
    webui_logs = filter(lambda line: "webui" in line.lower(), logs.splitlines())
    print("\n".join(webui_logs))
