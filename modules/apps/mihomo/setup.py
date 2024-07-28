import requests
from yaml import dump as _dump
from yaml import load as _load

from modules.core import Host, operation
from modules.package_manager import yay
from modules.systemd import ServiceState, service
from modules import fs

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


def yaml_loads(s: str):
    return _load(s, Loader=Loader)


def yaml_dumps(data: any):
    return _dump(data, Dumper=Dumper, allow_unicode=True)


def fetch_yaml(url: str) -> dict:
    resp = requests.get(url)
    resp.raise_for_status()
    return yaml_loads(resp.content.decode())


MIHOMO_CFG_PATH = "/etc/mihomo/config.yaml"


@operation
def setup(
    host: Host,
    sub_url: str | None = None,
    overwrite_cfg: dict | None = None,
):
    # TODO: 冲突配置检查（多次 setup 且使用了不同的参数）

    if overwrite_cfg is None:
        overwrite_cfg = {}

    # Search "mihomo" in AUR
    # https://aur.archlinux.org/packages?K=mihomo
    yay.install(packages=["mihomo-bin", "wget"])

    if sub_url is None:
        sub_url = host.get_var("mihomo_sub_url")
    if sub_url is None:
        return

    if len(overwrite_cfg) == 0:
        host.sudo(f"wget {sub_url} -O {MIHOMO_CFG_PATH}")
    else:
        cfg = fetch_yaml(sub_url)
        cfg.update(overwrite_cfg)
        fs.file(
            path=MIHOMO_CFG_PATH,
            content=yaml_dumps(cfg),
        )

    service(
        service="mihomo.service",
        state=ServiceState.ENABLE | ServiceState.RESTART,
    )
