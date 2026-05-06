---
title: Go Packages
date: 2022-11-14
tags:
    - golang
    - go-packages
    - the-go-programming-language-book
---
## What is a package
- it's a logical grouping of source files
- a package is comprised of one or more `*.go` files in a directory.
```bash
└── example_package
    ├── file1.go
    └── file2.go
```
## How to declare a package
- start source with a `package` statement.
- the `main` package is executable using it's [`main()`]() function.
```go
// declared on the first line
package main
```
## Package dependencies
- package dependencies are tracked in the `go.mod` file
## how to import packages
```go
package main
// import statements come after package declaration
import "fmt"
```
> why do imports need quotes when package declaration doesn't...?
## Remember
- the compiler won't allow unused packages, so use it or lose it.
