import os

from fabric import Connection

from .path import ls
from .vault import FileSecret

from ansible.parsing.yaml.loader import AnsibleLoader

YAML_EXTS = [".yaml", ".yml"]


def _load_yaml(path: str, file_name=None, vault_secrets=None):
    # Copy from: ansible/parsing/utils/yaml.py (_safe_load)

    if vault_secrets is None:
        # 第一个 None 是随便填的，具体效果并不清楚（It just works）
        vault_secrets = [(None, FileSecret("vault-password"))]

    with open(path, "r", encoding="utf-8") as f:
        stream = f.read()

    loader = AnsibleLoader(stream, file_name, vault_secrets)

    try:
        return loader.get_single_data()
    finally:
        try:
            loader.dispose()
        except AttributeError:
            pass  # older versions of yaml don't have dispose function, ignore


class Group:
    def __init__(self, name: str, group_vars: dict) -> None:
        self.name = name
        self.vars = dict() if group_vars is None else group_vars

    def members(self):
        return self.vars.get("members", list())

    def get_var(self, name: str):
        v = self.vars.get(name, None)
        return v


class Host:
    def __init__(self, name: str, host_vars: dict, groups: list[Group]) -> None:
        self.name = name
        self.vars = host_vars
        self.groups = groups

        self._connection = None

    def connection(self) -> Connection:
        if self._connection is None:
            self._connection = Connection(
                host=self.get_var("ssh_hostname"),
                user=self.get_var("ssh_username"),
                config={
                    "sudo": {
                        "password": self.get_var("sudo_password"),
                    },
                },
            )
        return self._connection

    def get_var(self, name: str):
        v = self.vars.get(name, None)
        gi = iter(self.groups)
        while v is None:
            g = next(gi, None)
            if g is None:
                break
            v = g.get_var(name, None)
        return v

    def in_group(self, name: str):
        for g in self.groups:
            if g.name == name:
                return True
        return False


class Inventory:
    def __init__(self, dirname: str = "./inventory") -> None:
        self.inventory_dir = dirname
        self.groups_dir = os.path.join(self.inventory_dir, "groups")
        self.hosts_dir = os.path.join(self.inventory_dir, "hosts")

        self.groups = self.__read_all_groups()

    def __read_all_groups(self):
        groups: list[Group] = []

        group_paths = ls(self.groups_dir)
        for gp in group_paths:
            name, ext = os.path.splitext(gp)
            try:
                group_vars = _load_yaml(gp)
                groups.append(Group(name, group_vars))
            except Exception:
                print("Read group failed:", gp)

        return groups

    def find_groups_by_member(self, member: str):
        groups: list[Group] = []
        for g in self.groups:
            if member in g.members():
                groups.append(g)
        return groups

    def get_host(self, name: str):
        possible_filenames = [name + ext for ext in YAML_EXTS]

        host_path = None
        for fn in possible_filenames:
            check_path = os.path.join(self.hosts_dir, fn)
            if os.path.exists(check_path):
                host_path = check_path
                break
        if host_path is None:
            FileNotFoundError(f"Host not exists: {name}")

        host_vars = _load_yaml(host_path)
        host = Host(name, host_vars, self.find_groups_by_member(name))
        return host


INVENTORY = Inventory()


def host(name: str):
    return INVENTORY.get_host(name)
