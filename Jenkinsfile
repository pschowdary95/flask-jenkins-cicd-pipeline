
pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = "${DOCKERHUB_CREDENTIALS_USR}/cicd-pipeline-project"
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install flake8
                    flake8 app/ tests/ --max-line-length=100
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install -r requirements-dev.txt
                    pytest tests/ -v
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} \
                    -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Push To DockerHub') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login \
                    -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin

                    for attempt in 1 2 3; do
                        if docker push ${IMAGE_NAME}:${IMAGE_TAG}; then
                            break
                        fi

                        if [ "$attempt" -eq 3 ]; then
                            exit 1
                        fi

                        echo "Push failed. Retrying in 10 seconds..."
                        sleep 10
                    done

                    for attempt in 1 2 3; do
                        if docker push ${IMAGE_NAME}:latest; then
                            break
                        fi

                        if [ "$attempt" -eq 3 ]; then
                            exit 1
                        fi

                        echo "Latest push failed. Retrying in 10 seconds..."
                        sleep 10
                    done
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f flask-app || true

                    docker run -d \
                    --restart unless-stopped \
                    -p 5001:5000 \
                    --name flask-app \
                    ${IMAGE_NAME}:${IMAGE_TAG}

                    sleep 5
                    docker inspect flask-app --format '{{.State.Status}}'
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded: ${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo 'Pipeline failed - check the stage logs above.'
        }
    }
}
