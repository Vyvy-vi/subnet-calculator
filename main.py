import math
from table2ascii import table2ascii, Alignment, PresetStyle

DEFAULT_AVAILABLE_SUBNET = "192.168.2.0/24"
DEFAULT_HOSTS = "24 50 8"
DEFAULT_WAN_LINKS = "3"

data = []


def cidr_to_subnet_mask(cidr):
    subnet_mask = cidr * "1" + (32 - cidr) * "0"
    subnet_mask = [
        int(subnet_mask[i : i + 8], 2) for i in range(0, len(subnet_mask), 8)
    ]
    return ipv4_to_str(subnet_mask)


def ipv4_to_str(ip):
    return ".".join([str(i) for i in ip])


def str_to_ipv4(s):
    ip = list(map(lambda x: int(x), s.split(".")))
    if len(ip) > 4:
        raise RuntimeError("Invalid IP String")
    return ip


def get_hosts(hosts):
    return sorted(list(map(lambda x: int(x), hosts.split(" "))), reverse=True)


network = (
    input(f"Enter network with CIDR ({DEFAULT_AVAILABLE_SUBNET}): ")
    or DEFAULT_AVAILABLE_SUBNET
)
subnet_requirement = (
    input(f"Enter no. of hosts for each subnet (eg: {DEFAULT_HOSTS}): ")
    or DEFAULT_HOSTS
)
wan_links = int(
    (input(f"Enter no. of WAN links (eg: {DEFAULT_WAN_LINKS}): ") or DEFAULT_WAN_LINKS)
)

ip, default_mask = network.split("/")
default_mask = int(default_mask)
ip = str_to_ipv4(ip)
subnet_requirement = get_hosts(subnet_requirement)

computed_subnet_size = [2 ** (math.floor(math.log2(i)) + 1) for i in subnet_requirement]

print(f"\nSubnetting {network} for hosts - {computed_subnet_size}")

cnt = 0
new_ip = ip[::]
for i in computed_subnet_size:
    H = round(math.log2(i))
    new_cidr = 32 - H
    cnt += 1
    network_addr = f"{ipv4_to_str(new_ip)}/{new_cidr}"

    new_ip[-1] += i
    for j in range(-1, -4, -1):
        while new_ip[j] > 255:
            new_ip[j] -= 255
            new_ip[j - 1] += 1

    data.append(
        [
            network_addr,
            cidr_to_subnet_mask(new_cidr),
            f"{i - 2} hosts",
            f"LAN{cnt}",
            ipv4_to_str(new_ip),
        ]
    )

cnt = 0
for i in range(wan_links):
    new_cidr = 32 - 2
    cnt += 1
    network_addr = f"{ipv4_to_str(new_ip)}/{new_cidr}"

    new_ip[-1] += 4
    for j in range(-1, -4, -1):
        while new_ip[j] > 255:
            new_ip[j] -= 255
            new_ip[j - 1] += 1

    data.append(
        [
            network_addr,
            cidr_to_subnet_mask(new_cidr),
            "2 hosts",
            f"WAN link{cnt}",
            ipv4_to_str(new_ip),
        ]
    )

output = table2ascii(
    header=[
        "Network Address",
        "Subnet Mask",
        "Usable Hosts",
        "Type",
        "Broadcast Address",
    ],
    body=data,
    style=PresetStyle.ascii_box,
)
print(output)
