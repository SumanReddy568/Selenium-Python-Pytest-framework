pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/SumanReddy568/Selenium-Python-Pytest-framework.git'
            }
        }

        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                        // Activate venv, run pytest with browser_name argument
                        sh '''
                        . venv/bin/activate
                        pytest --html=./reports/Pytest_Test_Run_Report.html -n auto --browser_name=chrome
                        '''
                    }
                }
            }
        }

        stage('Publish Test Results') {
            steps {
                junit '**/tests/test-results.xml'
            }
        }
    }
}

