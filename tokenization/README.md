# Tokenization application

## Prepare data

Run data-modification notebook.

## Prepare environment

```shell
sudo snap install microk8s --channel 1.25/stable --classic
microk8s enable dns hostpath-storage dns
juju bootstrap microk8s micro
juju deploy ./bundle.yaml
```

## Create S3 buckets

Create S3 buckets in Minio:
- tokens
- data

## Build application
```shell
docker build . -t bponieckiklotz/tokenization-app:dev
docker push bponieckiklotz/tokenization-app:dev
```

## Deploy in K8s cluster: 
TODO change it to deployment with service exposing it

```shell
kubectl apply -f - << END
apiVersion: v1
kind: Pod
metadata:
  name: tokenization-api
spec:
  containers:
  - name: api
    image: bponieckiklotz/tokenization-app:dev@sha256:58b3579ece9cc6b4ee4a1f00d0f2abd3e20e9e6e621dc17e8fa4769eaa1f6592
    env:
    - name: TOKENIZER_STORAGE_URL
      value: http://minio.kubeflow.svc.cluster.local:9000/
END
```

## Upload new data using JSON
Change the URL.
```http request
POST http://10.1.100.45/files/breast_cancer
Content-Type: application/json

< ./input_breast_cancer.json
```
