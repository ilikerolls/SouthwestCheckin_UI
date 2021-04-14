@echo off

WHERE pyuic55 >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
	ECHO pyuic5 wasn't found
	echo "Installing with pip install pyuic5-tool"
	
	python -m pip install --upgrade pip
	pip install pyuic5-tool
)

For %%A in ("%cd%/*.ui") do (
    Set UI_FILE=%%~nxA
)

echo "Generating Ui_main_Form.py from %UI_FILE%"
pyuic5 -x %UI_FILE% -o Ui_main_Form.py
pause