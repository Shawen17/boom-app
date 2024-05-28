pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('github-token') // ID of the secret text in Jenkins
        GITHUB_USERNAME = 'shawen17'
        IMAGE_NAME = "ghcr.io/${GITHUB_USERNAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat 'docker-compose build'
                }
            }
        }

        stage('Login to GHCR') {
            steps {
                script {
                    bat "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login ghcr.io -u ${GITHUB_USERNAME} --password-stdin"
                }
            }
        }

        stage('Tag and Push Images') {
            steps {
                script {
                    // Get the list of services from docker-compose file
                    def services = bat(script: "docker-compose config --services", returnStdout: true).trim().split('\r?\n')

                    // Tag and push each service
                    services.each { service ->
                        def imageId = bat(script: "docker-compose images -q ${service}", returnStdout: true).trim()
                        def fullImageName = "${IMAGE_NAME}-${service}:latest"

                        // Tag the image
                        bat "docker tag ${imageId} ${fullImageName}"

                        // Push the image
                        bat "docker push ${fullImageName}"
                    }
                }
            }
        }
    }

    post {
        cleanup {
            script {
                // Clean up the workspace
                deleteDir()
            }
        }
    }
}
