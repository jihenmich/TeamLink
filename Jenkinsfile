pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/jihenmich/TeamLink.git'  
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker build -t teamlink-backend backend/'  
                sh 'docker build -t teamlink-frontend frontend/'  
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Check Running Containers') {
            steps {
                sh 'docker ps'
            }
        }

        /*
        stage('Stop Services (Optional)') {
            steps {
                sh 'docker compose down'  // Falls die Container nach dem Test gestoppt werden sollen
            }
        }
        */
    }
}
