
# Dev tools
export PATH="$HOME/census-rm-dev-tools:$PATH"
alias set-project="gcloud config set project"

function whitelist {
    configure_and_whitelist.sh $GOOGLE_CLOUD_PROJECT
}

function dewhitelist {
    remove_from_whitelist.sh $GOOGLE_CLOUD_PROJECT
}

function exec-toolbox {
    kubectl exec -it $(kubectl get pods --selector=app=census-rm-toolbox -o jsonpath='{.items[*].metadata.name}') -- bash -c "export CLOUD_SHELL_USER=$LOGNAME && bash" || true
}

function toolbox {
    whitelist
    exec-toolbox
    dewhitelist
}
