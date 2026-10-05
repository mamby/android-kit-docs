---
title: Support prompts
description: Add an optional support card to page content with host-owned eligibility and callbacks.
permalink: /guides/support-prompt/
section: Components
---
Use the standalone `AndroidKitSupportPrompt` component for a Kit-rendered support
card and its detail sheet. Place it in the page's scrollable body with a stable
item key. `AndroidKitPage` has one content API and does not create a list.

```kotlin
val prompt = if (eligible) AndroidKitSupportPrompt(
    id = presentationId,
    onDonate = onOpenDonationDestination,
    onDismiss = onPromptDismissed,
) else null

AndroidKitPage(title = pageTitle) { padding ->
    LazyColumn(state = listState, contentPadding = padding) {
        if (prompt != null) {
            item(key = "support:${prompt.id}") { AndroidKitSupportPrompt(prompt) }
        }
        items(records, key = { it.id }) { record -> RecordCard(record) }
    }
}
```

The page supplies Kit-owned start/end margins and measured system/chrome
clearance. Apply its padding once as the scrollable body's `contentPadding`;
the viewport remains edge-to-edge. The prompt scrolls away and never opens a
sheet automatically.

Learn more opens the shared sheet. Not now, Close, Back, scrim, and swipe
dismissal end the presentation and invoke onDismiss once. Donate ends the
presentation and invokes onDonate once; it does not indicate successful payment.
Disabled prompts allow dismissal but cannot open the sheet or invoke donation.
Transient state survives configuration changes and scrolling through Compose's
saved item state. Removing the component/configuration removes the sheet. Hosts
remove the prompt from their collection when its presentation ends and supply a
new ID for each new eligible presentation. When selection is active, the owner
omits the prompt from the body.

Hosts own eligibility, cooldowns, persisted dismissal, confirmed-donor suppression,
and the destination. Only opt appropriate pages in. There is no payment provider,
analytics, automatic scheduling, or persistent policy inside Kit.

Kit owns the wording and translations in its private androidkit_compose_support_prompt_*
resources. Kit supplies the languages listed in [localization]({{ site.baseurl }}{% link guides/localization.md %}). Hosts cannot override the
translations; new languages must be added to Kit first. There are no per-prompt
text or rendering slots. The component accepts supported `AndroidKitCardColors`
only; Kit owns geometry, typography and controls.

The existing Settings support footer remains an independent persistent entry.
The Page demo has a Support prompt toggle; its donation action shows a preview
message and collects no payment.
