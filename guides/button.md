---
title: Buttons
description: Choose a text button variant and configure its colors.
permalink: /guides/button/
section: Components
---
`AndroidKitButton` is the Kit-owned text button. It uses a smooth pill shape and
provides Default, Destructive, Outline and Ghost variants. Hosts supply a label,
enabled state and callback; shape, typography, spacing, border width and
interaction rendering remain Kit-owned.

```kotlin
AndroidKitButton(label = "Save", onClick = onSave)
AndroidKitButton(
    label = "Delete",
    onClick = onDelete,
    variant = AndroidKitButtonVariant.Destructive,
)
```

Hosts can set variant colors in `AndroidKitThemeDefinition.componentColors.button`
with `AndroidKitButtonColors` and `AndroidKitButtonVariantColors`, or provide a
per-instance `colors` override. Unspecified roles inherit the active palette:
Default uses primary, Destructive uses error, Outline uses primary content and
border with a transparent container, and Ghost uses primary content
with no border or container. Disabled filled buttons use a muted surface fill;
Outline and Ghost remain transparent. Disabled filled backgrounds use 60%
opacity, while their text uses a 65% tint pre-composited into an opaque
theme-derived color. Outline and Ghost text and borders use a 60% tint
pre-composited into opaque theme-derived colors; their containers remain
transparent.

The button is separate from `AndroidKitFloatingActionButton`, which remains an
icon-only floating control with optional tooltip.
