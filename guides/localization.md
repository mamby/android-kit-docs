---
title: Localization
description: Keep shared component vocabulary in Kit and application content in your own resources.
permalink: /guides/localization/
section: Foundations
---
Android Kit translates shared component vocabulary through its own Android
resources. The active application configuration selects the component language.
Predefined labels cannot be replaced through Kit APIs or host resource overrides.

## Application-owned text

Use your application's resources for domain content, custom actions, option values
and messages. Resolve localized labels before entering non-composable action
builders such as the flyout DSL.

Host-owned Settings entries can supply `AndroidKitSettingsSearchTerms` for
cross-language matching. Their visible text remains application-owned. Built-in
Settings search terms are supplied by Kit.

## Declare supported languages

Declare each application-supported language in the host's `gradle.properties`:

```properties
androidKitSupportedLocales=en,fr,ar
```

Keep this declaration aligned with the application's language picker and Android
locale configuration. Choose languages supported by the consumed Kit release.

## Required resource validation

Every consuming application must apply the version-matched resource validation
script after its Android application plugin:

```kotlin
apply(from = rootProject.file("gradle/validate-androidkit-resources.gradle"))
```

Download the [{{ site.data.binary_releases.latest }} validator]({{ '/downloads/' | append: site.data.binary_releases.latest | append: '/validate-androidkit-resources.gradle' | relative_url }})
and commit it as `gradle/validate-androidkit-resources.gradle` in the Android
project. Its [SHA-256 checksum]({{ '/downloads/' | append: site.data.binary_releases.latest | append: '/validate-androidkit-resources.gradle.sha256' | relative_url }})
and the full [release manifest]({{ '/downloads/' | append: site.data.binary_releases.latest | append: '/manifest.json' | relative_url }})
are available for verification. Keep the script matched to the Kit version;
ordinary application builds use the committed copy without downloading scripts.

The build gate checks application resource directories and resolved dependency
AARs against the contract packaged in the Compose AAR. It rejects:

- Host or dependency overrides using the reserved `androidkit_` prefix.
- Application languages unsupported by Kit.
- Missing or incompatible contracts and incomplete bundled translations.
- Incompatible legacy Android resource qualifiers.

The gate is attached to packaging and check tasks. A Kotlin compilation alone
does not verify the resource contract. Maven AAR dependencies require no local
producer-variant setup.

## Locale identifiers

Use standard language tags such as `id`, `he` and `yi` in declarations and language
pickers. Android resource directories use their legacy qualifiers `in`, `iw` and
`ji` where required by Android resource lookup.

## Language changes and search history

Kit controls respond to the host application's locale configuration. Application
content still needs its own translated resources. Settings owns one shared search
scope; independent content searches own their page-specific histories. See
[Settings]({{ site.baseurl }}{% link guides/settings.md %}) and
[search pages]({{ site.baseurl }}{% link guides/search-page.md %}).
