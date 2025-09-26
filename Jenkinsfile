pipeline {
  agent any

  environment {
    DOCKER_REPO = "your-dockerhub-username/flask-todo"   // change this
    IMAGE_TAG = "${env.BUILD_ID}"                        // unique per build
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Run unit tests') {
      steps {
        // Use the host Docker to run tests inside a Python container (no need to have Python on Jenkins host)
        sh '''
          docker run --rm -v "$PWD":/app -w /app python:3.10-bullseye \
            bash -lc "pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt && pytest -q"
        '''
      }
    }

    stage('Build Docker image') {
      steps {
        script {
          // prefer using commit hash tag
          def shortCommit = sh(returnStdout: true, script: "git rev-parse --short=7 HEAD").trim()
          env.IMAGE_TAG = shortCommit
        }
        sh "docker build -t ${DOCKER_REPO}:${IMAGE_TAG} -t ${DOCKER_REPO}:latest ."
      }
    }

    stage('Push image to DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${DOCKER_REPO}:${IMAGE_TAG}
            docker push ${DOCKER_REPO}:latest
          '''
        }
      }
    }
  }

  post {
    always {
      // optional cleanup: remove built images on Jenkins host to save disk
      sh "docker rmi ${DOCKER_REPO}:${IMAGE_TAG} || true"
    }
    success {
      echo "Build and push succeeded: ${DOCKER_REPO}:${IMAGE_TAG}"
    }
    failure {
      echo "Build failed"
    }
  }
}
