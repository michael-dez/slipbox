---
title: zk-nvim
date: 2026-04-21
tags:
    - meta
    - neovim
    - zk
    - zettlekasten
---
zk-nvim is a neovim plugin that allows me to map [zk](j83x) commands to neovim so I can stay in my editor.

Opens a notes picker for active buffers. (Still needs mapped)
```
:ZKBuffers
```

Create a new note from visual selection and replaces the selection with a link to the note.
```
:'<,'>ZkNewFromContentSelection
```
