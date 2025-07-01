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
                sh "docker build -t todoapp:latest ."
            }
        }
        stage("Deploy"){
            steps{
                echo "Deploying the application"
                sh "docker rm -f todoapp || true"
                sh "docker run -d --name todoapp -p 5000:5000 todoapp:latest"
            }
        }
    }
}