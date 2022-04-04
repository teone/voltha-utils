lwc_path="/home/teone/Sites/voltha/Radisys_LWC_for_ONF_v1"
voltha_helm_chart_path="/home/teone/Sites/voltha/voltha-helm-charts"
lwc_helm_chart_path="/home/teone/Sites/voltha/Radisys_LWC_for_ONF_v1/Radisys_LWC_helm_charts"
value_file="${voltha_helm_chart_path}/lwc-values.yaml"
workflow="dt"
kind_cluster_name="voltha-dev" # default is "kind"
onu_count=16
pon_count=16

helm del -n infra voltha-infra
helm del -n voltha1 bbsim0 voltha1

cd $lwc_path

# load images in docker
sudo docker load -i Radisys_LWC_for_ONF_v2.tgz
sudo docker load -i redis_6.0.10-debian-10-r19.tgz

# load images in the kind cluster
kind load --name $kind_cluster_name docker-image lwc:latest
kind load --name $kind_cluster_name docker-image docker-registry.com:5000/bitnami/redis:6.0.10-debian-10-r19

cd $voltha_helm_chart_path
helm dep update $lwc_helm_chart_path/voltha-infra
helm upgrade --install --create-namespace -n infra voltha-infra $lwc_helm_chart_path/voltha-infra -f examples/${workflow}-values.yaml \
  -f $value_file --wait

helm dep update $voltha_helm_chart_path/voltha-stack
helm upgrade --install --create-namespace -n voltha1 voltha1 $voltha_helm_chart_path/voltha-stack -f $value_file --wait

helm upgrade --install -n voltha1 bbsim0 onf/bbsim --set olt_id=10 -f examples/${workflow}-values.yaml --set pon=$pon_count,onu=$onu_count --version 4.6.0 --set oltRebootDelay=5 --wait
