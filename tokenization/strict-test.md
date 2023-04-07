# Strict test

## Classic microk8s

Deploy microk8s in classic mode

```shell
sudo snap install microk8s --classic
```

Create new folder and write a file there

```shell
sudo mkdir -p /data
echo "hi from host" | sudo tee /data/hi.txt
```

Deploy a Pod with access to folder on the host

```shell
cat <<EOF | kubectl apply  -f -
apiVersion: v1
kind: Pod
metadata:
  name: ubu
spec:
  containers:
  - name: my-container
    image: ubuntu
    command: ["sleep", "3600"]
    volumeMounts:
    - name: data-volume
      mountPath: /data
  volumes:
  - name: data-volume
    hostPath:
      path: /data
EOF
pod/ubu configured
```

Check Pod status

```shell
kubectl get po
NAME   READY   STATUS    RESTARTS   AGE
ubu    1/1     Running   0          10m
```

Access file in the Pod

```shell
kubectl exec -it ubu -- bash
root@ubu:/# cat /data/hi.txt 
hi from host
```

## Strict microk8s

Deploy microk8s in strict mode

```shell
sudo snap install microk8s --channel 1.26-strict/stable
```

Create new folder and write a file there

```shell
sudo mkdir -p /data
echo "hi from host" | sudo tee /data/hi.txt
```

Deploy a Pod with access to folder on the host

```shell
cat <<EOF | kubectl apply  -f -
apiVersion: v1
kind: Pod
metadata:
  name: ubu
spec:
  containers:
  - name: my-container
    image: ubuntu
    command: ["sleep", "3600"]
    volumeMounts:
    - name: data-volume
      mountPath: /data
  volumes:
  - name: data-volume
    hostPath:
      path: /data
EOF
pod/ubu configured
```

Check Pod status

```shell
kubectl get po
NAME   READY   STATUS                 RESTARTS   AGE
ubu    0/1     CreateContainerError   0          11m
```

Describe Pod

```shell
kubectl describe po ubu
...
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  28s                default-scheduler  Successfully assigned default/ubu to microk8s-strict
  Normal   Pulled     25s                kubelet            Successfully pulled image "ubuntu" in 3.110907336s (3.110918648s including waiting)
  Warning  Failed     25s                kubelet            Error: failed to generate container "1bda12fbfcb4d2c319c423251f9d25fde0b18fdc91c3c66697e6f8098a963e00" spec: failed to generate spec: failed to mkdir "/data": mkdir /data: read-only file system
  Normal   Pulled     24s                kubelet            Successfully pulled image "ubuntu" in 763.702789ms (763.710383ms including waiting)
  Warning  Failed     24s                kubelet            Error: failed to generate container "d4dbe7802408ed1586a3384e3b524d4414b951b99245fe59b6b22f7d09f19f5d" spec: failed to generate spec: failed to mkdir "/data": mkdir /data: read-only file system
  Normal   Pulling    11s (x3 over 28s)  kubelet            Pulling image "ubuntu"
  Normal   Pulled     10s                kubelet            Successfully pulled image "ubuntu" in 685.997477ms (686.002165ms including waiting)
  Warning  Failed     10s                kubelet            Error: failed to generate container "83ce0ee08034a1be46fd45663b2ff9132269c3bf4612bbf941d9161e7e3530cd" spec: failed to generate spec: failed to mkdir "/data": mkdir /data: read-only file system
```
