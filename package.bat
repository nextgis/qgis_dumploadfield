mkdir dumploadfield
mkdir dumploadfield\i18n
xcopy *.py dumploadfield
xcopy *.ui dumploadfield
xcopy README.md dumploadfield
xcopy LICENSE dumploadfield
xcopy metadata.txt dumploadfield
xcopy icon.png dumploadfield
xcopy i18n\dumploadfield_ru.ts dumploadfield\i18n\dumploadfield_ru.ts
lrelease dumploadfield\i18n\dumploadfield_ru.ts
del dumploadfield\i18n\dumploadfield_ru.ts
zip -r dumploadfield.zip dumploadfield
del /s /q dumploadfield
rmdir /s /q dumploadfield