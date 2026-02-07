[app]
title = NexusLink
package.name = nexuslink
package.domain = lupine.studio
source.dir = .

# UPDATE: Added "PNG" (caps) just in case the extension is hiding something.
source.include_exts = py,png,json,kv,jpg,PNG

version = 1.2.0

# REQUIREMENTS: Lightweight mode (No heavy libraries that cause crashes)
requirements = python3,kivy

orientation = portrait
android.permissions = INTERNET

# ICON: Matches your screenshot exactly
icon.filename = Bloodfang.png

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
