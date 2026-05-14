---
title: Navigate info pages
date: 2026-05-13
tags:
    - shell
    - info
    - help
---
Keybinds are based on emacs... Per key binds can be set with a `texinfo` config at `~/.infokey` or `${XDG_CONFIG_HOME}/texinfo/infokey`. Another option is using `info --vi-keys` or set vi-keys as default in the [readline](l83n) config, `.inputrc`. Consider using a texinfo config because both default and vi-keys have some awkward defaults.

An info page node is basically a single [man](5gfy) page that can be linked with other nodes making a tree.

The `info` command with no arguments puts you at the top of the tree.

**help** `H`elp shows some of the most useful keybinds

## Navigate between nodes
Links to nodes are underlined and can be traversed with `Enter/Return`. Node navigation allows travel in the following "directions":

**previous** `p`

**next** `n`

**up** `u`

**down** `m` view subnodes of the current node

## Navigate within a node
The staples
- `<C-u>`
- `<C-d>`
- `gg`
- `G`

What else could one need?

## Reference
[texinfo config](https://github.com/michael-dez/dotfiles/blob/main/texinfo/infokey)
