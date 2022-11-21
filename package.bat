mkdir dumploadfield
xcopy *.py dumploadfield
xcopy README.md dumploadfield
xcopy LICENSE dumploadfield
xcopy metadata.txt dumploadfield
xcopy icon.png dumploadfield
zip -r dumploadfield.zip dumploadfield
del /Q dumploadfield
rd dumploadfield 