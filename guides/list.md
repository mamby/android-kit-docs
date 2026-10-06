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

`AndroidKitPage` supplies Kit-owned start/end margins along with its measured
system/chrome clearance. Pass its padding directly to `AndroidKitList.contentPadding`;
the list/grid does not add a second horizontal margin. A standalone list uses
only the `contentPadding` supplied by its owner.

Hosts switch `list.view` between `AndroidKitListView.List` and `.Grid`. List is the
default. Use the complete `AndroidKitList` component in either mode; Kit owns the
lazy container, item spacing and adaptive grid columns. Selection
belongs to the logical list and survives a view switch. List and grid keep separate
scroll states. Grid uses Kit's adaptive column count. Grid has **no swipe deletion**. Its menu
Delete and selection actions remain available.

Stable, nonblank, unique String IDs are required. Filtering/hiding is represented
by removing items from the supplied collection. Keyed Compose `animateItem` handles
insertions, removals and movement; selection feedback and chrome use brief transitions.
Compose honors the system animation duration scale.

The low-level lazy-list/grid item helpers are internal. Hosts cannot attach Kit
list interactions to a separately configured lazy container or override grid
column geometry. Supply a complete eligible ID set to the list state above the
lazy viewport, including off-screen items. Match those IDs to the collection's
enabled/selectable items; deleted, hidden or filtered-out IDs must be removed
from the set.

## Migration from 0.1.59

Replace host-owned `LazyColumn`/`LazyVerticalGrid` containers using
`androidKitListItems` with `AndroidKitList` and `rememberAndroidKitListState`.
Pass the page padding directly as `contentPadding`, keep item bodies visual-only,
and share the state's selection with page and navigation chrome. Remove
`gridColumns`; Kit determines the adaptive grid geometry. Both List and Grid
modes remain available, with their existing mode-specific interaction behavior.

## Selection and surrounding chrome

Activation is host-triggered; long press always opens the menu in normal mode.
`activate(setOf(id))` can start with an item selected. `activate()` starts with zero.
Selecting none leaves the mode open. Select all toggles all/none over eligible
supplied items, including off-screen items; it does not include unloaded records.
New IDs are unselected. Removed or ineligible IDs are pruned.
Select all and the selected count share one pill. Its checkbox has two states:
checked when every eligible item is selected, unchecked otherwise. Tapping the
pill with a partial selection selects all eligible items; tapping it when all
are selected clears the selection. Items use the same circled check icon when
selected and the same empty circle when unselected.
List items place the icon in a leading gutter. Grid items overlay it at the card's
top-start corner without narrowing the body; the corner follows layout direction.

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
uses full-row checkbox semantics, with a two-state Select all/count pill and a
localized selected-count description on that control. The leading gutter follows
layout direction.

The demo catalog includes one interactive List showcase with List/Grid switching,
host-triggered selection, menu and swipe deletion, confirmation and bulk actions.
See [component ownership]({{ site.baseurl }}{% link guides/component-contract.md %}).
