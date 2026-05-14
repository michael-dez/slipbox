---
title: Securely set a shell variable interactively
date: 2026-05-13
tags:
    - shell
    - interactive
---
Uses `read` with `-s` option to keep value out of shell history and `-r` option to save you 10 minutes on the rare occasion the input contains a backslash.
```bash
# waits for and 's'ilences user input like a password prompt
read -rs FOO && export FOO
```



