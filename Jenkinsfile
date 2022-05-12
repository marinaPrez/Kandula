node("node1") {
    customImage = ""
    stage("git checkout"){
        checkout scm
    }
    stage("build docker") {
        customImage = docker.build("kandula")
    }
    stage("verify dockers") {
      sh "docker images"
    }
    stage("push to registry"){
    withDockerRegistry(credentialsId: '7bcacd66-7e09-40e5-a59b-5b505e0b82d7') {
    customImage.push()
   }
    }
}

