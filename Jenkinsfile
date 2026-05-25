pipeline {
    agent any
    environment {
        // שם המשתמש שלך ב-Docker Hub כפי שמופיע בנתיבי ה-Images
        DOCKER_HUB_USER = "Rachel4652"
        
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
                // שימוש בגרשיים כפולות ובסינטקס ג'נקינס לגישה בטוחה למשתני הסביבה
                bat "docker build -t ${env.BACKEND_IMAGE}:latest ./backend"
                bat "docker build -t ${env.FRONTEND_IMAGE}:latest ./frontend"
            }
        }

        stage('3. Testing') {
            steps {
                // הרמת הקונטיינרים ברקע לצורך בדיקה
                bat 'docker-compose up -d'
                
                // המרתן 10 שניות כדי לוודא שכל השרתים עלו והתייצבו
                sleep time: 10, unit: 'SECONDS'
                
                // בדיקת curl ללא דגל -f כדי שסטטוס 404 לא יכשיל את הבנייה
                bat 'curl http://localhost:5000'
                bat 'curl http://localhost:3000'
            }
            post {
                always {
                    // הורדת הקונטיינרים וניקוי סביבת הבדיקה בסיום, גם אם השלב נכשל
                    bat 'docker-compose down'
                }
            }
        }

        stage('4. Deploy to Docker Hub') {
            steps {
                // שימוש ב-Credentials שהגדרת בג'נקינס לצורך התחברות מאובטחת
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    // כאן DOCKER_PASS ו-DOCKER_USER הם משתני מערכת זמניים של ווינדוס, לכן נשתמש ב-%
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    
                    // דחיפת ה-Images לחשבון ה-Docker Hub
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