setlocal

CALL \\isis\Shares\ISIS_Experiment_Controls_Public\ibex_utils\installation_and_upgrade\define_latest_genie_python.bat

%LATEST_PYTHON% -u scripts_divergence_checker.py

if %errorlevel% neq 0 (
    set errcode = %ERRORLEVEL%
    call \\isis\Shares\ISIS_Experiment_Controls_Public\ibex_utils\installation_and_upgrade\remove_genie_python.bat %LATEST_PYTHON_DIR%
    EXIT /b !errcode!
)

call \\isis\Shares\ISIS_Experiment_Controls_Public\ibex_utils\installation_and_upgrade\remove_genie_python.bat %LATEST_PYTHON_DIR%
