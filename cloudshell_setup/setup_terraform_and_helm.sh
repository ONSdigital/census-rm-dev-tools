git clone https://github.com/ONSdigital/census-rm-terraform.git ~/census-rm-terraform

git clone https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
tfenv --version

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get
chmod 700 get_helm.sh
./get_helm.sh
helm init --client-only
helm plugin install https://github.com/rimusz/helm-tiller

helm version --client

exec bash
