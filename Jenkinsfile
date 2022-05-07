pipeline {
    agent { label 'docker_node'}
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
                  script {    customImage = docker.build("marinapre/kandulaApp")}
           } } 
    }
}
