import os

from modules import docker
from iapyc.core import Host, operation
from iapyc.fs import DirectoryState, directory
from iapyc.template import template


@operation
def setup(
    host: Host,
    base_dir: str,
    webui_addr: str = "9898",
    data_dir: str = None,
    container_name: str = "PeerBanHelper",
):
    directory(path=base_dir, state=DirectoryState.EXISTS)

    this_dir = os.path.dirname(__file__)
    template(
        local_template_path=os.path.join(this_dir, "docker-compose.yml"),
        remote_dest_path=base_dir,
        template_vars={
            "webui_addr": webui_addr,
            "container_name": container_name,
            "data_dir": data_dir,
        },
    )

    docker.compose_up(path=base_dir)
