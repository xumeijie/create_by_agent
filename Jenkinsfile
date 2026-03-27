pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], 
               description: 'Test environment')
        choice(name: 'TEST_TYPE', choices: ['unit', 'integration', 'all'], 
               description: 'Type of tests to run')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Checked out from ${GIT_BRANCH}"'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python -m venv .venv
                    source .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    source .venv/bin/activate
                    
                    if [ "${TEST_TYPE}" = "unit" ]; then
                        pytest tests/test_unit.py -v --junit-xml=reports/junit.xml
                    elif [ "${TEST_TYPE}" = "integration" ]; then
                        pytest tests/test_integration.py -v --junit-xml=reports/junit.xml
                    else
                        pytest tests/ -v --junit-xml=reports/junit.xml
                    fi
                '''
            }
        }
        
        stage('Generate Reports') {
            steps {
                sh '''
                    source .venv/bin/activate
                    python reports/report_generator.py
                '''
            }
        }
        
        stage('Publish Results') {
            steps {
                junit 'reports/junit.xml'
                publishHTML([
                    reportDir: 'reports/html',
                    reportFiles: '*.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            cleanWs()
        }
        success {
            echo "Tests passed successfully!"
        }
        failure {
            echo "Tests failed!"
            mail to: 'team@example.com',
                 subject: "Test Failure in ${JOB_NAME}",
                 body: "Check the test report"
        }
    }
}
