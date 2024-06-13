pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Specify the branch explicitly to avoid mismatch
                git branch: 'main', url: 'https://github.com/SumanReddy568/Selenium-Python-Pytest-framework.git'
            }
        }

        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Capture potential errors within the stage
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                        sh 'source venv/bin/activate && cd tests && pytest'
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
