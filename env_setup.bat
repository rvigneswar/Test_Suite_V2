@ECHO OFF
ECHO ===============================
ECHO Creating the python environment
ECHO ===============================
python -m venv env
ECHO =============
ECHO upgrading pip
ECHO =============
.\env\Scripts\python.exe -m pip install --upgrade pip
ECHO ==========================
ECHO Instaling dependencies
ECHO ==========================
.\env\Scripts\python.exe .\env\Scripts\pip.exe install -r .\requirements.txt
ECHO ======================
ECHO Activating environment
ECHO ======================
.\env\Scripts\activate.bat
