node("node1") {
    customImage = ""
    stage("git checkout"){
         echo "###################################################"
         echo "Triggering Deployment, got notification from Github"
         echo "###################################################" 
         checkout scm
      }
    stage("build docker") {
        sh ("whoami;" ) 
        customImage = docker.build("marinapre/kandula")
    }
    stage("verify dockers") {
      sh "docker images"
      sh "trivy image --timeout 5m --severity CRITICAL,HIGH ${customImage}" 
    }
    stage("push to registry"){
      withDockerRegistry(credentialsId: 'dockerhub-cred') {
        customImage.push()
         }
    }
   stage ("deploy to K8S"){
            sh ("kubectl apply -f app_deployment.yaml; kubectl rollout restart deployment opsschool-app-marina")  
           }
   }

