
<p align="center">
  <img src="docs/images/WordListeXplorer-Banner.png" alt="WLX Banner">
</p>

<p align="center">
  A local wordlist intelligence and workflow management tool for offensive security & Bug Bounty workflows.
</p>

<p align="center">

  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/license-Apache%202.0-red.svg">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-3776AB.svg">
  <img src="https://img.shields.io/badge/interface-terminal-black.svg">
</p>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Install</a> •
  <a href="/docs/User-Guide.md">User Guide</a> •
  <a href=".CHANGELOG.md">Changelogs</a> •
</p>

---

# Overview

WLX (WordListeXplorer) is a local wordlist intelligence and workflow management platform built for offensive security professionals, penetration testers, red teamers, bug bounty hunters, and researchers who work with large-scale wordlist collections.


With WLX, users can:

- Organize massive wordlist collections into a structured local index
- Perform fast keyword-based searches across indexed wordlists
- Categorize wordlists using custom tags and filters
Export wordlists directly into shell environment variables
- Integrate wordlists seamlessly into offensive tooling and automation workflows
- Manage reusable workflow variables for faster operations and scripting

WLX is designed with a strong focus on operational efficiency and terminal-native workflows, making it ideal for daily offensive security & bug bounty operations.

## Features

- Recursive wordlist indexing
- SQLite-powered local database
- Fast keyword searching
- Tag-based filtering
- Bulk tagging operations
- Session-aware WLX variables
- Shell workflow integration
- Rich terminal UI

View the documentation to read through all the features & troubleshooting of WLX:

[![VIEW MANUAL](https://img.shields.io/badge/VIEW-MANUAL-black?style=for-the-badge&logo=gitbook&logoColor=white)](/docs/User-Guide.md)
---


<p align="center">
  <img src="docs/gifs/wlx-preview.gif" alt="WLX Preview">
</p>



# Installation


## Clone Repository

```bash
git clone https://github.com/ZeroPrime9/WordListeXplorer.git
cd WordListeXplorer/wlx/scripts
```

## Run Installer

```bash
chmod +x install.sh

./install.sh
```

The installer will:
- Install WLX
- Configure PATH
- Setup shell integration
- Configure WLX workflow helpers



# Quick Start


## Add Wordlist Directory

WLX supports adding and managing multiple wordlist directories.

```bash
wlx config addir /usr/share/seclists/
wlx config addir /usr/share/wordlists/
```

You can add any number of directories and WLX will recursively scan and index all supported wordlists from them.


## Scan Directory

After adding the wordlists to the config just do the following to scan and index the directories

```bash
wlx config index 
```

<img src="docs/gifs/wlx-quick-start.gif" alt="WLX Scan">



# WLX Features



## Search Wordlists

Search indexed wordlists instantly using keywords, filenames, or naming patterns directly from the terminal.


```bash
wlx search admin
```


## Filter Search Results

Narrow down results using one or more tags to quickly locate relevant wordlists for specific workflows or technologies.


```bash
wlx search login --filter api,auth,wfuzz
```

You can add any number of filters and WLX will filter and index all the wordlists.

<img src="docs/gifs/wlx-preview.gif" alt="WLX Searching Wordlists">


## Export Wordlists Into Variables

Export wordlists into reusable shell variables for direct integration into offensive security workflows and tooling.


```bash
wlxuse 12 username
wlxuse 15 password
```

## Use Exported Variables In Real Workflows

WLX variables can be used directly with tools such as Hydra, FFUF, Feroxbuster, and other offensive security tooling.

```bash
hydra -L $USERNAME -P $PASSWORD target
```
```bash
wlxuse 22 FUZZ

ffuf -u https://target/FUZZ -w $FUZZ
```

<img src="docs/gifs/wlx-vars.gif" alt="WLX Searching Wordlists">


## Tagging System

WLX supports:
- manual tagging
- bulk tagging
- multi-tag workflows
- filter-driven searching


## Bulk Tagging Example

```bash
wlx tag 12,15,18 auth,hydra,passwords
```


## Tagging Preview

<img src="docs/gifs/wlx-tag.gif" alt="WLX Searching Wordlists">

# Uninstallation

```bash
./scripts/uninstall.sh
```

# Roadmap

## v1.1
- Intelligent ranking engine
- Relevance-based search prioritization
- Smarter filtering workflows
- Advanced search intelligence
- Auto-Indexer for any new files


# License

Licensed under the Apache 2.0 License.

# Author

This tool created by Farzan Nobi (ZeroPrime9)