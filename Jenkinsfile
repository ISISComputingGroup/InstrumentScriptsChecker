#!groovy

pipeline {

    // using same agnert as ConfigCheck job
    agent {  
        label {
            label "ConfigCheck"
        }
    }
  
    triggers {
        cron('H * * * *')
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

    post {
        always { 
        logParser ([
            // projectRulePath: 'path/to/rules/file/on/the/node',
            parsingRulesPath: '/parse_rules',
            showGraphs: true, 
            unstableOnWarning: true, 
            useProjectRule: false,
        ])
        }
    }
}