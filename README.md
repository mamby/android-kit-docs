# Android Kit Documentation

Public documentation for Android Kit's Kotlin and Jetpack Compose modules.

**Website:** https://mamby.github.io/android-kit-docs/

The implementation is maintained in a separate private repository. This
repository contains documentation, usage examples, the MIT license, third-party
notices and the public Maven directory for compiled releases.

Android Kit `0.1.53` is published; see the site's release page for availability.

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

Build all five publications into Kit's `staging-repository`, then import them:

```powershell
python scripts/maven_release.py import --source <kit>/staging-repository `
  --version 0.1.53 --validator <kit>/gradle/validate-androidkit-resources.gradle `
  --license <kit>/LICENSE --notices <kit>/THIRD_PARTY_NOTICES.md
python scripts/maven_release.py check
```

The importer validates POMs, Gradle metadata and binary archives, refuses source
JARs and refuses to overwrite any versioned file with different contents. It
preserves earlier versions and generates checksums and a release manifest.
Update the release page, installation version and documentation version, then
commit and push. Pages verifies binary checksums before and after Jekyll builds.
Implementation source never belongs in this repository; the public validator is
a companion host build script.

## License

MIT. See [LICENSE](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).
