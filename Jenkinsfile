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

        stage("Check Instrument Scripts Repo Branches up-to-date") {
            steps {
                bat """
                    call scripts_divergence_checker.bat
                """
            }
        }
    }
}