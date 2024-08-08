import os

from modules import docker
from iapyc.core import Host, operation
from iapyc.fs import DirectoryState, directory
from iapyc.template import template

# https://docs.gitea.com/installation/install-with-docker


@operation
def setup(
    host: Host,
    base_dir: str,
    http_port: str = "3000",
    ssh_port: str = "2222",
    dir_data: None | str = None,
):
    directory(path=base_dir, state=DirectoryState.EXISTS)
    docker.compose_down(path=base_dir)

    if dir_data is None:
        dir_data = os.path.join(base_dir, "data")

    this_dir = os.path.dirname(__file__)
    template(
        local_template_path=os.path.join(this_dir, "docker-compose.yml"),
        remote_dest_path=base_dir,
        template_vars={
            "http_port": http_port,
            "ssh_port": ssh_port,
            "dir_data": dir_data,
        },
    )
    docker.compose_up(path=base_dir)
