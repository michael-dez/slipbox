---
title: Kustomize
date: 2026-05-17
tags:
    - cka
    - xiny
    - k8s
---

Kustomize lets you customize Kubernetes manifests without templates. It uses a `kustomization.yaml` file to declare transformations on top of base resources.
---
## Concepts
**[Base/Overlay pattern](b85a.md)**

**[Patching](giip.md)**

**[Image transformers](nbb9.md)**

**[ConfigMap and Secret generators](az5i.md)**

**[Components](kt1x.md)**


## Common cli commands

```bash
# Preview rendered output (dry run)
kubectl kustomize ./dir
kubectl kustomize ./overlays/prod

# Apply resources
kubectl apply -k ./dir
kubectl apply -k ./overlays/prod

# Delete resources
kubectl delete -k ./dir

# Diff against live cluster
kubectl diff -k ./dir
```

---

## kustomization.yaml example

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: my-namespace          # applied to all resources

resources:
  - deployment.yaml
  - service.yaml
  - ../base                      # reference a base directory

commonLabels:
  app: my-app
  env: prod

commonAnnotations:
  team: platform

namePrefix: prod-                # prepends to all resource names
nameSuffix: -v2

images:
  - name: nginx
    newTag: "1.25"
    newName: my-registry/nginx   # optional rename

configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=info
    files:
      - config.properties

secretGenerator:
  - name: app-secret
    literals:
      - DB_PASS=secret123
    type: Opaque

patches:
  - path: patch-replicas.yaml
  - patch: |-                    # inline patch
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-deploy
      spec:
        replicas: 5
```

---



## CKA exam patterns

**Add a label to all resources:**
```yaml
commonLabels:
  environment: staging
```

**Change namespace for everything:**
```yaml
namespace: staging
```

**Add a sidecar container via patch:**
```yaml
patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: my-deploy
      spec:
        template:
          spec:
            containers:
              - name: sidecar
                image: busybox
```

---

## Quick Reference

| Task | How |
|---|---|
| Apply a kustomization | `kubectl apply -k ./dir` |
| Preview output | `kubectl kustomize ./dir` |
| Set namespace on all resources | `namespace:` in kustomization.yaml |
| Add labels to all resources | `commonLabels:` |
| Prefix all resource names | `namePrefix:` |
| Change an image tag | `images:` block |
| Partial manifest override | Strategic merge patch |
| Surgical field edit | JSON 6902 patch with `op/path/value` |
| Generate ConfigMap from literals | `configMapGenerator:` |
| Reuse across multiple overlays | `components:` |

