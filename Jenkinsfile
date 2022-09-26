pipeline {
    agent{
        label "gcp-agent-1"
        // can run gcloud command
    }
    environment {
        MONGO_HOST = "mongo://localhost:27017"
        MONGO_DB = "ithome_ironman"
    } 
    stages {
        stage('Data pipeline(stage 1)') {
            matrix {
                axes {
                    axis {
                        name 'DATA'
                        values 'user_info', 'content_info'
                    }
                }
                stages {
                    stage("Pull mongo data"){
                        steps{
                            sh """
                                python3 mongo_client.py -c ${DATA} \
                                    to-csv --csv-file-path output/${DATA}/${DATA}.csv
                            """
                        }
                    }
                    stage("Check mongo data"){
                        steps{
                            script{
                                MONGO_DATA_COUNT = sh (
                                    script: "python3 mongo_client.py -c ${DATA} count-data --contain-header",
                                    returnStdout: true
                                ).trim().toInteger()
                                CSV_DATA_COUNT = sh (
                                    script: "cat output/${DATA}/${DATA}.csv|wc -l",
                                    returnStdout: true
                                ).trim().toInteger()
                                if (MONGO_DATA_COUNT != CSV_DATA_COUNT){
                                    echo "Mongo data:  ${MONGO_DATA_COUNT}"
                                    echo "Csv data:  ${CSV_DATA_COUNT}"
                                    sh "false"
                                }
                            }
                        }
                    }
                    stage("Check data quality"){
                        steps{
                            sh """
                            docker run -v ${WORKSPACE}output/${DATA}/:/usr/src/github/ piperider run
                            """
                            sh "python3 get_piperider_result.py ----data-source-name ${DATA}"
                        }
                    }                     
                }
            }
        }
        stage('Data pipeline(stage 2)') {
            matrix {
                axes {
                    axis {
                        name 'MONGO_COLLECTION'
                        values 'user', 'devops_groups'
                    }
                    axis {
                        name 'GCS_FILE_NAME'
                        values 'user_info', 'ironman_content'
                    }                    
                }
                excludes {
                    exclude {
                        axis {
                            name 'MONGO_COLLECTION'
                            values 'user'
                        }
                        axis {
                            name 'GCS_FILE_NAME'
                            values 'ironman_content'
                        }
                    }
                    exclude {
                        axis {
                            name 'MONGO_COLLECTION'
                            values 'devops_groups'
                        }
                        axis {
                            name 'GCS_FILE_NAME'
                            values 'user_info'
                        }
                    }                    
                }
                stages {
                    stage("Push to GCS"){
                        steps{
                            echo "push to gcs ${MONGO_COLLECTION} ${GCS_FILE_NAME}"
                        }
                    }
                    stage("Check upload to GCS data"){
                        steps{
                            echo "cat to gcs|wc -l ${MONGO_COLLECTION} ${GCS_FILE_NAME}"
                        }
                    }
                }
            }
        }
        stage("Move to prodcution folder on GCS"){
            steps{
                echo "mv to gcs"
            }
        }                 
    }
    post{
        success{
            cleanWs()
        }
    }
}