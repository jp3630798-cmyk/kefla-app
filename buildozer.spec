
[app]
title = Kefla IA
package.name = keflaia
version = 0.2
package.domain = org.kefla
source.dir = .
source.include_exts = py,png,jpg,jpeg
requirements = python3,kivy,pygame,edge-tts,SpeechRecognition,google-genai,certifi,requests,urllib3,idna,charset-normalizer,pillow,six
orientation = portrait
android.permissions = INTERNET,RECORD_AUDIO
icon.filename = logo.png
android.api = 31
android.sdk = 31
android.ndk = 25b
android.minapi = 21

[buildozer]
log_level = 2
# (str) Android build tools version to use
android.build_tools_version = 31.0.0
