---
title: patches
date: 2026-05-17
tags:
    - kustomize
---

## Strategic Merge Patch (most common)

Merges with existing resource. Looks like a partial manifest.

```yaml
# patch-replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deploy
spec:
  replicas: 5
  template:
    spec:
      containers:
        - name: app
          resources:
            limits:
              memory: "512Mi"
```

## JSON 6902 Patch

Precise surgical operations using `op`, `path`, `value`.

```yaml
# In kustomization.yaml
patches:
  - target:
      kind: Deployment
      name: my-deploy
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
      - op: add
        path: /spec/template/spec/containers/0/env/-
        value:
          name: ENV
          value: production
      - op: remove
        path: /spec/template/spec/containers/0/livenessProbe
```

| `op` value | Effect |
|---|---|
| `replace` | Change an existing field |
| `add` | Add a new field or array element |
| `remove` | Delete a field |

---


