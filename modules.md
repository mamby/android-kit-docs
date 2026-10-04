---
title: Modules
description: Choose the Android Kit artifacts your application needs and align them with the BOM.
permalink: /modules/
section: Start here
---
All artifacts use the Maven group `net.mamby.androidkit`.

| Artifact | Responsibility |
| --- | --- |
| `foundation` | Theme mode and external Android intents |
| `localization` | Per-app locales and locale-aware formatting |
| `compose` | Themes, adaptive layouts, components, forms and navigation UI |
| `navigation3` | Navigation 3 multi-back-stack state and the Kit page renderer |
| `bom` | Aligns the versions of all Kit library modules |

## Shared presentation

The `compose` module supplies Kit's shared controls and page presentation. Hosts
provide typed data, state and callbacks, plus application-owned content inside
supported page, card, sheet and navigation body slots.

Use the [component contract]({% link guides/component-contract.md %}) to understand
the ownership boundary, then choose guides from the documentation menu.

## Navigation

Use `navigation3` when your application needs Kit's Navigation 3 state or
`AndroidKitNavDisplay`. The host still owns routes, destinations and navigation
decisions. Read [navigation]({% link guides/navigation.md %}).

## Distribution

The demo application is a reference consumer, not a library artifact. App branding,
launcher artwork and the demo's Prism theme are not packaged in published modules.

The implementation repository is maintained separately from this public
documentation repository. Public releases will contain compiled artifacts and
dependency metadata. See [installation]({{ '/installation/' | relative_url }}).
