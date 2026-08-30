
[app]
title = Kefla IA
package.name = keflaia
package.domain = org.kefla
source.dir = .
source.include_exts = py,png,jpg,jpeg
requirements = python3,kivy,pygame,edge-tts,SpeechRecognition,google-genai,certifi,requests,urllib3,idna,charset-normalizer,pillow,six
orientation = portrait
android.permissions = INTERNET,RECORD_AUDIO
icon.filename = logo.png
android.api = 33
android.minapi = 21

[buildozer]
log_level = 2