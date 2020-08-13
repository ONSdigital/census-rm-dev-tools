# census-rm-dev-tools

Tools and scripts for cloudshell and concourse. Tools to be run inside the RM cluster can be found in [census-rm-toolbox](https://github.com/ONSdigital/census-rm-toolbox/).

## Configure and Whitelist Cloud Shell Tool

This repo includes scripts to configure the cloud shell to point at an RM cluster in a project and whitelist/un-whitelist itself.  

### Prerequisites
#### Install pyenv
Requres [pipenv](https://github.com/pypa/pipenv) and [pyenv](https://github.com/pyenv/pyenv)


To be able to use these scripts, you'll need to have [pyenv](https://github.com/pyenv/pyenv#installation) installed in your cloudshell environment to be able to install a python 3 version. To do this you can use these commands:
```shell script
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"
```

#### Install python 3 and pipenv
Once this is done, you should be able to install python 3 and pipenv dependencies using these commands:
```shell script
pyenv install 3.7.4
pyenv global 3.7.4
pip install pipenv
pipenv install --dev
```

### Set Up Aliases and Shortcuts
If you're going to be running these commands regularly it may be helpful to have the scripts on your `PATH` and set up some alias in your cloudshell bash.
Add these lines to your `~/.bashrc` file in the cloudshell 
```shell script
export PATH="<PATH_TO_CENSUS_RM_DEV_TOOLS>:$PATH"
alias prod-configure="configure_and_whitelist.sh census-rm-prod"
alias prod-exit="remove_from_whitelist.sh census-rm-prod"

function prod-toolbox {
    prod-configure
    kubectl exec -it $(kubectl get pods --selector=app=census-rm-toolbox -o jsonpath='{.items[*].metadata.name}') -- bash -c "export CLOUD_SHELL_USER=$LOGNAME && bash" || true
    prod-exit
}
```

The `prod-toolbox` function then gives you a single command to get into a toolbox pod and de-whitelist your cloudshell when it's finished.

### Usage
#### Configure and Whitelist
To point the cloudshell at a project and whitelist itself in the RM cluster, run
```shell script
configure_and_whitelist.sh <PROJECT_ID>
```

This changes the `gcloud` target project, generates the `kubectl` context and adds a whitelist entry to the target projects cluster for your current cloudshell IP.

#### Remove Whitelist Entry
To delete your cloudshell whitelist entry when you are finished, run
```shell script
remove_from_whitelist.sh <PROJECT_ID>
```

## Work From Home (WFH) Whitelist Script
To whitelist yourself on White Lodge and Black Lodge clusters and DB, plus a bunch of other things, run this script:
```bash
./whitelist_me_for_wfh.sh
```

## Colleague (i.e. tester) Work From Home (WFH) Whitelist Script
Once you have whitelisted yourself you can easily add all the whitelisting for a colleague who is working from home by running the following script:
```bash
./whitelist_for_wfh.sh <IP ADDRESS> <NAME OF PERSON>
```
