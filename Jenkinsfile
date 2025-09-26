// Jenkinsfile for the To-Do Application CI Pipeline
pipeline {
    // Agent definition: Use any available agent (your Linux machine if Jenkins is running there)
    agent any

    // Environment variables needed throughout the pipeline
    environment {
        // Replace 'your-dockerhub-username' with your actual Docker Hub username
        DOCKER_IMAGE_NAME = "h8815/todowebapp"
        // Replace 'your-registry-url' if using ECR or another registry. For Docker Hub, it's just 'docker.io'
        DOCKER_REGISTRY = "docker.io" 
    }

    // Define the stages of your CI pipeline
    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out Git repository..."
                // Use the 'checkout scm' step to clone the repository configured in the Jenkins job
                checkout scm
            }
        }
        
        stage('Install Dev Dependencies') {
            steps {
                echo "Installing development dependencies..."
                // It's good practice to install dependencies in a virtual environment
                // or ensure the `pip` commands are isolated.
                // For a simple Jenkins setup, this assumes global python or a pre-configured agent.
                sh 'python3 -m pip install -r requirements-dev.txt'
            }
        }

        stage('Lint & Format Check') {
            steps {
                echo "Running linting and format checks..."
                // Run flake8 for code quality checks
                sh 'flake8 .'
                // Run black in check mode (to only report issues, not fix them)
                sh 'black --check .'
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                echo "Executing unit tests..."
                // Run your pytest suite
                sh 'pytest'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building the Docker image..."
                    // Get the short Git commit hash for tagging the Docker image
                    def gitCommitHash = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                    
                    // Build the Docker image with a tag based on the Git commit hash
                    sh "docker build -t ${DOCKER_IMAGE_NAME}:${gitCommitHash} ."
                    
                    // Tag it as 'latest' as well (optional, but convenient for local testing/dev)
                    sh "docker tag ${DOCKER_IMAGE_NAME}:${gitCommitHash} ${DOCKER_IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    echo "Pushing the Docker image to the registry..."
                    def gitCommitHash = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()

                    // Use Jenkins credentials for Docker login
                    // 'dockerhub-credentials' is a Jenkins Secret Text credential you must create
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD} ${DOCKER_REGISTRY}"
                        sh "docker push ${DOCKER_IMAGE_NAME}:${gitCommitHash}"
                        sh "docker push ${DOCKER_IMAGE_NAME}:latest" // Push latest tag too
                    }
                }
            }
        }
        
        // This stage will be for the GitOps handoff later, leave it commented for now
        // stage('Update GitOps Repo') {
        //     steps {
        //         echo "Updating the image tag in the GitOps repository..."
        //         // This is where Jenkins would clone your GitOps repo, update the values.yaml,
        //         // commit, and push. This is the handoff to ArgoCD.
        //     }
        // }
    }
    
    // Post-build actions (e.g., clean up, send notifications)
    post {
        always {
            echo "Pipeline finished."
            // Optionally add JUnit test report publishing here
            // junit '**/test-results/*.xml' // if your tests generate XML reports
        }
        failure {
            echo "Pipeline failed! Check logs for errors."
        }
    }
}