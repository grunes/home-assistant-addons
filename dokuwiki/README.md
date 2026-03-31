# Home Assistant Add-on: DokuWiki

![Supports aarch64 Architecture](https://img.shields.io/badge/aarch64-yes-green.svg)
![Supports amd64 Architecture](https://img.shields.io/badge/amd64-yes-green.svg)

## Über

This add-on provides **DokuWiki** as a lightweight, file-based wiki for Home Assistant.
It is suitable for documentation, notes, how-tos, and internal knowledge bases—without an external database.

## Funktionen

- Fast, file-based wiki (no database required)
- Simple web interface for editing and management
- Persistent data storage via add-on storage
- Suitable for private or team documentation in your home network

## Hinweis zu Image & Version

- This add-on uses the Docker image from the official DokuWiki project.
- The app version matches the version of the Docker image used.

## Installation

1. In Home Assistant, open **Settings → Add-ons**.
2. Add this repository as an add-on source (if it is not already added).
3. Installiere **DokuWiki**.
4. Start the add-on.

## Konfiguration

This add-on usually does not require extensive basic configuration.
Optional settings can be configured on the add-on configuration page.

Example:

```yaml
log_level: info
```

## Nutzung

- Start the add-on.
- Open the web interface via **Open Web UI**.
- Create pages, structure namespaces, and start documenting.

## Daten & Persistenz

All wiki data is stored in the add-on data directory and remains available after restarts and updates.

## Sicherheit

- Prefer running the add-on in a trusted network.
- Use secure credentials if authentication is enabled.
- Regularly check for updates to the add-on and Home Assistant.

## Support

If you encounter issues, please open an issue in the corresponding repository and include:

- Add-on version
- Home Assistant version
- Relevant log excerpts
- Reproduction steps

---

**Note:** This is a community add-on and has no official affiliation with the DokuWiki developers.
