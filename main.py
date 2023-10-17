import math
from table2ascii import table2ascii, Alignment, PresetStyle
from config import defaults
from utils import *

def cidr_to_subnet_mask(cidr):
    subnet_mask = cidr * "1" + (32 - cidr) * "0"
    subnet_mask = int_to_ipv4(int(subnet_mask, 2))
    return ipv4_to_str(subnet_mask)


network = (
    input(f"Enter network with CIDR ({defaults.AVAILABLE_SUBNET}): ")
    or defaults.AVAILABLE_SUBNET
)
subnet_requirement = (
    input(f"Enter no. of hosts for each subnet (eg: {defaults.HOSTS}): ")
    or defaults.HOSTS
)
wan_links = int(
    (input(f"Enter no. of WAN links (eg: {defaults.WAN_LINKS}): ") or defaults.WAN_LINKS)
)


def calculate_subnets(network, subnet_requirement, wan_links):
    data = []
    ip, default_mask = network.split("/")
    default_mask = int(default_mask)
    ip = str_to_ipv4(ip)

    subnet_requirement = get_hosts(subnet_requirement)
    computed_subnet_size = [
        2 ** (math.floor(math.log2(i)) + 1) for i in subnet_requirement
    ]

    print(f"\nSubnetting {network} for hosts - {computed_subnet_size}")

    new_ip = ip[::]
    for i, size in enumerate(computed_subnet_size):
        new_cidr = 32 - round(math.log2(size))
        network_addr = f"{ipv4_to_str(new_ip)}/{new_cidr}"

        new_ip = shift_ipv4(new_ip, size)

        data.append(
            [
                network_addr,
                cidr_to_subnet_mask(new_cidr),
                f"{size - 2} hosts",
                f"LAN{i + 1}",
                ipv4_to_str(new_ip),
            ]
        )

    for i in range(wan_links):
        new_cidr = 32 - 2
        network_addr = f"{ipv4_to_str(new_ip)}/{new_cidr}"
        new_ip = shift_ipv4(new_ip, 4)

        data.append(
            [
                network_addr,
                cidr_to_subnet_mask(new_cidr),
                "2 hosts",
                f"WAN link{i + 1}",
                ipv4_to_str(new_ip),
            ]
        )
    return data


def print_table(data):
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


print_table(calculate_subnets(network, subnet_requirement, wan_links))
