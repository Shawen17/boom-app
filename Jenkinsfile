def LendsqrBackendImage
def LendsqrImage
import groovy.json.*


pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('github-token') 
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
        AWS_REGION = "eu-north-1"
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
                           bat 'docker compose -f docker-compose.build.yml build lendsqr_backend'
                        }
                    }
                }
                stage('Build lendsqr Image') {
                    steps {
                        script {
                           bat 'docker compose -f docker-compose.build.yml build lendsqr'
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
        stage('Test Backend Image') {
             environment{
                LENDSQR_BACKEND_IMAGE = "${LendsqrBackendImage}" 
                LENDSQR_IMAGE = "${LendsqrImage}"
            }
            steps {
                script{
                    
                    withEnv([
                        "LENDSQR_BACKEND_IMAGE=$LENDSQR_BACKEND_IMAGE",
                    ])
                    
                    {
                        bat '''
                        docker run -p 6379:6379 -d --name redis-test redis
                        echo Testing...
                        docker run --rm -e REDIS=localhost  -e DB_USER=%DB_USER% -e PASSWORD=%PASSWORD% -e CLUSTERNAME=%CLUSTERNAME% --network host %LENDSQR_BACKEND_IMAGE% pytest
                        '''
                    }
                }
            }
        }
        // stage('Deploy Images to EKS Cluster'){
        //     environment{
        //         LENDSQR_BACKEND_IMAGE = "${LendsqrBackendImage}" 
        //         LENDSQR_IMAGE = "${LendsqrImage}"
                
        //     }
        //     steps{
        //         script {
        //             withEnv([
        //                 "DB_USER=${DB_USER}",
        //                 "PASSWORD=${PASSWORD}",
        //                 "CLUSTERNAME=${CLUSTERNAME}",
        //                 "REACT_APP_MEDIA_URL=${REACT_APP_MEDIA_URL}",
        //                 "LENDSQR_BACKEND_IMAGE=${LENDSQR_BACKEND_IMAGE}",
        //                 "LENDSQR_IMAGE=${LENDSQR_IMAGE}",
                        
        //             ]) {
        //                  bat '''
        //                 echo %DOCKERHUB_CREDENTIALS% | docker login ghcr.io -u %GITHUB_USERNAME% --password-stdin
                        
        //                 kubectl apply -f service.yaml
        //                 '''
        //                 def deploymentYaml = readFile('deployment.yaml')
        //                 def modifiedYaml = deploymentYaml
        //                     .replace('${LENDSQR_IMAGE}', "${LENDSQR_IMAGE}")
        //                     .replace('${LENDSQR_BACKEND_IMAGE}', "${LENDSQR_BACKEND_IMAGE}")
        //                     .replace('${DB_USER}', "${DB_USER}")
        //                     .replace('${PASSWORD}', "${PASSWORD}")
        //                     .replace('${CLUSTERNAME}', "${CLUSTERNAME}")
        //                     .replace('${REACT_APP_MEDIA_URL}', "${REACT_APP_MEDIA_URL}")
                            
        //                 writeFile file: 'modified-deployment.yaml', text: modifiedYaml
        //                 bat '''
        //                 kubectl apply -f modified-deployment.yaml
        //                 kubectl get ingress || kubectl apply -f ingress.yaml
        //                 '''
        //              }
        //         }
        //     }
        // }
        
        stage('Check and Stop Containers') {
            steps {
                bat '''
                    powershell -Command "docker container ls -q | ForEach-Object { docker stop $_ }"
                '''
            }
        }
        stage('Remove All Containers') {
            steps {
                bat '''
                    powershell -Command "docker rm $(docker ps -q -a) -f"
                '''
            }
        }
        stage('Remove All Images') {
            steps {
                bat '''
                    powershell -Command " docker image rm -f $(docker image ls -q)"
                '''
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
                        // "DB_USER=$DB_USER",
                        // "PASSWORD=$PASSWORD",
                        // "CLUSTERNAME=$CLUSTERNAME",
                        // "REACT_APP_LENDSQR_API_URL=$REACT_APP_LENDSQR_API_URL",
                        // "REACT_APP_MEDIA_URL=$REACT_APP_MEDIA_URL",
                        "LENDSQR_BACKEND_IMAGE=$LENDSQR_BACKEND_IMAGE",
                        "LENDSQR_IMAGE=$LENDSQR_IMAGE",
                        "TAG=$TAG"
                    ]) {
                        bat '''
                        echo %DOCKERHUB_CREDENTIALS% | docker login ghcr.io -u %GITHUB_USERNAME% --password-stdin
                        docker compose -f docker-compose.run.yml up -d
                        '''
                    }
                }
            }
        }
    }

    post {
        // always {
        //     script {
        //         // Get the EXTERNAL-IP of the service and print it
        //         def externalIp = bat (
        //             script: 'kubectl get service boom-app-frontend-service -o jsonpath="{.status.loadBalancer.ingress[0].ip}"',
        //             returnStdout: true
        //         ).trim()
        //         echo "External IP: ${externalIp}"
        //     }
        // }
        cleanup {
            script {
              deleteDir()
            }
        }
    }
}
