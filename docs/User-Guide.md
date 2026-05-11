# WordListeXplorer Guide
Documentation & User Guide to use WordListeXplorer

## Introduction

WLX (WordListeXplorer) is a local wordlist intelligence and workflow management platform built for offensive security professionals, penetration testers, red teamers, bug bounty hunters, and researchers who work with large-scale wordlist collections.

Modern security workflows often involve thousands of wordlists spread across multiple directories, repositories, and tools. WLX simplifies this process by providing a centralized, searchable, and workflow-focused interface for managing and using wordlists directly from the terminal.

With WLX, users can:

- Organize massive wordlist collections into a structured local index
- Perform fast keyword-based searches across indexed wordlists
- Categorize wordlists using custom tags and filters
Export wordlists directly into shell environment variables
- Integrate wordlists seamlessly into offensive tooling and automation workflows
- Manage reusable workflow variables for faster operations and scripting

WLX is designed with a strong focus on operational efficiency and terminal-native workflows, making it ideal for daily offensive security & bug bounty operations.


## Table of Contents

1. Installation
2. First-Time Setup
3. Scanning Wordlists
4. Searching Wordlists
5. Filtering with Tags
6. Manual Tagging
7. Removing Tags
8. WLX Variables
9.  Uninstalling WLX
10. Resetting WLX
11. Troubleshooting


## 1.0 Installation

**1.1 Clone Repository**

```bash
git clone https://github.com/ZeroPrime9/WordListeXplorer.git
cd WorldListExplorer/wlx/scripts
```

**1.2 Run Installer**

```bash
chmod +x installer.sh
./installer.sh
```

The installer will:
- Install WLX
- Configure PATH
- Configure shell integration
- Setup WLX workflow helpers

**1.3 Verify Installation**

```bash
wlx --help
wlx
```

## 2.0 First-Time Setup

Before searching, WLX must index your wordlists so they can be searched efficently.

**2.1 Add a Wordlist Directory**

To index a directory containing wordlists:

```bash
wlx config addir /usr/share/seclists
```

**2.2 Add multiple directories:**

You can add multiple directories at any time

```bash
wlx config addir ~/wordlists
wlx config addir ~/usr/share/wordlists
```

**2.3 View Configured Directories**

Once a directory has been added to WLX, you can view all configured and indexed wordlist locations using:

```bash
wlx config list
```

This command displays every directory currently registered with WLX for indexing and searching


## 3.0 Scanning Wordlists

WLX stores indexed wordlists locally inside its SQLite database for fast and efficient searching. After adding your wordlist directories, run a scan to index all files into the WLX database:

```bash
wlx config index
```

WLX will recursively process all configured directories and add supported wordlists to the local index. Depending on the size of your collections, the initial scan may take some time.

## 4.0 Searching Wordlists

WLX provides fast and flexible searching across all indexed wordlists stored in the local database.

**4.1 Basic Search**

Perform a keyword search across indexed wordlists:

```bash
wlx search admin
```
This searches for wordlists related to the term `admin` and returns matching results from the local index.

**4.2 Search with Filters**

You can narrow down search results using tag filters:

```bash
wlx search login --filter api,auth
```
In this example:

- `login` is the primary search keyword
- `--filter` limits results to wordlists tagged with:
  - api
  - auth

You can also search using only filters:

```bash
wlx search "" --filter api, auth
```

In this example:

- `""` there is no primary search keyword
- `--filter` limits results to wordlists only tagged with:
  - api
  - auth

Filters help reduce noise and make it easier to find relevant wordlists within large collections. You can specify multiple filters separated by commas.


**4.3 Search Results**

WLX displays the following information for each result:

- ID
- Name
- Tags
- File Size
- Path

## 5.0  Manual Tagging

WLX allows you to manually assign tags to wordlists to improve organization, filtering, and search accuracy. Tags make it easier to categorize wordlists based on their purpose, technology, platform, or usage type.

Common examples include:

- injection
- api
- hydra
- passwords
- web
- subdomains
- fuzzing

**5.1 Single Wordlist**

Apply a tag to a specific wordlist using its ID:

```bash
wlx tag 12 auth
```
This assigns the tag auth to the wordlist with ID 12.

**5.2 Multiple Wordlists**

You can apply the same tag to multiple wordlists at once:

```bash
wlx tag 12,15,20 auth
```
This adds the `auth` tag to wordlists id `12,15,20`

**5.3 Multiple Tags**
Multiple tags can also be assigned in a single command:

```bash
wlx tag 12,15 auth,hydra,passwords
```
This applies the following tags:

- auth
- hydra
- passwords

To both wordlists ID:

- 12
- 15

## 6.0 Removing Tags

WLX also allows you to remove previously assigned tags from wordlists.

This helps keep your wordlist organization clean and ensures tags remain accurate over time.

**6.1 Remove Single Tag**

Remove a specific tag from a wordlist using its ID:

```bash
wlx untag 12 auth
```

This removes the auth tag from the wordlist with ID 12.

**6.2 Remove Multiple Tags**

You can remove multiple tags from one or more wordlists in a single command:

```bash
wlx untag 12,15 auth,passwords
```

This removes the following tags:

- auth
- passwords

From wordlists:

- 12
- 15

## 7.0 WLX Variables

WLX can integrate directly into your shell workflow by exporting wordlist paths into environment variables.

This makes it easier to reference commonly used wordlists in scripts, commands, and security tools without repeatedly typing full file paths.


**7.1 Export Wordlists Into Variables**

Export a wordlist using its WLX ID:

```bash
wlxuse 12 vulndir
```

In this example:

- `12` is the wordlist ID
- `USERNAME` becomes the environment variable name

WLX will automatically map the selected wordlist path to the variable and you can then use it directly in your shell

```bash
feroxbuster -u https://vulnweb.com -w $VULNDIR
```

`wlxuse` with hydra

```bash
wlxuse 12 USERNAME
wlxuse 15 PASSWORD

hydra -L $USERNAME -P $PASSWORD target
```


**7.2 View Active Variables**

To view all currently exported WLX variables:

```bash
wlx vars
```
This displays all active variable mappings created through WLX. Once the terminal is closed all exported variable gets deleted.


## Example Output

```text
USERNAME -> /usr/share/seclists/Usernames/top-usernames-shortlist.txt
```

## 8.0 Configuration Management

**8.1 Add Directory**

Add a directory to WLX so it can be scanned and indexed for searchable wordlists:

```bash
wlx config addir /path
```

WLX will store the directory in its configuration and include it during future scans.

**8.2 Remove Directory**

Remove a configured directory using its configuration ID:

```bash
wlx config rmdir 1
```

In this example, `1` represents the configured directory ID shown in the configuration list.

Removing a directory prevents WLX from scanning it in future indexing operations.

**8.3 List Configuration**

View all currently configured directories registered with WLX:

```bash
wlx config list
```
This command displays:

- Configuration IDs
- Indexed directory paths
- Registered scan locations


**8.4 Diagnostics**

Run diagnostics to verify WLX configuration, database connectivity, indexing status, and environment setup:

```bash
wlx config diag
```

**8.5 Resetting WLX**


WLX provides a reset option to completely clear its local configuration and indexed data.

Running a reset will remove:

- The local SQLite database
- All configured directories
- Indexed wordlist metadata
- Active WLX session variables

This is useful when rebuilding the index from scratch, troubleshooting issues, or starting with a clean configuration.


```bash
wlx config reset
```
After resetting, you will need to re-add your directories, source your shell and run a new scan before searching wordlists again.

## 9.0 Uninstalling WLX

WLX includes an uninstall script to safely remove the application and clean up its shell integrations.

**9.1 Run Uninstaller**

From the WLX project directory, execute:

```bash
./scripts/uninstall.sh
```

The uninstaller will:

- Remove WLX binaries and helper scripts
- Clean shell configuration entries
- Remove exported WLX environment variables
- Delete local WLX data and configuration files

Depending on your shell environment, the script may prompt you to reload or source your shell configuration after completion.

## 10.0 Troubleshooting

This section covers common WLX issues and how to resolve them.

**10.1 WLX Command Not Found**


If the wlx command is not recognized, ensure that:

```bash
~/.local/bin
```

is included in your system `PATH`.

You can verify this with:

```bash
echo $PATH
```
If required, reload your shell configurations:

```bash
source ~/.bashrc
```
For ZSH users:

```bash
source ~/.zshrc
```

**10.2 Variables Not Exporting**

WLX variables must be exported using:

```bash
wlxuse
```

Example:

```bash
wlxuse <id> USERNAME
```

Do not use:

```bash
wlx use
```

as it is not a valid command

**10.3 Database Missing**

If searches return no results or the database has not been created yet, run a scan to generate and populate the local index:

```bash
wlx scan
```
Ensure that at least one directory has been added before scanning.

**10.4 Check Environment Health**

To verify WLX configuration, database connectivity, indexing status, and shell integration, run:

```bash
wlx config diag
```
Diagnostics can help identify configuration issues, missing dependencies, or indexing problems.



