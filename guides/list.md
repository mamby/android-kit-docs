---
title: Lists and selection
description: Declare list and grid items, context actions, swipe deletion and bulk selection.
permalink: /guides/list/
section: Components
---
`AndroidKitList` renders host-owned **visual-only** item bodies. Kit owns the full
item's tap, context menu, highlight, swipe, selection check, semantics and animation.
Do not place clickable controls, pointer/key handlers, menus or selectable text
inside the body. This body slot is an explicit exception to sealed item rendering;
it does not open Kit chrome, interaction feedback or control styling to hosts.

```kotlin
val eligibleIds = records.filter { it.enabled && it.selectable }.map { it.id }.toSet()
val list = rememberAndroidKitListState(eligibleIds)
val selection = AndroidKitListSelection(list.selection, onActionError = onError) {
    icon(deleteIcon, deleteLabel, destructive = true) { ids ->
        // Await confirmation and persistence. Cancellation/failure retains selection.
        deleteRecords(ids)
    }
    overflow {
        item(shareLabel, icon = shareIcon) { ids ->
            shareRecords(ids)
            AndroidKitListActionResult.Success
        }
    }
}
AndroidKitPage(
    title = title,
    selection = selection,
    actions = listOf(AndroidKitTextAction(selectLabel, { list.selection.activate() })),
) { clearance ->
    AndroidKitList(
        items = records,
        key = { it.id },
        state = list,
        contentPadding = clearance,
        enabled = { it.enabled },
        selectable = { it.selectable },
        onItemClick = onOpen,
        contextMenu = { record -> {
            item(selectLabel, onClick = { list.selection.activate(setOf(record.id)) })
        } },
        deleteAction = { record -> AndroidKitListDeleteAction({ onDelete(record.id) }) },
    ) { record ->
        AndroidKitCard(title = record.title) { Text(record.description) }
    }
}
```

## View and scrolling

Hosts switch `list.view` between `AndroidKitListView.List` and `.Grid`. Selection
belongs to the logical list and survives a view switch. List and grid keep separate
scroll states. Grid uses an adaptive column count by default; `gridColumns` accepts
Compose's `GridCells` as a layout option. Grid has **no swipe deletion**. Its menu
Delete and selection actions remain available.

Stable, nonblank, unique String IDs are required. Filtering/hiding is represented
by removing items from the supplied collection. Keyed Compose `animateItem` handles
insertions, removals and movement; selection feedback and chrome use brief transitions.
Compose honors the system animation duration scale.

Use `LazyListScope.androidKitListItems` in an existing Page/SearchPage list and
`LazyGridScope.androidKitListItems` in an existing grid. Both use the same Kit item
shell; the grid helper never enables swipe. Provide their shared `selectionState`
and a complete eligible ID set above the lazy viewport, including off-screen items.
Multiple declaration groups in one logical list must have globally unique keys.
Match the supplied eligible IDs to the current collection's enabled/selectable
items; deleted, hidden or filtered-out IDs must be removed from this set.

## Selection and surrounding chrome

Activation is host-triggered; long press always opens the menu in normal mode.
`activate(setOf(id))` can start with an item selected. `activate()` starts with zero.
Selecting none leaves the mode open. Select all toggles all/none over eligible
supplied items, including off-screen items; it does not include unloaded records.
New IDs are unselected. Removed or ineligible IDs are pruned.

Share the same `AndroidKitListSelection` with Page or SearchPage and the enclosing
`AndroidKitFloatingNavigation`. These owners replace the header, suppress ordinary
actions/search/floating controls and hide compact or expanded navigation. Suppression
is explicit: host-owned controls outside these owners must observe `state.isActive`.
The selection header ignores immersive title-bar hiding. Search retains its query
and scroll position, clears focus/IME on entry and hides recent-history controls.

X, system Back and Escape clear selection. While a bulk action runs, these exits,
row toggles, Select all and other bulk actions are disabled. Callbacks receive an
immutable selected-ID snapshot. Return `Success` only after successful completion;
it clears and closes selection. `Cancelled` and `Failure()` retain it.
`Failure(remainingIds)` retains only a subset of the submitted IDs, reconciled
against current eligibility. The required `onActionError` callback receives unexpected
exceptions; busy state is released. Hosts own confirmation, persistence, undo and
failure messages, and should use their lifecycle-aware state holder for durable work.
The UI coroutine is cancelled when its action bar leaves composition. Cancellation
never reports success.

Selection is deliberately not saved: recreation starts in normal mode. Hoist the
owner per logical page, not into a retained singleton or ViewModel. Normal navigation
away disposes the page owner. There is no automatic selection entry or persisted data.

## Delete and accessibility

Declare a typed `AndroidKitListDeleteAction` once. Kit appends a localized, destructive
Delete entry to the item menu and enables both swipe directions in List view. Disabled
or missing Delete disables swipe. Kit invokes the host callback and resets a retained
row; it does not remove records or assume confirmation succeeded.

Menu highlight and selection feedback remain visible above opaque host backgrounds.
Touch-and-hold, secondary mouse click, Menu/Shift+F10 and the accessibility menu action
use the shared context menu. Delete also has a custom accessibility action. Selection
uses full-row checkbox semantics, with a round tri-state Select all control and a
localized selected-count description. The leading gutter follows layout direction.

The demo catalog includes one interactive List showcase with List/Grid switching,
host-triggered selection, menu and swipe deletion, confirmation and bulk actions.
See [component ownership]({% link guides/component-contract.md %}).
