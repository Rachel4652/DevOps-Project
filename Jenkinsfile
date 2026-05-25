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
                // מוריד את הקוד העדכני ביותר מ-GitHub שלך
                checkout scm
            }
        }

        stage('2. Build Images') {
            steps {
                // בונה את תמונות הדוקר לפי ה-Dockerfiles שבתיקיות
                sh 'docker build -t ${BACKEND_IMAGE}:latest ./backend'
                sh 'docker build -t ${FRONTEND_IMAGE}:latest ./frontend'
            }
        }

        stage('3. Testing') {
            steps {
                // מריץ את המערכת באופן זמני כדי לבדוק שהיא תקינה
                sh 'docker-compose up -d'
                
                // ממתין 10 שניות כדי לתת לשרתים זמן לעלות
                sleep time: 10, unit: 'SECONDS'
                
                // בדיקה שה-Backend מגיב (פורט 5000)
                sh 'curl -f http://localhost:5000 || exit 1'
                
                // בדיקה שה-Frontend מגיב (פורט 3000)
                sh 'curl -f http://localhost:3000 || exit 1'
            }
            post {
                always {
                    // מוריד את קונטיינרי הבדיקה כדי שלא יתפסו מקום סתם
                    sh 'docker-compose down'
                }
            }
        }

        stage('4. Deploy to Docker Hub') {
            steps {
                // מתחבר ל-Docker Hub בצורה מאובטחת ומעלה את התמונות
                // (מניח שהגדרת Credentials ב-Jenkins בשם 'docker-hub-creds')
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push ${BACKEND_IMAGE}:latest'
                    sh 'docker push ${FRONTEND_IMAGE}:latest'
                }
            }
        }

        stage('5. Final Production Deploy') {
            steps {
                // השלב הסופי: הרמת המערכת האמיתית שתישאר באוויר עבור הבדיקה של המורה
                sh 'docker-compose up -d'
            }
        }
    }
}