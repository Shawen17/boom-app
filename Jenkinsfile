pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('github-token') // ID of the secret text in Jenkins
        GITHUB_USERNAME = 'shawen17'
        IMAGE_NAME = "ghcr.io/${GITHUB_USERNAME}"
        DOCKER_BUILDKIT = '1'
        DB_USER=credentials('DB_USER')
        PASSWORD=credentials('PASSWORD')
        CLUSTERNAME=credentials('CLUSTERNAME')
        SECRET_KEY=credentials('SECRET_KEY')
        HOST=credentials('HOST')
        AUTH_PASSWORD=credentials('AUTH_PASSWORD')
        AWS_SECRET_ACCESS_KEY=credentials('AWS_SECRET_ACCESS_KEY')
        AWS_ACCESS_KEY_ID=credentials('AWS_ACCESS_KEY_ID')
        REACT_APP_LENDSQR_API_URL=credentials('REACT_APP_LENDSQR_API_URL')
        REACT_APP_MEDIA_URL=credentials('REACT_APP_MEDIA_URL')
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
                            withEnv([
                                "SECRET_KEY=${SECRET_KEY}",
                                "HOST=${HOST}",
                                "AUTH_PASSWORD=${AUTH_PASSWORD}",
                                "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}",
                                "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}",
                                ]){
                                bat 'docker-compose -f docker-compose.build.yml build lendsqr_backend'
                            }
                        }
                    }
                }
                stage('Build lendsqr Image') {
                    steps {
                        script {
                           bat 'docker-compose -f docker-compose.build.yml build lendsqr'
                        }
                    }
                }
                
            }
        }

        stage('Login to GHCR') {
            steps {
                script {
                    
                    bat 'echo %DOCKERHUB_CREDENTIALS% | docker login ghcr.io -u %GITHUB_USERNAME% --password-stdin'
                }
            }
        }

        stage('Tag and Push Images in Parallel') {
            steps {
                script {
                    // Get the list of services from docker-compose file
                    // def services = bat(script: "docker-compose config --services", returnStdout: true).trim().split('\r?\n')
                    def services = ['lendsqr_backend', 'lendsqr']

                    def parallelStages = [:]

                    services.each { service ->
                        parallelStages["Tag and Push ${service}"] = {
                            def imageId = bat(script: "docker-compose -f docker-compose.build.yml images -q ${service}", returnStdout: true).trim()
                            bat "echo imageId is %imageId%"
                            def fullImageName = "${IMAGE_NAME}-${service}:latest"
                            bat "echo full imagename is  %fullImageName%"
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
        // stage('Run Containers') {
        //     steps {
        //         script {
        //             withEnv([
        //                 "DB_USER=${DB_USER}",
        //                 "PASSWORD=${PASSWORD}",
        //                 "CLUSTERNAME=${CLUSTERNAME}",
        //                 "SECRET_KEY=${SECRET_KEY}",
        //                 "HOST=${HOST}",
        //                 "AUTH_PASSWORD=${AUTH_PASSWORD}",
        //                 "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}",
        //                 "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}",
        //                 "REACT_APP_LENDSQR_API_URL=${REACT_APP_LENDSQR_API_URL}",
        //                 "REACT_APP_MEDIA_URL=${REACT_APP_MEDIA_URL}"
        //             ]) {
        //                 bat 'docker-compose -f docker-compose.run.yml up -d'
        //             }
        //         }
        //     }
        // }
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
