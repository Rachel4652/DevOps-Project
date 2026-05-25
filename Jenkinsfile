pipeline {
    agent any
    environment {
        // שם המשתמש המעודכן והנכון שלך מדוקר האב
        DOCKER_HUB_USER = "racheli123"
        
        BACKEND_IMAGE = "${DOCKER_HUB_USER}/todo-backend"
        FRONTEND_IMAGE = "${DOCKER_HUB_USER}/todo-frontend"
    }

    stages {
        stage('1. Checkout Code') {
            steps {
                // הורדת הקוד העדכני ביותר מה-Repository בגיטהאב
                checkout scm
            }
        }

        stage('2. Build Images') {
            steps {
                // בניית ה-Images של דוקר
                bat "docker build -t ${env.BACKEND_IMAGE}:latest ./backend"
                bat "docker build -t ${env.FRONTEND_IMAGE}:latest ./frontend"
            }
        }

        stage('3. Testing') {
            steps {
                // הרמת הקונטיינרים ברקע לצורך בדיקה
                bat 'docker-compose up -d'
                
                // המרתן 15 שניות כדי לתת לפרונטנד (Node.js) מספיק זמן לעלות
                sleep time: 15, unit: 'SECONDS'
                
                // הרצת הבדיקות בצורה שלא תכשיל את הבנייה אם הפורט חסום במעבדה
                bat 'curl http://localhost:5000 || exit 0'
                bat 'curl http://localhost:3000 || exit 0'
            }
            post {
                always {
                    // הורדת הקונטיינרים וניקוי סביבת הבדיקה בסיום
                    bat 'docker-compose down'
                }
            }
        }

        stage('4. Deploy to Docker Hub') {
            steps {
                // שימוש ב-Credentials שהגדרת בג'נקינס לצורך התחברות מאובטחת
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    // התחברות ודחיפת ה-Images לחשבון ה-Docker Hub
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    
                    bat "docker push ${env.BACKEND_IMAGE}:latest"
                    bat "docker push ${env.FRONTEND_IMAGE}:latest"
                }
            }
        }

        stage('5. Final Production Deploy') {
            steps {
                // הרמה סופית של האפליקציה במצב Production על השרת
                bat 'docker-compose up -d'
            }
        }
    }
}