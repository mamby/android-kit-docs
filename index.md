---
title: Overview
description: Reusable Android foundations, adaptive layouts and Jetpack Compose components.
permalink: /
home: true
section: Start here
---
<section class="hero">
  <p class="eyebrow">Kotlin · Jetpack Compose · AndroidX</p>
  <h1>A shared foundation for Android apps.</h1>
  <p class="hero-description">Build with opinionated components, adaptive layouts and a consistent interaction model. Android Kit brings navigation, settings, search and everyday controls together.</p>
  <div class="hero-actions">
    <a class="button button-primary" href="{{ '/installation/' | relative_url }}">Get started <span aria-hidden="true">→</span></a>
    <a class="button" href="{{ '/modules/' | relative_url }}">Explore the modules</a>
  </div>
  <div class="hero-meta"><span>Jetpack Compose</span><span>Android 8.0+</span><span>MIT licensed</span></div>
</section>

<div class="feature-grid">
  <section class="feature-card"><h2>Consistent components</h2><p>Kit owns control layout, typography and interaction. Supply typed content, state, callbacks and supported colors.</p></section>
  <section class="feature-card"><h2>Adaptive layouts</h2><p>Use pages, lists and navigation that account for window space, system insets and input methods.</p></section>
  <section class="feature-card"><h2>Connected settings</h2><p>One complete catalog powers settings pages and search, with persistent values and a shared history scope.</p></section>
  <section class="feature-card"><h2>Localized vocabulary</h2><p>Kit supplies translations for shared controls. Application content and domain-specific messages remain yours.</p></section>
</div>

## Explore the guides

<div class="guide-grid">
  <a class="guide-card" href="{{ '/guides/theme/' | relative_url }}"><h3>Themes and colors</h3><p>Set the palette and supported component colors.</p><span class="card-arrow" aria-hidden="true">Read the guide →</span></a>
  <a class="guide-card" href="{{ '/guides/settings/' | relative_url }}"><h3>Settings and search</h3><p>Declare one catalog for the entire settings experience.</p><span class="card-arrow" aria-hidden="true">Read the guide →</span></a>
  <a class="guide-card" href="{{ '/guides/list/' | relative_url }}"><h3>Lists and selection</h3><p>Connect item actions, grids and bulk selection.</p><span class="card-arrow" aria-hidden="true">Read the guide →</span></a>
  <a class="guide-card" href="{{ '/guides/section-card/' | relative_url }}"><h3>Section cards</h3><p>Present typed actions, controls and information.</p><span class="card-arrow" aria-hidden="true">Read the guide →</span></a>
</div>

## Documentation and distribution

These guides and compiled packages describe **Android Kit {{ site.data.binary_releases.latest }}**. Compiled
artifacts are available from this site's Maven repository. The
[installation guide]({{ '/installation/' | relative_url }}) explains the repository
configuration; the [release page]({{ '/releases/' | relative_url }}) lists
published versions and their companion downloads.

Android Kit's implementation repository is maintained privately. Its distributed
binaries, documentation and examples remain MIT licensed. See the
[license and notices]({{ '/license/' | relative_url }}).
