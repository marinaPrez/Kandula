pipeline {
    agent any
    triggers {
       githubPush()
    }
    stages {
        stage('Checkout Project from Github') {
            steps {
                checkout scm
                echo "Project has been checked out from Git"
            }
          }
        stage("build docker") {
          steps { 
          customImage = docker.build("marinapre/kandulaApp")
           } } 
    }
}
