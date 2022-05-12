node("node1") {
    customImage = ""
    stage("git checkout"){
        checkout scm
    }
    stage("build docker") {
        customImage = docker.build("kandula-app")
    }
    stage("verify dockers") {
      sh "docker images"
    }
    stage("push to registry"){
    withDockerRegistry(credentialsId: '20d9099b-62c5-4d93-a8c8-eca1a5322d1a') {
    customImage.push()
   }
    }
}

