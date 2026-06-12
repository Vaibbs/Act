# [Kubernetes Auto-Scaling Demo](https://github.com/Vaibbs/Act/blob/main/ScreenRec_260612_48578.mp4)

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── dockerfile
├── config.txt          # ConfigMap
├── chat-dep.txt        # Deployment
├── chat.txt            # Service
└── pod.yaml
```

---

## Build Docker Image

```bash
docker build -t mychatapp:v1 -f dockerfile .
```

### Test Locally (Optional)

```bash
docker run -d --name mychatapp-test -p 5000:5000 mychatapp:v1

curl http://localhost:5000

docker stop mychatapp-test
docker rm mychatapp-test
```

---

## Push Image to Docker Hub

```bash
docker tag mychatapp:v1 <dockerhub-username>/mychatapp:v1

docker login

docker push <dockerhub-username>/mychatapp:v1
```

Update the image reference in `chat-dep.txt`:

```yaml
image: <dockerhub-username>/mychatapp:v1
```

---

## Deploy to Kubernetes

### Create ConfigMap

```bash
kubectl apply -f config.txt
```

### Create Deployment

```bash
kubectl apply -f chat-dep.txt
```

### Create Service

```bash
kubectl apply -f chat.txt
```

---

## Verify Resources

```bash
kubectl get deployments

kubectl get pods

kubectl get svc

kubectl get configmaps
```

Watch pod creation:

```bash
kubectl get pods -w
```

View logs:

```bash
kubectl logs -f deployment/chat-app
```

---

## Configure Horizontal Pod Autoscaler

```bash
kubectl autoscale deployment chat-app \
  --cpu-percent=50 \
  --min=1 \
  --max=10
```

Verify:

```bash
kubectl get hpa
```

Watch scaling events:

```bash
kubectl get hpa -w
```

---

## Access Application

```bash
kubectl get svc
```

If using Minikube:

```bash
minikube service chat-service --url
```

---

## Install hey

```bash
go install github.com/rakyll/hey@latest
```

Verify installation:

```bash
hey -h
```

---

## Load Testing

Basic test:

```bash
hey -n 1000 -c 50 http://<SERVICE-IP>:<PORT>/
```

Heavy test to trigger autoscaling:

```bash
hey -n 10000 -c 200 http://<SERVICE-IP>:<PORT>/
```

Sustained load for 5 minutes:

```bash
hey -z 5m -c 200 http://<SERVICE-IP>:<PORT>/
```

---

## Monitor Scaling

```bash
kubectl get hpa -w
```

In another terminal:

```bash
kubectl get pods -w
```

You should see additional replicas being created as CPU utilization increases.

---

## Cleanup

```bash
kubectl delete -f chat.txt

kubectl delete -f chat-dep.txt

kubectl delete -f config.txt

kubectl delete hpa chat-app
```
