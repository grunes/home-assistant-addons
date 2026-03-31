#!/usr/bin/env python3
"""
HMIP Multicast Relay - Relays link-local multicast (TTL=1) between interfaces.

Uses SO_BINDTODEVICE to ensure sockets are bound to the correct interface,
and raw IP_ADD_MEMBERSHIP with interface index (ip_mreqn) to join multicast
groups on exactly the right interface.
"""

import socket
import struct
import sys
import threading
import logging
import time

MULTICAST_TTL = 1
BUFFER_SIZE = 65535

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("hmip-relay")


def get_ifindex(ifname: str) -> int:
    """Get interface index by name using SIOCGIFINDEX."""
    import fcntl
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        result = fcntl.ioctl(
            s.fileno(),
            0x8933,  # SIOCGIFINDEX
            struct.pack("256s", ifname.encode("utf-8")[:15]),
        )
        return struct.unpack("I", result[16:20])[0]
    finally:
        s.close()


def ifname_for_ip(ip: str) -> str:
    """Find the interface name for a given IP address."""
    import subprocess
    result = subprocess.run(
        ["ip", "-4", "-o", "addr", "show"],
        capture_output=True, text=True, check=True,
    )
    for line in result.stdout.strip().split("\n"):
        parts = line.split()
        # Format: idx: ifname inet x.x.x.x/prefix ...
        if len(parts) >= 4:
            addr = parts[3].split("/")[0]
            if addr == ip:
                return parts[1].rstrip(":")
    raise ValueError(f"No interface found with IP {ip}")


def make_recv_socket(group: str, port: int, bind_ip: str, ifname: str) -> socket.socket:
    """Create a socket that receives multicast on a specific interface."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Bind to specific interface at kernel level
    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_BINDTODEVICE,
        ifname.encode("utf-8") + b"\0",
    )

    # Bind to group address + port
    sock.bind(("", port))

    # Join multicast group using ip_mreqn (with interface index)
    # struct ip_mreqn { multicast_addr, local_addr, ifindex }
    ifindex = get_ifindex(ifname)
    mreqn = struct.pack(
        "4s4sI",
        socket.inet_aton(group),
        socket.inet_aton("0.0.0.0"),
        ifindex,
    )
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreqn)

    log.info("Recv socket: group=%s port=%d iface=%s (idx=%d)", group, port, ifname, ifindex)
    return sock


def make_send_socket(group: str, bind_ip: str, ifname: str) -> socket.socket:
    """Create a socket that sends multicast on a specific interface."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Bind to specific interface
    sock.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_BINDTODEVICE,
        ifname.encode("utf-8") + b"\0",
    )

    # Set TTL
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)

    # Set outgoing interface using ip_mreqn
    ifindex = get_ifindex(ifname)
    mreqn = struct.pack(
        "4s4sI",
        socket.inet_aton("0.0.0.0"),
        socket.inet_aton("0.0.0.0"),
        ifindex,
    )
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, mreqn)

    # Disable loopback
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)

    log.info("Send socket: iface=%s (idx=%d)", ifname, ifindex)
    return sock


def relay(
    group: str,
    port: int,
    recv_ifname: str,
    recv_ip: str,
    send_ifname: str,
    send_ip: str,
    direction: str,
):
    """Receive multicast on one interface, re-send on another."""
    recv_sock = make_recv_socket(group, port, recv_ip, recv_ifname)
    send_sock = make_send_socket(group, send_ip, send_ifname)

    log.info("Relay %s: %s:%d  %s -> %s", direction, group, port, recv_ifname, send_ifname)

    pkt_count = 0
    while True:
        try:
            data, (src_addr, src_port) = recv_sock.recvfrom(BUFFER_SIZE)

            # Prevent loops: skip packets from our own send interface
            if src_addr == send_ip:
                continue

            send_sock.sendto(data, (group, port))
            pkt_count += 1

            if pkt_count <= 5 or pkt_count % 100 == 0:
                log.info(
                    "%s: relayed %d bytes from %s:%d (total: %d)",
                    direction, len(data), src_addr, src_port, pkt_count,
                )
        except OSError as e:
            log.error("%s: socket error: %s - retrying in 5s", direction, e)
            time.sleep(5)


def main():
    if len(sys.argv) < 5:
        print(
            f"Usage: {sys.argv[0]} <group> <port> <source_ip> <target_ip> [log_level]",
            file=sys.stderr,
        )
        sys.exit(1)

    group = sys.argv[1]
    port = int(sys.argv[2])
    source_ip = sys.argv[3]
    target_ip = sys.argv[4]
    log_level = sys.argv[5] if len(sys.argv) > 5 else "info"

    log.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    source_ifname = ifname_for_ip(source_ip)
    target_ifname = ifname_for_ip(target_ip)

    log.info("HMIP Relay starting for %s:%d", group, port)
    log.info("  LAN:    %s (%s)", source_ifname, source_ip)
    log.info("  Docker: %s (%s)", target_ifname, target_ip)

    t1 = threading.Thread(
        target=relay,
        args=(group, port, source_ifname, source_ip, target_ifname, target_ip, "LAN->Docker"),
        daemon=True,
    )
    t2 = threading.Thread(
        target=relay,
        args=(group, port, target_ifname, target_ip, source_ifname, source_ip, "Docker->LAN"),
        daemon=True,
    )

    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
