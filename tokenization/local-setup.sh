#!/bin/bash

sudo snap install microk8s --channel 1.24/stable --classic
microk8s enable dns hostpath-storage

#wait for storage to be available
microk8s.kubectl get po -A

juju bootstrap microk8s micro

juju add-model kubeflow
juju deploy ./bundle.yaml

microk8s.kubectl get svc minio -n kubeflow
