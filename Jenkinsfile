#!groovy

pipeline {

    agent {  
        label {
            label "scriptdivergencechecker"
        }
    }

    environment {
    }
  
    triggers {
        cron('H 1 * * *')
    }
  
    stages {  
        
        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Dependencies") {
        steps {
          echo "Installing local genie python"
          bat """
                setlocal
                set WORKWIN=%WORKSPACE:/=\\%
                rd /s /q %WORKWIN%\\Python3
                call build\\update_genie_python.bat ${env.WORKSPACE}\\Python3
                if %errorlevel% neq 0 exit /b %errorlevel%
          """
        }
    }    

        stage("Check Instrument Scripts Repo Branches up-to-date") {
            steps {
                bat """
                    call scripts_divergence_checker.bat
                """
            }
        }
    }
}