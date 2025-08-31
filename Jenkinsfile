pipeline{
    agent any
    
    stages{
        stage("Code"){
            steps{
                echo "Cloning the code form github"
                git url:"https://github.com/h8815/ToDo-Web-app.git", branch:"main"
            }
        }
        stage("Build"){
            steps{
                echo "Building the application"
                sh "docker build -t todowebapp:latest ."
            }
        }
        stage("Deploy"){
            steps{
                echo "Deploying the application"
                sh "docker rm -f todowebapp || true"
                sh "docker run -d --name todowebapp -p 5000:5000 todowebapp:latest"
            }
        }
    }
}