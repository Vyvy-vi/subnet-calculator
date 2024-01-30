from table2ascii import table2ascii, Alignment, PresetStyle


def ipv4_to_int(octets):
    return (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]


def int_to_ipv4(num):
    return [(num >> 24) & 255, (num >> 16) & 255, (num >> 8) & 255, num & 255]


def shift_ipv4(ip, num_devices):
    ip_int = ipv4_to_int(ip)
    shifted_ip_int = ip_int + num_devices
    shifted_ip = int_to_ipv4(shifted_ip_int)
    return shifted_ip


def ipv4_to_str(ip):
    return ".".join([str(i) for i in ip])


def str_to_ipv4(s):
    ip = list(map(lambda x: int(x), s.split(".")))
    if len(ip) > 4:
        raise RuntimeError("Invalid IP String")
    return ip


def get_hosts(hosts):
    return sorted(list(map(lambda x: int(x), hosts)), reverse=True)


def cidr_to_subnet_mask(cidr):
    subnet_mask = cidr * "1" + (32 - cidr) * "0"
    subnet_mask = int_to_ipv4(int(subnet_mask, 2))
    return ipv4_to_str(subnet_mask)


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
