# Home Assistant Add-on: DokuWiki

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg)

## About

This add-on provides **DokuWiki** as a lightweight, file-based wiki for Home Assistant.
It is suitable for documentation, notes, how-tos, and internal knowledge bases—without an external database.

## Features

- Fast, file-based wiki (no database required)
- Simple web interface for editing and management
- Persistent data storage via add-on storage
- Suitable for private or team documentation in your home network

## Note on Image & Version

- This add-on uses the Docker image from the official DokuWiki project.
- The app version matches the version of the Docker image used.

## Installation

1. In Home Assistant, open **Settings → Add-ons**.
2. Add this repository as an add-on source (if it is not already added).
3. Installiere **DokuWiki**.
4. Start the add-on.

## Configuration

This add-on usually does not require extensive basic configuration.
Optional settings can be configured on the add-on configuration page.

Example:

```yaml
log_level: info
```

## Usage

- Start the add-on.
- Open the web interface via **Open Web UI**.
- Create pages, structure namespaces, and start documenting.

## Data & Persistence

All wiki data is stored in the add-on data directory and remains available after restarts and updates.

---

**Note:** This is a community add-on and has no official affiliation with the DokuWiki developers.
