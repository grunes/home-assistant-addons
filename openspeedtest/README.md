# Open Speedtest (Home Assistant Add-on)

Run a self-hosted internet speed test UI inside Home Assistant.

## Overview

This add-on packages **Open Speedtest** and exposes its web interface for local speed testing.

## Image Version Policy

This add-on always uses the container image from the project repository with the **matching version tag**.

- Add-on version `X.Y.Z` pulls image tag `X.Y.Z`
- No floating `latest` tag is used
- Every add-on release is tied to the exact upstream image version

This ensures predictable behavior and reproducible deployments.

Current Open Speedtest image tags can be found on Docker Hub:

- https://hub.docker.com/r/openspeedtest/latest/tags?ordering=name

## Usage

1. Install the add-on from this repository.
2. Start the add-on.
3. Open the add-on web UI and run your speed test.

## Notes

- Keep the add-on updated to receive new Open Speedtest releases.

---

**Note:** This is a community add-on and has no official affiliation with the Open Speedtest developers.