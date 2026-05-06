---
title: Find and Replace
date: 2023-05-22
tags:
 - bash
 - sed
 - find
---
A simple example of how to use the `-exec` option of the `find` command to use `sed` for customizable "global search and replace".
```bash
find . -name <file_pattern> -exec sed -i s/<find_pattern>/<replace_pattern>/g' {} \;
```



