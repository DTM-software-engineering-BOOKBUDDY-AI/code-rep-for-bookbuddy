@echo off
echo Fixing Flask and test dependencies...
pip uninstall -y flask pytest-flask
pip install flask==2.2.5 pytest-flask==1.2.0

echo Dependencies have been fixed. Now you can run tests. 