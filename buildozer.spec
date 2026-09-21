[app]

# (str) Title of your application
title = Calculator

# (str) Package name
package.name = calculator

# (str) Package domain (needed for android packaging)
package.domain = org.vanraj

# (str) Source where the app lives
source.dir = .

# (list) Source files to include (let it include py, kv, png, jpg)
source.include_exts = py,kv,png,jpg

# (list) Application requirements
requirements = python3,kivy

# (str) Version of the application
version = 1.0

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[android]

# (int) Android API version to use
android.api = 33

# (int) Minimum API version
android.minapi = 21

# (list) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a
