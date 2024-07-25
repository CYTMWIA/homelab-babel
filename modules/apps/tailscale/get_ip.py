from modules.core import Host, operation


@operation
def get_ip(host: Host):
    res = host.run("ip --brief address show")
    if res.failed:
        raise Exception(str(res))

    lines = res.stdout.splitlines()
    for line in lines:
        if line.startswith("tailscale"):
            ip_with_mask = line.split()[2]
            ip_only = ip_with_mask[: ip_with_mask.index("/")]
            return ip_only

    raise Exception("Could not find tailscale ip")
