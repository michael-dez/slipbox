---
title: man
date: 2026-05-13
tags:
    - help
    - posix
    - apropros
    - whatis
---

Nearly as old as unix and began as literal manuals. Frequently described as terse and I wouldn't disagree. For more comprehensive docs accessible from a terminal, use [info](mw2b.md) pages if available. For faster examples, use [tldr](xu1f.md).

## Section numbers
Every man page displays a section number in the header on either side of the page title. The section number indicates the category of man page.

| Number | Page type |
| --- | --- |
| **1** | Executable programs or shell commands |
| **2** | System calls (functions provided by the kernel) |
| **3** | Library calls (functions within program libraries) |
| **5** | File formats and conventions, e.g. `/etc/passwd`|
| **7** | Miscellaneous |
| **8** | System administration commands (usually only for root)|

## Usage

Open man page specifying the section number.
```bash
# man <page>.<number>
man man.1
```

Search for a page by keyword, without knowing page name.
```bash
man -k <keyword>
# or
apropros <keyword>
```

One line summary of what a command does.
```bash
man -f <command>
# or
whatis <command>
```
