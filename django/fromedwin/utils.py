import ipaddress

def is_private_ipv4(address):
    try:
        ipaddress.IPv4Address(address).is_private
        return True
    except ValueError:
        return False
