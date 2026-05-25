pipeline {
    agent any
    environment {
        // ---- שני את השם פה לשם המשתמש שלך ב-Docker Hub ----
        DOCKER_HUB_USER = "your_dockerhub_username"
        
        BACKEND_IMAGE = "${DOCKER_HUB_USER}/todo-backend"
        FRONTEND_IMAGE = "${DOCKER_HUB_USER}/todo-frontend"
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('2. Build Images') {
            steps {
                // שימוש ב-bat במקום sh עבור ווינדוס
                bat 'docker build -t %BACKEND_IMAGE%:latest ./backend'
                bat 'docker build -t %FRONTEND_IMAGE%:latest ./frontend'
            }
        }

        stage('3. Testing') {
            steps {
                bat 'docker-compose up -d'
                
                sleep time: 10, unit: 'SECONDS'
                
                // בדיקת curl מותאמת לווינדוס (או שימוש ב-curl המובנה)
                bat 'curl -f http://localhost:5000'
                bat 'curl -f http://localhost:3000'
            }
            post {
                always {
                    bat 'docker-compose down'
                }
            }
        }

        stage('4. Deploy to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    // התחברות והעלאה מותאמת לווינדוס
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push %BACKEND_IMAGE%:latest'
                    bat 'docker push %FRONTEND_IMAGE%:latest'
                }
            }
        }

        stage('5. Final Production Deploy') {
            steps {
                bat 'docker-compose up -d'
            }
        }
    }
}