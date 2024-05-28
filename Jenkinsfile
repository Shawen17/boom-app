pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('github-token') // ID of the secret text in Jenkins
        GITHUB_USERNAME = 'shawen17'
        IMAGE_NAME = "ghcr.io/${GITHUB_USERNAME}"
        DOCKER_BUILDKIT = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images in Parallel') {
            parallel {
                stage('Build lendsqr_backend Image') {
                    steps {
                        script {
                            bat 'docker-compose build lendsqr_backend'
                        }
                    }
                }
                stage('Build lendsqr Image') {
                    steps {
                        script {
                            bat 'docker-compose build lendsqr'
                        }
                    }
                }
                // Add more stages for additional services as needed
            }
        }

        stage('Login to GHCR') {
            steps {
                script {
                    bat "echo ${DOCKERHUB_CREDENTIALS} | docker login ghcr.io -u ${GITHUB_USERNAME} --password-stdin"
                }
            }
        }

        stage('Tag and Push Images in Parallel') {
            steps {
                script {
                    // Get the list of services from docker-compose file
                    def services = bat(script: "docker-compose config --services", returnStdout: true).trim().split('\r?\n')

                    def parallelStages = [:]

                    services.each { service ->
                        parallelStages["Tag and Push ${service}"] = {
                            def imageId = bat(script: "docker-compose images -q ${service}", returnStdout: true).trim()
                            def fullImageName = "${IMAGE_NAME}-${service}:latest"

                            // Tag the image
                            bat "docker tag ${imageId} ${fullImageName}"

                            // Push the image
                            bat "docker push ${fullImageName}"
                        }
                    }

                    parallel parallelStages
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
