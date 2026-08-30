
[app]
title = Kefla IA
package.name = keflaia
version = 0.2
package.domain = org.kefla
source.dir = .
source.include_exts = py,png,jpg,jpeg
requirements = python3,kivy,pygame,certifi,requests
orientation = portrait
android.permissions = INTERNET,RECORD_AUDIO
icon.filename = logo.png
android.api = 33
android.sdk = 33
android.ndk = 25b
android.minapi = 21

[buildozer]
log_level = 2
# (str) Android build tools version to use
android.build_tools_version = 31.0.0
android.accept_sdk_license = True
