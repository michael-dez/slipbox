---
title: Kustomize image transformers
date: 2026-05-17
tags:
    - kustomize
    - k8s
---


Override image tags without changing base manifests:

```yaml
images:
  - name: nginx              # must match image name in manifests
    newTag: "1.25.3"
  - name: my-app
    newName: gcr.io/my-project/my-app
    newTag: "v2.1.0"
```
