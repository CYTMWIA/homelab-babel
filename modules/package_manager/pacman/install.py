from modules.core import Host, auto_host
from .setup import setup


@auto_host
def install(host: Host, packages: str | list[str]):
    setup()

    if isinstance(packages, str):
        packages = [packages]
    pkgs_s = " ".join(packages)
    host.sudo(f"pacman -Sy --noconfirm --needed {pkgs_s}")
