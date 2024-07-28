from modules.core import Host, operation
from enum import Enum, auto

import os


class DirectoryState(Enum):
    DELETED = auto()
    EMPTY = auto()
    EXISTS = auto()


@operation
def directory(
    host: Host,
    path: str,
    state: DirectoryState,
    owner: str | None = None,
    mode: str = "755",
):
    path = path.strip()
    if owner is None:
        owner = host.run("whoami").stdout.strip()

    if state == DirectoryState.DELETED:
        host.sudo(f"rm -rf {path}")
        return

    # 创建目录
    host.sudo(f"mkdir -m {mode} -p {path}")
    host.sudo(f"chown {owner} {path}")

    if state == DirectoryState.EXISTS:
        # do nothing
        return

    if state == DirectoryState.EMPTY:
        if not path.endswith("/"):
            path += "/"
        path += "*"
        host.sudo(f"rm -rf {path}")


@operation
def is_dir_exists(host: Host, path: str):
    ls_output = host.sudo(f"ls -l -L '{os.path.dirname(path)}'").stdout.splitlines()
    basename = os.path.basename(path)
    for line in ls_output:
        line = line.strip()
        if line.startswith("d") and line.endswith(basename):
            return True
    return False
