# MovieRecommender v5

This is the fifth version of the MovieRecommender project. 
Versions 3 and 4 have set up orchestration and primitive observability using 
primarily Kubernetes and Prometheus, cAdvisor and Grafana for monitoring. Version 5 adds
instrumentation to our two services to monitor their latency and throughput.
Between v4 and v5, the code of the recommender and ratings service has changed, as have
the Prometheus k8s files.

NOTE: There is also a small change in the Dockerfiles of the services to
fix a bug with installing requirements. If you have already built the images for v4, 
you will need to rebuild them for v5.

Here are the steps to set up and run the MovieRecommender v5:

### Build and Push Docker Images

1. Make sure you have a Docker Hub account and are logged in to Docker CLI:

   ```bash
   docker login
   ```

2. Build and push the Docker images for the recommender and ratings services:

   ```bash
   docker build -t <your-dockerhub-username>/ratings:instrumented-v1 -f ratings_service/Dockerfile .
   docker push <your-dockerhub-username>/ratings:instrumented-v1
   ```
   
   ```bash
   docker build -t <your-dockerhub-username>/recommender:instrumented-v1 -f recommender_service/Dockerfile .
   docker push <your-dockerhub-username>/recommender:instrumented-v1
   ```
   
3. Deploy the Kubernetes cluster.

   ```bash
   kubectl apply -f k8s/redis
   kubectl apply -f k8s/ratings
   kubectl apply -f k8s/recommender
   kubectl apply -f k8s/cAdvisor
   kubectl apply -f k8s/prometheus
   kubectl apply -f k8s/grafana
   ```
   
4. (Optional) If your cluster was already running and you want to update a service
run the following command after the apply command for the service you want to update:

   ```bash
   kubectl rollout restart deployment <deployment-name>
   ```