def LendsqrBackendImage
def LendsqrImage

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
                            script {
                                // Create a temporary file to store the image ID
                                def imageIdFile = "imageId_${service}.txt"
                                
                                // Capture the image ID to the file
                                bat "docker images -q boom-app-job-${service} > ${imageIdFile}"

                                // Read the image ID from the file
                                def imageId = readFile(imageIdFile).trim()
                                
                                if (imageId) {
                                    def fullImageName = "${IMAGE_NAME}/boom-app-job-${service}:${env.BUILD_ID}"
                                    
                                    // Tag the image
                                    bat "docker tag ${imageId} ${fullImageName}"

                                    // Push the image
                                    bat "docker push ${fullImageName}"

                                    if(service=='lendsqr_backend'){
                                       LendsqrBackendImage = fullImageName
                                    }else{
                                       LendsqrImage = fullImageName
                                    }

                                } else {
                                    error "Failed to retrieve image ID for ${service}"
                                }
                                // Clean up the temporary file
                                bat "del ${imageIdFile}"
                            }
                        }
                    }
                    parallel parallelStages
                }
            }
        }
         stage('Cleanup') {
            steps {
                script {
                    // Remove unused Docker images
                    bat '''
                        docker image prune -f
                        unused_images=$(docker images -f "dangling=false" -q)
                        for image in ${unused_images}; do
                            if [ -z "$(docker ps -q --filter ancestor=${image})" ]; then
                                docker rmi ${image}
                            fi
                        done
                    '''
                }
            }
        }

        stage('Run Containers') {
            environment{
                LENDSQR_BACKEND_IMAGE = "${LendsqrBackendImage}" 
                LENDSQR_IMAGE = "${LendsqrImage}"
                TAG = "${env.BUILD_ID}"
            }
            steps {
                
                script {
                    withEnv([
                        "DB_USER=${DB_USER}",
                        "PASSWORD=${PASSWORD}",
                        "CLUSTERNAME=${CLUSTERNAME}",
                        "REACT_APP_LENDSQR_API_URL=${REACT_APP_LENDSQR_API_URL}",
                        "REACT_APP_MEDIA_URL=${REACT_APP_MEDIA_URL}",
                        "LENDSQR_BACKEND_IMAGE=${LENDSQR_BACKEND_IMAGE}",
                        "LENDSQR_IMAGE=${LENDSQR_IMAGE}",
                        "TAG=${TAG}"
                    ]) {
                        bat '''
                        echo %DOCKERHUB_CREDENTIALS% | docker login ghcr.io -u %GITHUB_USERNAME% --password-stdin
                        docker-compose -f docker-compose.run.yml up -d
                        '''
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
