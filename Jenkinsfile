// pipeline {
//   agent any
//   environment {
//     PROJECT = 'rshop-85731'
//     IMAGE = "gcr.io/$PROJECT/mlops-gke-app:$BUILD_NUMBER"
//     CLUSTER = 'your-gke-cluster'
//     ZONE = 'europe-west1-b'
//   }
//   stages {
//     stage('Checkout') { steps { git 'https://github.com/sanogosy/mlops-flask-app.git' } }
//     stage('Train')    { steps { sh 'python train.py' } }
//     stage('Build & Push') {
//       steps {
//         sh 'docker build -t $IMAGE .'
//         withCredentials([file(credentialsId: 'gcloud-key', variable: 'GCLOUD_KEY')]) {
//           sh '''
//             gcloud auth activate-service-account --key-file=$GCLOUD_KEY
//             gcloud auth configure-docker
//             docker push $IMAGE
//           '''
//         }
//       }
//     }
//     stage('Deploy to GKE') {
//       steps {
//         withCredentials([file(credentialsId: 'gcloud-key', variable: 'GCLOUD_KEY')]) {
//           sh '''
//             gcloud auth activate-service-account --key-file=$GCLOUD_KEY
//             gcloud container clusters get-credentials $CLUSTER --zone $ZONE --project $PROJECT
//             kubectl set image deployment/mlops-app flask=$IMAGE
//             kubectl rollout status deployment/mlops-app
//           '''
//         }
//       }
//     }
//   }
// }

pipeline {
  agent any

  environment {
    IMAGE_NAME = "sanogosy/mlops-flask-app"
    IMAGE_TAG = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/sanogosy/mlops-flask-app'
      }
    }

    stage('Train') {
      steps {
        sh 'python train.py'
      }
    }

    stage('Build & Push Docker') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker build -t $IMAGE_NAME:$IMAGE_TAG .
            docker push $IMAGE_NAME:$IMAGE_TAG
            docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest
            docker push $IMAGE_NAME:latest
          '''
        }
      }
    }

    stage('Deploy to GKE') {
      steps {
        withCredentials([file(credentialsId: 'gcloud-key', variable: 'GCLOUD_KEY')]) {
          sh '''
            gcloud auth activate-service-account --key-file=$GCLOUD_KEY
            gcloud container clusters get-credentials $CLUSTER --zone $ZONE --project $PROJECT
            kubectl set image deployment/mlops-app flask=$IMAGE
            kubectl rollout status deployment/mlops-app
          '''
        }
      }
    }

  }
}