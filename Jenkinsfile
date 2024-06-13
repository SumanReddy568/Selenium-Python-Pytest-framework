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
                        sh '. venv/bin/activate && cd tests && pytest'
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
