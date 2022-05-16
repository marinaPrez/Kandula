node("node1") {
    customImage = ""
    stage("git checkout"){
         echo "###################################################"
         echo "Triggering Deployment, got notification from Github"
         echo "###################################################" 
         checkout scm
      }
    stage("build docker") {
        customImage = docker.build("marinapre/kandula")
    }
    stage("verify dockers") {
      sh "docker images"
    }
    stage("push to registry"){
      withDockerRegistry(credentialsId: '125075c2-3206-43a3-88cb-364fa0691ba3') {
        customImage.push()
         }
    }
   stage ("deploy to K8S"){
            sh ("pwd;  kubectl apply -f app_deployment.yaml")  
           }
   }

