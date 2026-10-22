**file**: docs/requirements/requirement-python-about.md
**Status**: Active (Version 1.0.1)
**Area**: python
**Key**: `requirement-python-about`
**Philosophy**: CIAO **v2.10.2** / CIAO-Lite

## 1. Purpose

The about page is identity, the domain diagnostics, the cache labels, the host check, and the star box. It is not a remote version check and it does not upload an archive.

Project nature: a command-line program. About is a page you open, not a second installer.

### 1.1 Human-facing

**In one sentence:** `py-backup about` on a terminal opens a page that names PyBackup, the deposit folder, and the cache labels.

| Box | Meaning | Example |
|-----|---------|---------|
| You / this login | You read the page. It does not change the computer. | `py-backup about` |
| The other role | A version check that talks to a package index is row 84, not this page | `py-backup version-check` |
| Not this file | How archives are named | The backup requirement |

| Includes | Excludes |
|----------|----------|
| Identity, domain sentence, cache labels, host check, star box | Uploading an archive or running pip |
| Row 83 and typed `about` | A printed name `py-tui` |

| Surface | What you open | What for |
|---------|---------------|----------|
| `py-backup about` | the page | identity and deposit |
| Row 83 | the same page from the menu | the same text |

| You do… | What it means | What you type |
|---------|---------------|---------------|
| Open about | On a terminal the page waits. Off a terminal it prints and does not wait. | `py-backup about` |

## 2. Core Rules (Mandatory)

1. Class `AboutPage` composes the page. Class `CheckSystem` supplies the host check. The page **MUST NOT** name `py-tui`.
2. The identity block **MUST** include the product name and version, the domain sentence `Domain: Pack a folder into a dated gzip archive and restore it`, and `Runtime tools: tar`.
3. Domain lines **MUST** include Backup root, Backup notation, Deposit directory, Sudo deposit status, sudoer-cli or `not_found`, sudoer-adm or `absent`, sudoer inbound or `not_found`, the writable flag, `host_sudoers_present`, and `host_sudoers_path`.
4. Cache labels in English **MUST** stay exact: `Cache folder used`, `Cache folder preferred`, `Cache folder 1st`, `Cache folder 2nd`, `Persistence storage`. Persistence is `~/.local/PyBackup` when a home directory exists.
5. The star box stays. When the page is longer than the screen, Up and Down scroll it.
6. Row **83** and typed `about` on a terminal open this page. Typed `about` off a terminal prints it and does not wait.

### 2.1 Implementation Notes

| Field | Value |
|-------|--------|
| Deposit default | `/var/backup/PyBackup` |
| Homepage on the page | `https://github.com/cloudgen/PyBackup` |

### 2.2 Code example

```text
PyBackup 1.0.0
Domain: Pack a folder into a dated gzip archive and restore it
Runtime tools: tar
Backup root: /var/backup
Backup notation: PyBackup
Deposit directory: /var/backup/PyBackup
Cache folder used: <resolved leaf>
Cache folder preferred: <first parent>
Cache folder 1st: <second parent>
Cache folder 2nd: <third parent>
Persistence storage: ~/.local/PyBackup
```

```text
py-backup about
```

There is no Python text-menu mold. This block is the product sample.

## Terminologies

### Operational verb

**Definition:** An operational verb is a CLI routed-verb that runs the product. Typed `about` is an operational verb that shows this page. It does not pack a folder and it does not install.

**Human daily-life explanation:** About is the card on the counter that says who the shop is. It is not the packing bench.

**Daily-life example:** You type `py-backup about` and read the deposit folder. You do not hand over a folder to pack.

## 3. Status history

| Date | Status | Notes |
|------|--------|-------|
| 2026-10-22 | Active 1.0.0 | About page law |
| 2026-10-22 | Active 1.0.1 | Printed field sample and `py-backup about`. |

**Last Updated**: 2026-10-22
**Owner**: project maintainers
**Alignment**: Registry `docs/requirements/index.md`; **CIAO** (https://github.com/cloudgen/ciao); CIAO-Lite (https://github.com/cloudgen/ciao-lite).
