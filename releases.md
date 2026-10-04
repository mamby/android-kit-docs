---
title: Releases
description: Published binaries and the documentation version they correspond to.
permalink: /releases/
section: Distribution
---
## Public binaries

Latest published version: **{{ site.data.binary_releases.latest }}**.

Each version includes four library AARs, the BOM, POM dependencies, Gradle module
metadata and artifact checksums. No implementation sources or source JARs are published.

{% for version in site.data.binary_releases.versions %}
### {{ version }}

- [Resource validator]({{ '/downloads/' | append: version | append: '/validate-androidkit-resources.gradle' | relative_url }}) and [validator SHA-256]({{ '/downloads/' | append: version | append: '/validate-androidkit-resources.gradle.sha256' | relative_url }}).
- [MIT license]({{ '/downloads/' | append: version | append: '/LICENSE.txt' | relative_url }}) and [third-party notices]({{ '/downloads/' | append: version | append: '/THIRD_PARTY_NOTICES.txt' | relative_url }}).
- [Release manifest with file checksums]({{ '/downloads/' | append: version | append: '/manifest.json' | relative_url }}).

{% endfor %}
## Release notes

### 0.1.53 — 4 October 2026

First public binary distribution through the [Maven endpoint]({{ '/maven/' | relative_url }}).
This packages the existing `0.1.53-SNAPSHOT` implementation as a fixed version;
component behavior and public APIs are unchanged.

- Four library AARs: `foundation`, `localization`, `compose` and `navigation3`.
- BOM, POM dependencies, Gradle module metadata and artifact checksums.
- [Resource validator]({{ '/downloads/0.1.53/validate-androidkit-resources.gradle' | relative_url }})
  and [validator SHA-256]({{ '/downloads/0.1.53/validate-androidkit-resources.gradle.sha256' | relative_url }}).
- [MIT license]({{ '/downloads/0.1.53/LICENSE.txt' | relative_url }}) and
  [third-party notices]({{ '/downloads/0.1.53/THIRD_PARTY_NOTICES.txt' | relative_url }}).
- [Release manifest with file checksums]({{ '/downloads/0.1.53/manifest.json' | relative_url }}).

No implementation sources or source JARs are published.

## Documentation version

The current documentation was prepared from the **{{ site.documentation_version }}**
Kit release.
Examples and migration notes describe that checkout; use documentation matching
the binary version your application consumes.

## Release policy

- Publish the library modules and BOM together.
- Preserve already published versions so existing builds remain reproducible.
- Publish a new version for corrections instead of overwriting a release.
- Include the MIT license and applicable third-party notices.
- Keep implementation source archives out of the public distribution.
