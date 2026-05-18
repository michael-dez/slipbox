---
title: Kustomize ConfigMap and Secret generators
date: 2026-05-17
tags:
    - kustomize
    - k8s
    - configMapGenerator
    - secretGenerator
---

Generated resources get a hash suffix by default (e.g. `app-config-7f8k2m9t`).
```yaml
configMapGenerator:
  - name: app-config
    literals:
      - KEY=value
    files:
      - configs/app.properties   # key = filename
    envs:
      - .env                     # reads key=value pairs

secretGenerator:
  - name: db-secret
    literals:
      - username=admin
      - password=s3cr3t
    type: Opaque
```

To **disable the hash suffix**:
```yaml
configMapGenerator:
  - name: app-config
    options:
      disableNameSuffixHash: true
    literals:
      - KEY=value
```
