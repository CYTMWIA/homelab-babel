from modules.core import Host, operation
from modules.package_manager import pacman


@operation
def setup(host: Host):
    if is_installed():
        print("yay already installed")
        return

    pacman.install(packages=["git", "base-devel"])

    host.run("rm -rf yay-bin && git clone https://aur.archlinux.org/yay-bin.git")

    pacman_path = host.run("which pacman").stdout.strip()
    sudo_cfg = "/etc/sudoers.d/pacman_tmp"

    host.sudo("mkdir -p /etc/sudoers.d")

    # Cannot echo "hello" > x.txt even with sudo? - Ask Ubuntu
    # https://askubuntu.com/questions/103643/cannot-echo-hello-x-txt-even-with-sudo
    # The redirection is done by the shell before sudo is even started.
    host.sudo(f"bash -c 'echo \"ALL ALL=NOPASSWD: {pacman_path}\" > {sudo_cfg}'")

    # 运行到最后会调用 sudo，所以提前修改 sudoers 文件
    host.run("cd yay-bin && makepkg -si")

    host.sudo(f"rm -f {sudo_cfg}")


@operation
def is_installed(host: Host):
    which = host.run("which yay", raise_for_failure=False)
    return bool(len(which.stdout.strip()))
