[app]
title = Calculator
package.name = calculator
package.domain = org.vanraj
source.dir = .
source.include_exts = py,kv,png,jpg
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
