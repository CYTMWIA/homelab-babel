import os

from iapyc import fs
from iapyc.core import Host, operation
from iapyc.package_manager import pacman
from iapyc.systemd import ServiceState, service
from iapyc.template import template


@operation
def installed(host: Host):
    which = host.run("which docker", raise_for_failure=False)
    return bool(len(which.stdout.strip()))


ALREADY_SETUP = set()


@operation
def setup(host: Host):
    if host.name in ALREADY_SETUP:
        return
    ALREADY_SETUP.add(host.name)

    if not installed():
        pacman.install(packages=["docker", "docker-compose"])
        service(
            service="docker.service",
            state=ServiceState.ENABLE | ServiceState.START,
        )

    docker_http_proxy = host.get_var("docker_http_proxy")
    if docker_http_proxy is not None:
        # TODO: 检查是否已设置代理
        print("Set proxy for docker:", docker_http_proxy)
        this_dir = os.path.dirname(__file__)
        fs.directory(path="/etc/docker/", state=fs.DirectoryState.EXISTS)
        template(
            local_template_path=os.path.join(this_dir, "daemon.json"),
            remote_dest_path="/etc/docker/daemon.json",
            template_vars={
                "docker_http_proxy": docker_http_proxy,
            },
        )
        service(
            service="docker.service",
            state=ServiceState.RESTART,
        )


@operation
def run(host: Host, image: str, name: str, args: None | list[str] = None):
    if args is None:
        args = []
    args = " ".join(args)

    # TODO: 实现 docker run


@operation
def compose_up(host: Host, path: str):
    setup()
    host.sudo(f"cd {path} && docker compose up -d")


@operation
def compose_down(host: Host, path: str, raise_for_failure=False):
    setup()
    host.sudo(f"cd {path} && docker compose down", raise_for_failure=raise_for_failure)


@operation
def logs(host: Host, container: str):
    return host.sudo(f"docker logs {container}").stdout
