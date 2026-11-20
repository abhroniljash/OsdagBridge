@echo off
setlocal enabledelayedexpansion
set TARGET=
for %%A in (%*) do (
    set ARG=%%~A
    if "!ARG:~-4!"==".tex" set TARGET=!ARG!
)
if defined TARGET (
    "D:\IIT Boumby\tectonic_bin\tectonic.exe" "!TARGET!"
) else (
    "D:\IIT Boumby\tectonic_bin\tectonic.exe" %*
)
