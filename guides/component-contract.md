---
title: Component ownership
description: Keep Kit's shared controls consistent while composing your application's content.
permalink: /guides/component-contract/
section: Start here
---
Android Kit is opinionated. It owns the shape, typography, geometry, predefined
icons and labels, control arrangement, accessibility semantics and interaction
behavior of its components.

## What the application supplies

- Typed content and domain data.
- State, callbacks and availability options.
- Supported placement and layout choices.
- The theme palette and supported component colors.
- Application body content in page, card, sheet and navigation body slots.

Public component APIs do not expose arbitrary rendering slots for headers,
controls, menus, settings rows or badges. See [themes]({% link guides/theme.md %})
for the color-only appearance contract.

## Application-owned content

Your application owns its content styling, routes, authentication, permissions,
business rules and domain persistence. Kit's body slots let you compose that
content within the shared presentation.

Apply the managed content padding supplied by pages and sheets to the scrolling
content. This lets the viewport remain edge-to-edge while clearing the component's
measured chrome and system insets.

## Typed controls and actions

Use [section cards]({% link guides/section-card.md %}) for typed rows and controls.
Declare menu entries through the [action flyout]({% link guides/action-flyout.md %})
DSL; Kit renders their icons, text, spacing and dismissal behavior.

[Lists]({% link guides/list.md %}) accept application-owned item bodies while Kit
owns item interaction, menus, selection and supported swipe actions.

## Settings and history

Declare one complete [Settings catalog]({% link guides/settings.md %}) in an owner
above Settings navigation. Main, About and subpages share its catalog, persistent
values, search history and privacy state.

Independent [content searches]({% link guides/search-page.md %}) keep a separate
history and privacy scope for each logical page.

## Shared vocabulary

Kit owns predefined control wording and translations. Your application owns
content labels, custom action labels, option values and domain messages.
Consumers must apply the [localization build gate]({% link guides/localization.md %}).
