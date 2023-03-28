# Create infrastructure in Azure

## Edge site

Clone the repository

```shell
git clone https://github.com/marowid/kubecon2023demo.git
```

Create a VM with size Standard D4s v5 (4 vcpus, 16 GiB memory). Add SSH key and allow access via
port 22.

Create the Azure Storage Account in the same Region

Go to `infrastructure` folder. Fill in the access-key and secret-keys

```shell
echo -n "<storage-account-name>" > access-key.secret
echo -n "<key1>" > secret-key.secret
```

Prepare cluster

```shell
sudo snap install microk8s --channel 1.24/stable --classic
sudo usermod -a -G microk8s $USER
mkdir -p ~/.kube
sudo chown -f -R $USER ~/.kube

#relogin
newgrp microk8s

microk8s enable hostpath-storage dns ingress
```

Install juju and deploy the bundle.

```shell
sudo snap install juju --classic
juju bootstrap microk8s micro
juju add-model kubeflow
```

Deploy bundle

```shell
juju deploy ./edge-bundle.yaml
```

Post deployment steps

1. Add secret to access minio from seldon core

## Data center site

Clone the repository

```shell
git clone https://github.com/marowid/kubecon2023demo.git
```

Create a VM with size Standard D16as v5 (16 vcpus, 64 GiB memory). Add SSH key and allow access via
port 22.

Create the Azure Storage Account in the same Region

Go to `infrastructure` folder. Fill in the access-key and secret-keys

```shell
echo -n "<storage-account-name>" > access-key.secret
echo -n "<key1>" > secret-key.secret
```

Prepare cluster

```shell
sudo snap install microk8s --channel 1.24/stable --classic
sudo usermod -a -G microk8s $USER
mkdir -p ~/.kube
sudo chown -f -R $USER ~/.kube

#relogin
newgrp microk8s

microk8s enable hostpath-storage dns ingress
```

Install juju and deploy the bundle.

```shell
sudo snap install juju --classic
juju bootstrap microk8s micro
juju add-model kubeflow
```


