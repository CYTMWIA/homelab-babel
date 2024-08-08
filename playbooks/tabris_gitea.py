from modules.apps import gitea
from iapyc.core import host, Host

h: Host = host("tabris")
with h:
    gitea.setup(base_dir="/srv/gitea")
