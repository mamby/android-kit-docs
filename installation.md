---
title: Installation
description: Add Android Kit's Maven repository and select the modules your application needs.
permalink: /installation/
section: Start here
---
<div class="callout" markdown="1">
**Binary publication is pending.** This site currently provides documentation.
The Maven endpoint has no Kit releases yet, so the configuration below will work
once a version is listed on the [release page]({{ '/releases/' | relative_url }}).
</div>

## Requirements

- An Android application using Kotlin and Jetpack Compose.
- Android 8.0 (API 26) or newer at runtime.
- A toolchain compatible with the Kit version you choose. The documentation
  snapshot was built against Android API 37.

## Add the repository

Add Kit's public repository to your Android project's `settings.gradle.kts`.
Keep Google Maven and Maven Central for AndroidX and other dependencies.

```kotlin
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
        maven {
            name = "AndroidKit"
            url = uri("https://mamby.github.io/android-kit-docs/maven/")
            content {
                includeGroup("net.mamby.androidkit")
            }
        }
    }
}
```

Public host repositories should resolve a published version from this endpoint
by default. Maven Local can remain an opt-in development source on a maintainer's
machine; contributors and GitHub Actions do not have that machine's local cache.

## Select a version and modules

Set `androidKitVersion` in your project's `gradle.properties` to an exact version
listed on the [release page]({{ '/releases/' | relative_url }}). Add the BOM and
the modules you use to your application's `build.gradle.kts`:

```kotlin
dependencies {
    val androidKitVersion = providers.gradleProperty("androidKitVersion").get()
    implementation(platform("net.mamby.androidkit:bom:$androidKitVersion"))
    implementation("net.mamby.androidkit:compose")
    implementation("net.mamby.androidkit:navigation3")
}
```

The BOM aligns module versions. `navigation3` is only needed when you use Kit's
Navigation 3 state and page renderer. See [modules]({{ '/modules/' | relative_url }})
for each artifact's responsibility.

## Integrate with your app

Place Kit's Compose components beneath `AndroidKitTheme`. Configure the palette
through `AndroidKitThemeDefinition`; keep typography, geometry and shared control
rendering Kit-owned. Start with [themes]({% link guides/theme.md %}) and the
[component contract]({% link guides/component-contract.md %}).

Consuming applications must also apply the resource validation build gate and
declare their supported locales. See [localization]({% link guides/localization.md %}).

## Include the license

Retain the MIT copyright and permission notice when redistributing Kit, including
inside an application. Preserve applicable third-party notices as well. The
private implementation repository is not needed to download or use a published
binary. See [license and notices]({{ '/license/' | relative_url }}).
