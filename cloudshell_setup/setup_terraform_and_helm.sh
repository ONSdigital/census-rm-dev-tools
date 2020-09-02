# Clone our terraform repo
git clone https://github.com/ONSdigital/census-rm-terraform.git ~/census-rm-terraform

# Install Tfenv
git clone https://github.com/tfutils/tfenv.git ~/.tfenv
echo 'PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
tfenv --version

# Install helm 2 and helm-tiller plugin
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get
chmod 700 get_helm.sh
./get_helm.sh
helm init --client-only
helm plugin install https://github.com/rimusz/helm-tiller
helm version --client

exec "$SHELL"
