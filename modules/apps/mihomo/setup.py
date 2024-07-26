from modules.core import Host, operation
from modules.package_manager import yay
from modules.systemd import service, ServiceState

MIHOMO_CFG_PATH = "/etc/mihomo/config.yaml"


@operation
def setup(host: Host, sub_url: str | None = None):
    # TODO: 冲突配置检查（多次 setup 且使用了不同的参数）

    # Search "mihomo" in AUR
    # https://aur.archlinux.org/packages?K=mihomo
    yay.install(packages=["mihomo-bin", "wget"])

    if sub_url is None:
        sub_url = host.get_var("mihomo_sub_url")
    if sub_url is None:
        return

    host.sudo(f"wget {sub_url} -O {MIHOMO_CFG_PATH}")

    service(
        service="mihomo.service",
        state=ServiceState.ENABLE | ServiceState.RESTART,
    )
