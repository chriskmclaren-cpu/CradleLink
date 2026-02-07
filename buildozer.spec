[app]
title = NexusLink
package.name = nexuslink
package.domain = lupine.studio
source.dir = .
source.include_exts = py,png,json,kv
version = 1.1.0

# FIXED: Added openssl (critical for connection) and requests dependencies
requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna,openssl

orientation = portrait
android.permissions = INTERNET
icon.filename = Bloodfang.png

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
