import subprocess
import argparse
from netifaces import interfaces
from re import match

def sanitize(interface, mac):
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    if match(mac_pattern, mac) is None:
        raise ValueError("Provided MAC address is not valid")
    elif interface not in interfaces():
        raise ValueError(f"Provided interface '{interface}' does not exist")
    return interface, mac

def change_mac(interface, mac):
    interface, mac = sanitize(interface, mac)
    try:
        subprocess.run(["ip", "link", "set", interface, "down"], check=True)
        subprocess.run(["ip", "link", "set", interface, "address", mac], check=True)
        subprocess.run(["ip", "link", "set", interface, "up"], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to change MAC address for {interface}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="MAC changer")
    parser.add_argument("-i", "--interface", help="select interface")
    parser.add_argument("-a", "--address", help="specify which mac address to use")

    args = parser.parse_args()

    if args.interface and args.address:
        try:
            change_mac(args.interface, args.address)
            print(f"MAC address of {args.interface} changed to {args.address}")
            print(subprocess.run(["ip", "a"], check=True))
        except ValueError as e:
            print(e)
    else:
        print("No valid parameters provided. Use --help for more information.")

if __name__ == "__main__":
    main()