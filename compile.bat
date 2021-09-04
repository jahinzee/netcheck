@echo off
python -m nuitka netcheck.py --standalone --windows-icon-from-ico="res\ico\default_light.ico" --include-data-dir=res=res  --plugin-enable=tk-inter --windows-disable-console
pause