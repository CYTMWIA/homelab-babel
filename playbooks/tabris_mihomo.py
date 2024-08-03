from modules.apps import mihomo
from modules.core import host, Host
from modules.fs import directory, DirectoryState

h: Host = host("tabris")
with h:
    mihomo.setup(
        overwrite_cfg={
            "allow-lan": True,
            "mixed-port": 7890,
            "external-controller": "0.0.0.0:9091",
        },
    )
    mihomo.setup_metacubexd(
        base_dir="/srv/metacubexd",
    )
