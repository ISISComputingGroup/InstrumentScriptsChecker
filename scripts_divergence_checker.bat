setlocal

REM Create local python environment from genie python on share
REM git clone https://github.com/ISISComputingGroup/ibex_utils.git
CALL \\isis\Shares\ISIS_Experiment_Controls_Public\ibex_utils\installation_and_upgrade\define_latest_genie_python.bat

%LATEST_PYTHON% -u scripts_divergence_checker.py
if %errorlevel% neq 0 exit /b %errorlevel%