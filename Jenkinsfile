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
      withDockerRegistry(credentialsId: 'dockerhub-cred') {
        customImage.push()
         }
    }
   stage ("deploy to K8S"){
            sh ("pwd;  kubectl apply -f app_deployment.yaml; kubectl rollout restart deployment opsschool-app-marina")  
           }
   }

