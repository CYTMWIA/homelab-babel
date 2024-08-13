from modules.apps import gitea
from iapyc.core import host, Host

h: Host = host("server-la")
with h:
    gitea.setup_runner(
        base_dir="/srv/gitea_runner",
        instance_url="http://tabris:3000/",
        registration_token="SaZCyK0n2KVDt7lbK3Ka5r6t9aMS8Xu4S8bj7X7l",
        runner_name=h.name,
    )
