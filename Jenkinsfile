#!groovy

pipeline {

    agent {  
        label {
            label "ConfigCheck"
        }
    }
  
    triggers {
        cron('H 1 * * *')
    }
  
    stages {  

        stage("Checkout") {
            steps {
                timeout(time: 2, unit: 'HOURS') {
                    retry(5) {
                        checkout scm
                    }
                }
            }
        }   

        stage("Dependencies") {
            steps {
                echo "Installing local genie python"
                timeout(time: 1, unit: 'HOURS') {
                    bat """
                    setlocal
                    set WORKWIN=%WORKSPACE:/=\\%
                    rd /s /q %WORKWIN%\\Python3
                    call build\\update_genie_python.bat ${env.WORKSPACE}\\Python3
                    if %errorlevel% neq 0 exit /b %errorlevel%
                 """
                }
            }
        }    

        stage("Check Instrument Scripts Repo Branches up-to-date") {
            steps {
                echo "Checking Instrument Scripts Repo Branches up-to-date"
                timeout(time: 5, unit: 'HOURS') {
                    bat """
                        call scripts_divergence_checker.bat
                    """
                }
            }
        }
    }
}