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
    http_proxy: None | str = None,
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
            "http_proxy": http_proxy,
        },
    )
    docker.compose_up(path=base_dir)


@operation
def setup_runner(
    host: Host,
    base_dir: str,
    instance_url: str,
    registration_token: str,
    runner_name: str,
):
    base_dir = base_dir.removesuffix("/")

    directory(path=base_dir, state=DirectoryState.EXISTS)
    docker.compose_down(path=base_dir)

    this_dir = os.path.dirname(__file__)
    template(
        local_template_path=os.path.join(this_dir, "runner/config.yaml"),
        remote_dest_path=base_dir,
        template_vars={},
    )
    template(
        local_template_path=os.path.join(this_dir, "runner/docker-compose.yml"),
        remote_dest_path=base_dir,
        template_vars={
            "base_dir": base_dir,
            "instance_url": instance_url,
            "registration_token": registration_token,
            "runner_name": runner_name,
        },
    )

    docker.compose_up(path=base_dir)
