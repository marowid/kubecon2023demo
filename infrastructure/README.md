# Create infrastructure in Azure

## Edge site

Clone repository: https://github.com/marowid/kubecon2023demo.git

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
