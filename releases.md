---
title: Releases
description: Published binaries and the documentation version they correspond to.
permalink: /releases/
section: Distribution
---
## Public binaries

**No binary versions have been published to this repository yet.**

This page will list each available version and its changes after its compiled
artifacts have been published and verified at the
[Maven endpoint]({{ '/maven/' | relative_url }}).

## Documentation snapshot

The current documentation was prepared from the **{{ site.documentation_version }}**
Kit checkout. This is a development snapshot, not an available public release.
Examples and migration notes describe that checkout; use documentation matching
the binary version your application consumes.

## Release policy

- Publish the library modules and BOM together.
- Preserve already published versions so existing builds remain reproducible.
- Publish a new version for corrections instead of overwriting a release.
- Include the MIT license and applicable third-party notices.
- Keep implementation source archives out of the public distribution.
