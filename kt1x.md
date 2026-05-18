---
title: Kustomize components
date: 2026-05-17
tags:
    - kustomize
    - k8s
---
Components let you define optional features that can be included by multiple overlays.

```yaml
# components/monitoring/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component

resources:
  - servicemonitor.yaml

patches:
  - path: add-annotations.yaml
```

```yaml
# overlays/prod/kustomization.yaml
resources:
  - ../../base

components:
  - ../../components/monitoring
  - ../../components/autoscaler
```
