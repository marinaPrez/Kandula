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
    withDockerRegistry(credentialsId: '5f37e4d2-30ef-43cc-83eb-5fffb84a4876') {
    customImage.push()
   }
    }
}

