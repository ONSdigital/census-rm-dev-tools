# census-rm-dev-tools

Tools and scripts for cloudshell and concourse. Tools to be run inside the RM cluster can be found in [census-rm-toolbox](https://github.com/ONSdigital/census-rm-toolbox/).

## Cloudshell Setup
### Start a cloudshell
See https://cloud.google.com/shell/docs for help on cloudshell basics and documentation. Proceed with these steps once you have a cloudshell command line ready.

### Clone this repo
```shell script
git clone https://github.com/ONSdigital/census-rm-dev-tools.git ~/census-rm-dev-tools
```

### Set up python and dev/support shortcuts
Run these commands in your cloudshell. It may take a few minutes to install python.
```shell script
pushd ~/census-rm-dev-tools
./cloudshell_setup/setup_python_and_tools.sh
popd
```

This installs pyenv, pipenv and some useful functions and aliases

Try testing it with
```shell script
set-project census-rm-ci
toolbox
```
This should whitelist your cloudshell in the census-rm-ci project and connect you to the toolbox in the CI cluster.

Exit with `CTRL+D` or the `exit` command and you should see the script report that it has successfully de-whitelisted you on exit tidy up.  

### Functions and aliases usage
After setting up python and the dev tools you should should be able to use the following aliases and functions:

#### Set the current gcloud project with
```shell script
set-project <PROJECT NAME>
```

#### Access the toolbox in the current project with
```shell script
toolbox
```
This should whitelist your cloudshell, exec into the toolbox in the currently configured project, then de-whitelist on exit.
If the de-whitelisting fails for any reason (it can only run one concurrent update at a time which can cause conflicts), run `dewhitelist` manually to complete the tidy up.

#### Whitelist your cloudshell
To run `kubectl` commands you may want to whitelist your cloudshell manually with
```shell script
whitelist
```
It is then important to:
#### De-whitelist your cloudshell
```shell script
dewhitelist
```

### Terraform and Helm
We use terraform (via tfenv) and helm v2 with the tillerless plugin for our infrastructure management, these are the steps to set up those tools on your cloudshell. This is only necessary if you need to be able to make infrastructure changes.

#### Creating a github personal token
Clone the terraform repo with
The easiest way to clone the terraform repo on a cloudshell is with a personal token. Follow the steps here https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token and create a token with only "repo" permissions.
**Do not** store this token anywhere. If you need to clone or pull the repo again just regenerate the token. Copy the token, you'll need it for the next step.

#### Run the setup script
```shell script
pushd ~/census-rm-dev-tools
./cloudshell_setup/setup_terraform_and_helm.sh
popd
```
The first thing this does is attempt to clone our terraform repo. You will be prompted for your github username and password. Enter your username as normal but paste the access token in the place of the password.
It then installs `tfenv` and `helm v2` plus the tillerless plugin. The first time you run any terraform commands, `tfenv` should automatically install and use the required `terraform cli` version.

#### Checking out a terraform release
If you need to run terraform at a tagged version run
```shell script
cd ~/census-rm-terraform
git checkout <TAG>
```
This should prompt you again for your github credentials so you'll need to regenerate your access token from earlier. Navigate to the token you created in your github developer settings and click `regenerate token` and copy the regenerated token.
Paste the token in place of your password again and it should check out the tag you passed in.


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
