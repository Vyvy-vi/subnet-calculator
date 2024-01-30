import math
import sys
import argparse
from config import defaults
from enum import Enum
from utils import *


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("Error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def calculate_subnets(network, subnet_requirement, wan_links, flsm):
    data = []
    ip, default_mask = network.split("/")
    default_mask = int(default_mask)
    ip = str_to_ipv4(ip)

    subnet_requirement = get_hosts(subnet_requirement)
    computed_subnet_size = [
        2 ** (math.floor(math.log2(i)) + 1) for i in subnet_requirement
    ]

    if flsm:
        max_size = max(computed_subnet_size)
        computed_subnet_size = [max_size for i in computed_subnet_size]

    print(
        f"\n{'FLSM' if flsm else 'VLSM'} Subnetting {network} for hosts - {computed_subnet_size}"
    )

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


if __name__ == "__main__":
    parser = Parser(description="Perform IP subnetting")
    parser.add_argument(
        "network",
        metavar="ip",
        type=str,
        nargs="?",
        help=f"Network IP with CIDR that needs to be subnetted (eg: {defaults.AVAILABLE_SUBNET}).",
    )
    parser.add_argument(
        "subnet_requirement",
        metavar="hosts",
        type=str,
        nargs="*",
        help=f"Number of hosts required for subnets (eg: {' '.join(defaults.HOSTS)}).",
    )
    parser.add_argument(
        "--wan_links",
        "-w",
        metavar="wan",
        type=int,
        nargs="?",
        default=defaults.WAN_LINKS,
        help=f"Number of hosts required for subnets (eg: {defaults.WAN_LINKS}).",
    )
    parser.add_argument(
        "--flsm",
        "-f",
        action="store_true",
        help="VLSM is used by default. Use this flag for FLSM subnetting. ",
    )

    if len(sys.argv) < 3:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    print(args)

    print_table(
        calculate_subnets(
            args.network, args.subnet_requirement, args.wan_links, args.flsm
        )
    )
