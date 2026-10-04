---
title: Maven repository
description: Public endpoint for compiled Android Kit artifacts.
permalink: /maven/
section: Distribution
---
## Endpoint

```text
https://mamby.github.io/android-kit-docs/maven/
```

**Available version: 0.1.53.** Check [releases]({{ '/releases/' | relative_url }})
for changes and companion downloads.

The Maven repository contains compiled AARs, POMs, Gradle module metadata,
checksums and the BOM under the standard `net/mamby/androidkit/` layout. It does not
contain implementation source JARs.

See [installation]({{ '/installation/' | relative_url }}) for the Gradle repository
configuration. Google Maven and Maven Central remain separate sources for Kit's
third-party dependencies.
