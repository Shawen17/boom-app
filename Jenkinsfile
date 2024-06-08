def LendsqrBackendImage
def LendsqrImage

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
        ECS_CLUSTER = "boom-complete-app"
        ECS_TASK_DEFINITION_FAMILY = "boom-app-family"
        
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Perform Test with Pytest') {
            steps {
                bat 'cd lendsqr_backend && pytest'
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
                                bat 'docker compose -f docker-compose.build.yml build lendsqr_backend'
                            }
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
        stage('Register/Update ECS Task Definition') {
            steps {
                script {
                    def taskDefinitionTemplate = readFile 'ecs-task-definition-template.json'
                    def jsonSlurper = new JsonSlurper()
                    def taskDefinitionJson = jsonSlurper.parseText(taskDefinitionTemplate)

                    taskDefinitionJson.containerDefinitions[0].image = LendsqrBackendImage
                    taskDefinitionJson.containerDefinitions[1].image = LendsqrImage

                    // Update environment variables
                    taskDefinitionJson.containerDefinitions[0].environment.find { it.name == 'DB_USER' }.value = "${DB_USER}"
                    taskDefinitionJson.containerDefinitions[0].environment.find { it.name == 'PASSWORD' }.value = "${PASSWORD}"
                    taskDefinitionJson.containerDefinitions[0].environment.find { it.name == 'CLUSTERNAME' }.value = "${CLUSTERNAME}"
                    taskDefinitionJson.containerDefinitions[1].environment.find { it.name == 'REACT_APP_LENDSQR_API_URL' }.value = "${REACT_APP_LENDSQR_API_URL}"
                    taskDefinitionJson.containerDefinitions[1].environment.find { it.name == 'REACT_APP_MEDIA_URL' }.value = "${REACT_APP_MEDIA_URL}"

                    def updatedTaskDefinition = writeJSON returnText: true, json: taskDefinitionJson

                    writeFile file: 'ecs-task-definition.json', text: updatedTaskDefinition

                    withCredentials([
                        string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                        string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                    ]) {
                         bat '''
                        set AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%
                        set AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%
                        aws ecs register-task-definition ^
                            --family %ECS_TASK_DEFINITION_FAMILY% ^
                            --cli-input-json file://ecs-task-definition.json ^
                            --region %AWS_REGION%
                        '''
                    }
                }
            }
        }
        stage('Deploy to ECS') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
                        string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
                    ]) {
                        bat '''
                        aws ecs update-service ^
                            --cluster ${ECS_CLUSTER} ^
                            --service your-ecs-service-name ^
                            --force-new-deployment ^
                            --region %AWS_REGION%
                        '''
                    }
                }
            }
        }
        
    //     stage('Check and Stop Containers') {
    //         steps {
    //             bat '''
    //                 powershell -Command "docker container ls -q | ForEach-Object { docker stop $_ }"
    //             '''
    //         }
    //     }
    //     stage('Remove All Containers') {
    //         steps {
    //             bat '''
    //                 powershell -Command "docker rm $(docker ps -q -a) -f"
    //             '''
    //         }
    //     }
    //     stage('Remove All Images') {
    //         steps {
    //             bat '''
    //                 powershell -Command " docker image rm -f $(docker image ls -q)"
    //             '''
    //         }
    //     }
        
    //     stage('Run Containers') {
    //         environment{
    //             LENDSQR_BACKEND_IMAGE = "${LendsqrBackendImage}" 
    //             LENDSQR_IMAGE = "${LendsqrImage}"
    //             TAG = "${env.BUILD_ID}"
    //         }
    //         steps {
                
    //             script {
    //                 withEnv([
    //                     "DB_USER=${DB_USER}",
    //                     "PASSWORD=${PASSWORD}",
    //                     "CLUSTERNAME=${CLUSTERNAME}",
    //                     "REACT_APP_LENDSQR_API_URL=${REACT_APP_LENDSQR_API_URL}",
    //                     "REACT_APP_MEDIA_URL=${REACT_APP_MEDIA_URL}",
    //                     "LENDSQR_BACKEND_IMAGE=${LENDSQR_BACKEND_IMAGE}",
    //                     "LENDSQR_IMAGE=${LENDSQR_IMAGE}",
    //                     "TAG=${TAG}"
    //                 ]) {
    //                     bat '''
    //                     echo %DOCKERHUB_CREDENTIALS% | docker login ghcr.io -u %GITHUB_USERNAME% --password-stdin
    //                     docker compose -f docker-compose.run.yml up -d
    //                     '''
    //                 }
    //             }
    //         }
    //     }
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
