pipeline {
    agent any
    environment {
        ECR_REPO = '183295407444.dkr.ecr.us-east-1.amazonaws.com/meditrack' //ECR repository
        IMAGE_TAG = "appointment-service" // Using Jenkins build ID as the image tag
        KUBECONFIG_CREDENTIALS = 'kubeconfig' // Kubernetes kubeconfig credential ID in Jenkins
    }
    stages {
        stage('Checkout Code') {
            steps {
                // Clone the repository containing your application code
                git branch: 'main', url: 'https://github.com/nithinkolamunna/meditrack/tree/main/appointment'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh """
                    # Log in to Amazon ECR
                    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_REPO}
                    
                    # Build the Docker image
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                    
                    # Push the Docker image to ECR
                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    """
                }
            }
        }
        stage('Deploy Green') {
            steps {
                script {
                    sh """
                    # Update the green deployment with the new image
                    kubectl set image deployment/green-app green-app=${ECR_REPO}:${IMAGE_TAG} --kubeconfig=${KUBECONFIG_CREDENTIALS}
                    
                    # Wait for the green deployment to roll out successfully
                    kubectl rollout status deployment/green-app --kubeconfig=${KUBECONFIG_CREDENTIALS}
                    """
                }
            }
        }
        stage('Validate Green') {
            steps {
                script {
                    sh """
                    # Check the status of green pods to ensure they are running successfully
                    kubectl get pods -l app=green-app -o wide --kubeconfig=${KUBECONFIG_CREDENTIALS}
                    """
                }
            }
        }
        stage('Switch Traffic') {
            steps {
                script {
                    sh """
                    # Update the service to point to the green deployment
                    kubectl patch service meditrackApp-service -p '{\"spec\":{\"selector\":{\"app\":\"green-app\"}}}' --kubeconfig=${KUBECONFIG_CREDENTIALS}
                    """
                }
            }
        }
        stage('Remove Blue') {
            steps {
                script {
                    sh """
                    # Remove the blue deployment after successful traffic switch
                    kubectl delete deployment blue-app --kubeconfig=${KUBECONFIG_CREDENTIALS}
                    """
                }
            }
        }
    }
}
