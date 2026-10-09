=== CCTV Video Directory ===
Contributors: kevintyson
Requires at least: 6.2
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later

Search Claremont CCTV videos with program/channel filters, sorting, optional regular expressions, and corresponding school board meeting pages.

== Installation ==
1. In WordPress, go to Plugins > Add New Plugin > Upload Plugin.
2. Select cctv-video-directory.zip, install it, and activate it.
3. Edit or create a public page. Add a Shortcode block containing:
   [cctv_directory]
4. Publish the page. A full-width page template is recommended.

No API keys, sign-in for visitors, build tools, or separate database setup are needed. This requires a WordPress installation that permits custom plugins.

== Updating the directory ==
The plugin includes 4,252 videos, including the October 7, 2026 school board meeting, so it works immediately.

WordPress stores the complete directory on your server. A daily scheduled job retrieves CCTV collections and meeting pages in small steps. WordPress scheduled tasks depend on site visits; low-traffic sites should have their host schedule wp-cron.php regularly.

For an immediate source refresh, open Settings > CCTV Directory and press Refresh from CCTV. Keep that page open until it reports completion. A full refresh visits hundreds of source pages and can take several minutes. Closing the page allows scheduled tasks to continue the job, but it may take longer. The previous directory stays available until a complete refresh succeeds. Source failures leave the previous directory intact and show an administrator status message.

Visitors search locally without waiting for a server search. Browser storage is automatic and optional; the app continues if storage is unavailable. When a changed list is available, an update notice lets visitors apply it. The visitor Update video list button reloads the latest list already published by WordPress; it does not start a source crawl. Administrators use Settings > CCTV Directory to retrieve new material from CCTV.

== External services ==
Server refreshes read public metadata from https://reflect-claremont.cablecast.tv and meeting pages from https://csbmn.claremontv.org/. Thumbnails are loaded from CCTV. Watch and meeting links open the corresponding external pages. Videos are hosted by CCTV, not copied to WordPress. No search terms are sent to these services by the directory.

== Display and compatibility ==
The responsive directory is embedded in a same-origin frame to isolate it from theme styles. Use a full-width page for the best desktop layout; narrow pages, tablets and phones use the responsive layout. WordPress security plugins must allow public access to the plugin's admin-ajax.php view, manifest and catalog actions. Administrator refresh actions require administrator permission and a WordPress nonce.

== Removal ==
Deactivating stops scheduled refreshes. Saved catalog data remains in WordPress options to preserve the directory when reactivating.
