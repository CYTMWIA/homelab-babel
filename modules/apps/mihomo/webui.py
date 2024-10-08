import os

from iapyc.core import Host, operation
from iapyc.fs import DirectoryState, directory
from iapyc.template import template

from modules import docker


@operation
def setup_metacubexd(
    host: Host,
    base_dir: str,
    webui_addr: str = "10091",
    container_name: str = "metacubexd",
):
    # MetaCubeX/metacubexd
    # https://github.com/MetaCubeX/metacubexd

    directory(path=base_dir, state=DirectoryState.EXISTS)

    this_dir = os.path.dirname(__file__)
    template(
        local_template_path=os.path.join(this_dir, "metacubexd-compose.yml"),
        remote_dest_path=os.path.join(base_dir, "docker-compose.yml"),
        template_vars={
            "container_name": container_name,
            "webui_addr": webui_addr,
        },
    )

    docker.compose_up(path=base_dir)
