pipeline {
    agent{
        label "gcp-agent-1"
        // can run gcloud command
    }
    environment {
        MONGO_HOST = "mongodb://localhost:27017"
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
                            sh  '''
                            MONGO_DATA_COUNT=$(python3 mongo_client.py -c ${DATA} count-data --contain-header)
                            CSV_DATA_COUNT=$(cat output/${DATA}/${DATA}.csv|wc -l)
                            echo "Mongo data count: ${MONGO_DATA_COUNT}"
                            echo "CSV data count: ${CSV_DATA_COUNT}"
                            if [ $CSV_DATA_COUNT != $CSV_DATA_COUNT ]; then exit 1; fi
                            '''
                        }
                    }
                    stage("Check data quality"){
                        steps{
                            sh """
                            docker run -v ${WORKSPACE}/output/${DATA}/:/usr/src/github/ piperider run
                            """
                            sh '''
                            sudo rm -rf ${WORKSPACE}/output/${DATA}/.piperider/outputs/latest
                            sudo ln -s ${WORKSPACE}/output/${DATA}/.piperider/outputs/$(ls ${WORKSPACE}/output/${DATA}/.piperider/outputs | grep ithome|tail -n1) ${WORKSPACE}/output/${DATA}/.piperider/outputs/latest
                            '''
                            sh "python3 get_piperider_result.py --data-source-name ${DATA} "
                        }
                    }
                    stage("Push to GCS"){
                        steps{
                            sh """
                            gcloud alpha storage cp output/${DATA}/${DATA}.csv gs://crawler_result/ithome/ironman2022
                            """
                        }
                    }                                     
                }
            }
        }              
    }
    post{
        always{
            archiveArtifacts artifacts: 'output/**', followSymlinks: false
        }
    }
}