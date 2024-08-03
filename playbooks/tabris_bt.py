from modules.apps import qbittorrent, jellyfin, peerbanhelper
from modules.core import host, Host

h: Host = host("tabris")
with h:
    qb_base = "/srv/qbittorrent"
    qb_download_dir = qb_base + "/downloads"
    qbittorrent.setup(
        base_dir=qb_base,
        config_dir=qb_base + "/config",
        download_dir=qb_download_dir,
        watch_dir=qb_base + "/watch",
    )

    peerbanhelper.setup(
        base_dir="/srv/peerbanhelper/",
        data_dir="/srv/peerbanhelper/data",
    )

    # 放这可能不太合适，但单独放到一个文件感觉也不太方便……
    jellyfin.setup(
        base_dir="/srv/jellyfin",
        media_dir=qb_download_dir,
    )

