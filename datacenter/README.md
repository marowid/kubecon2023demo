# Create infrastructure in Azure for KubeCon Datacenter

Select a region in Azure. For all consecutive Azure resources use the same region to avoid unnecessary costs.

## Create Azure storage

Create the Azure Storage Account in the same Region.

## Create VMs (datacenter main and confidential compute with GPU)

Deploy both VMs in the same VPC to ensure the connectivity between the cluster nodes

For **Datacenter** create a VM with size Standard D16as v5 (16 vCPU, 64 GiB memory). Select the Ubuntu 22.04 as the OS. Add SSH key and allow access via
port 22. Stop the VM after creation and increase the size of the disk to bigger than 80GB.

For **confidential computing** create a VM with size Standard NC6s v2 (6 vCPU, 112 GiB memory). This VM has a GPU. Select the Ubuntu 22.04 (Confidential) as the OS. Add SSH key and allow access via
port 22.

Edit the configuration of the VM NICs to allow the Microk8s to cluster. You need to allow "IP forwarding" in the configuration of the NIC which will be used to handle the microk8s internal traffic. In our case, we have only a single NIC so in the VM details go to the "Networking" tab, then select the Network interface, then go to the "IP configurations" and change the value of "IP forwarding" to the Enabled.

## Build Microk8s cluster

SSH into the Datacenter VM and clone the repository

```shell
git clone https://github.com/marowid/kubecon2023demo.git
cd kubecon2023demo/datacenter
```

Add the secret values for object storage using values from "Access keys" in the Storage accounts.

```shell
echo -n "<Storage account name>" > ./secrets/access-key.secret
echo -n "<key1.Key>" > ./secrets/secret-key.secret
```

Install Microk8s

```shell
sudo snap install microk8s --channel 1.24/stable --classic
sudo usermod -a -G microk8s $USER
mkdir -p ~/.kube
sudo chown -f -R $USER ~/.kube

newgrp microk8s

# workaround for one of the microk8s-kubeflow bugs
sudo sysctl fs.inotify.max_user_instances=1280
sudo sysctl fs.inotify.max_user_watches=655360
```

SSH into the Confidential computing VM and repeat the "Install Microk8s" step.

Install also the GPU driver if you selected the GPU-accelerated VM.

```shell
sudo apt install ubuntu-drivers-common -y
sudo ubuntu-drivers install --gpgpu
sudo apt install nvidia-utils-525-server -y

sudo reboot
```

In the terminal of the Datacenter VM start adding nodes to the cluster by

```shell
microk8s add-node
```

In the terminal of the Confidential Computing window paste the result of the command from Datacenter:

```shell
microk8s join 10.1.10.3:25000/xxxxxxxxxxxxxxxxxxx 
```

When you see both of the nodes available and in the "Ready" state label and add taints to the nodes. We want to use the GPU node only when needed.

```shell
microk8s.kubectl taint nodes kubecon-conf confidential=true:PreferNoSchedule
microk8s.kubectl label nodes kubecon-conf confidential=true
```

Enable plugins in for microk8s cluster (remove the "gpu" from command if not needed)

```shell
microk8s enable hostpath-storage dns ingress gpu
```

Check if GPU is working using the NGC container

```shell
$ microk8s.kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vector-add
spec:
  restartPolicy: OnFailure
  containers:
    - name: cuda-vector-add
      image: "k8s.gcr.io/cuda-vector-add:v0.1"
      resources:
        limits:
          nvidia.com/gpu: 1
EOF


$ microk8s.kubectl logs cuda-vector-add
[Vector addition of 50000 elements]
Copy input data from the host memory to the CUDA device
CUDA kernel launch with 196 blocks of 256 threads
Copy output data from the CUDA device to the host memory
Test PASSED
Done
```

## Deploy Kubeflow

Install juju and deploy the bundle.

```shell
sudo snap install juju --classic
juju bootstrap microk8s micro
juju add-model kubeflow
```

Deploy bundle

```shell
juju deploy ./dc-bundle.yaml --trust
```

Check istio-ingressgateway-workload NodePort

```shell
kubectl get svc istio-ingressgateway-workload -n kubeflow
```

```shell
PUBLIC_URL=http://20.224.249.29:30080/
juju config dex-auth public-url="$PUBLIC_URL"
juju config oidc-gatekeeper public-url="$PUBLIC_URL"

#you are exposing it to the public so its better to change the password
juju config dex-auth static-username=admin static-password=admin

juju run --unit istio-pilot/0 -- "export JUJU_DISPATCH_PATH=hooks/config-changed; ./dispatch"
```

## Post-deployment steps

Apply integrations for static user

```shell
USER_NAMESPACE=admin

cat <<EOF | kubectl apply -n $USER_NAMESPACE -f -
apiVersion: kubeflow.org/v1alpha1
kind: PodDefault
metadata:
  name: mlflow-server-minio
spec:
  desc: Allow access to MLFlow
  env:
  - name: MLFLOW_S3_ENDPOINT_URL
    value: http://minio.kubeflow:9000
  - name: MLFLOW_TRACKING_URI
    value: http://mlflow-server.kubeflow.svc.cluster.local:5000
  selector:
    matchLabels:
      mlflow-server-minio: "true"
EOF

cat <<EOF | kubectl apply -n $USER_NAMESPACE -f -
apiVersion: kubeflow.org/v1alpha1
kind: PodDefault
metadata:
 name: access-minio
spec:
 desc: Allow access to Minio
 selector:
   matchLabels:
     access-minio: "true"
 env:
   - name: AWS_ACCESS_KEY_ID
     valueFrom:
       secretKeyRef:
         name: mlpipeline-minio-artifact
         key: accesskey
         optional: false
   - name: AWS_SECRET_ACCESS_KEY
     valueFrom:
       secretKeyRef:
         name: mlpipeline-minio-artifact
         key: secretkey
         optional: false
   - name: MINIO_ENDPOINT_URL
     value: http://minio.kubeflow.svc.cluster.local:9000
EOF

kubectl get secret mlflow-server-seldon-init-container-s3-credentials -n kubeflow -o yaml \
 | sed "s/namespace: kubeflow/namespace: $USER_NAMESPACE/g" \
 | sed 's/name: mlflow-server-seldon-init-container-s3-credentials/name: seldon-init-container-secret/g' \
 | sed 's/aHR0cDovL21pbmlvOjkwMDA=/aHR0cDovL21pbmlvLmt1YmVmbG93OjkwMDA=/g' \
 | kubectl apply -n $USER_NAMESPACE -f -
```

Login using $PUBLIC_URL!
