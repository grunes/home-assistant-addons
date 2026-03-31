# HMIP Multicast Relay Add-on

Relays multicast traffic for Homematic IP devices (HMIPW-DRAP, HMIP-HAP) between the physical host network and Docker container networks.

> **Beta:** This add-on was developed and tested on a Home Assistant Green. The Docker image is currently built locally by the Supervisor — there is no pre-built image available yet.

## Problem

Docker bridge networks do not forward multicast packets from the host network into containers by default. Homematic IP Wired Access Points (HMIPW-DRAP) and Homematic IP Access Points (HMIP-HAP) use multicast for device discovery and communication. When running OpenCCU in a Docker container on Home Assistant OS, these multicast packets never reach the container.

The existing HA Multicast plugin (`plugin-multicast`) only handles mDNS (224.0.0.251:5353) via `mdns-repeater` and cannot relay arbitrary multicast groups.

## Solution

This add-on runs a Python-based multicast relay with `host_network: true` and `NET_ADMIN` capability. It creates bidirectional multicast sockets bound to the physical network interface and the Docker bridge, so multicast packets flow in both directions.

## Configuration

| Option | Default | Description |
|---|---|---|
| `multicast_groups` | `["224.0.0.120:43438", "224.0.0.1:43439"]` | Multicast group:port entries to relay (format `GROUP:PORT`) |
| `source_interface` | *(auto-detect)* | Physical network interface (e.g. `eth0`, `end0`) |
| `target_interface` | *(auto-detect)* | Docker bridge interface (e.g. `hassio`, `docker0`) |
| `log_level` | `info` | Log verbosity: `debug`, `info`, `warning`, `error` |

## Important Notes

- **OpenCCU must also run with `host_network: true`** (or on the same Docker bridge as `target_interface`) for the multicast packets to actually reach it.
- This add-on is intended as an alternative, potentially more stable solution to the [HMIPHAP/HMIPWDRAP support patch](https://github.com/OpenCCU/OpenCCU/wiki/Installation-HomeAssistant#hmiphaphmipwdrap-support-patch), but it still needs sufficient real-world testing.
- If both this add-on and OpenCCU use `host_network: true`, no relay is needed — they share the host network stack and multicast works natively. In that case this add-on is only needed if OpenCCU runs on a bridge network.
- The `multicast_groups` list should include the specific multicast addresses used by your HMIP devices. The defaults cover HMIP-HAP and HMIPW-DRAP discovery. You may need to capture traffic with `tcpdump -i eth0 -n multicast` to identify additional groups your devices use.

---

**Note:** This is a community add-on and has no official affiliation with the OpenCCU developers.