pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/SumanReddy568/Selenium-Python-Pytest-framework.git'
            }
        }
        
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'source venv/bin/activate && cd tests && pytest'
            }
        }
        
        stage('Publish Test Results') {
            steps {
                junit '**/test-results.xml'
            }
        }
    }
}
