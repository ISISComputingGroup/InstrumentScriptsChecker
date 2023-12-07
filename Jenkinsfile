#!groovy

pipeline {

    // using same agnert as ConfigCheck job
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

        stage("Check Instrument Scripts Repo Branches up-to-date") {
            steps {
                echo "Checking Instrument Scripts Repo Branches up-to-date"
                timeout(time: 1, unit: 'HOURS') {
                    bat """
                        call scripts_divergence_checker.bat
                    """
                }
            }
        }
    }
}