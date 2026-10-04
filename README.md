# Android Kit Documentation

Public documentation for Android Kit's Kotlin and Jetpack Compose modules.

**Website:** https://mamby.github.io/android-kit-docs/

The implementation is maintained in a separate private repository. This
repository contains documentation, usage examples, the MIT license, third-party
notices and the public Maven directory for compiled releases.

Binary publication is pending; see the site's release page for availability.

## Publishing the site

The `Publish documentation` GitHub Actions workflow builds this repository with
GitHub's Jekyll Pages action, checks generated links and the search index, and
deploys successful builds to GitHub Pages. Pushes to `main` publish automatically;
pull requests build and validate without deploying.

In repository **Settings → Pages**, the publishing source is **GitHub Actions**.

## Updating guides

Public usage guides are imported from the matching Kit checkout with:

```powershell
python scripts/import_guides.py --source <path-to-android-kit>
```

The importer includes only selected Markdown usage guides, never library source.
Review imported examples and update `documentation_version` in `_config.yml` when
preparing documentation for a different version.

## Maven distribution

Publish compiled artifacts beneath `maven/` using the standard Maven directory
layout. Preserve each released version, POM dependencies, Gradle metadata and BOM.
Do not publish implementation source JARs. The Pages build retains binary files
unchanged alongside the documentation.

## License

MIT. See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).
