## WIP:
## Installation
To install Pyroute you may choose one out of three different options:
* Pipenv
* Vagrant
* Docker

## Install Pyroute using Pipenv

 1. Clone this repo, we use `develop` branch for development.
 2. Install pipenv on global python from your machine `pip install --user pipenv`
 3. Run `pipenv --three`
 4. Run `pipenv install '-e .' --dev`
 5. Go to your *~/.bashrc* or *~/.zshrc*
 6. Edit the file and issue these commands to setup an alias
 7. Restart your terminal


**This works with zsh shell:**
```
# ——— PYROUTE ——— #
export PYROUTEPATH=$HOME/Projects/pyroute

pyroute_activate(){
    ssh-add ~/.ssh/id_rsa
    cd $PYROUTEPATH
    pipenv shell
}
alias pyrouteenv=pyroute_activate
```

* Create a test folder in different location than pyroute code

* Create a subfolder named `config`

* Create a `config.json` file, copy and save the following to it:

```
{
    "tests": {
        "path": [
    "tests/modules/webdriver/WDM_test_get_current_url.py"
                ],
        "preffix": "test_",
        "data": "$PATH",
		    "verbosity": "LOW"
   },
    "modules": {
        "webdriver": {
        	"desired_capabilities": {
            	"browserName": "firefox",
            	"version": "57"
          		},
        "keep_cookies": "1",
        "host": "http://127.0.0.1:4444/wd/hub",
        "url": "http://www.enroute.xyz"
        			}
   				},
    "colors": {
        "color": "on",
        "custom": "BRG_CYAN",
        "error": "RED",
        "failure": "BRG_RED",
        "loading_modules": "BRG_WHITE",
        "loading_tests": "BRG_WHITE",
        "modules_loaded": "BRG_WHITE",
        "passed_time": "BRG_GREEN",
        "pyroute_logo": "BRG_YELLOW",
        "running_test": "BRG_WHITE",
        "finished_test": "BRG_CYAN",
        "tests_completed": "BRG_GREEN",
        "tests_loaded": "BRG_WHITE",
        "warning": "ORANGE"
      }
}

```

* Create a `pyroute_tests_folder` folder

* Create a file named `features.py`

* From this folder you're going to run `pyroute run` command


## Install Pyroute using Vagrant

**Install Vagrant and Virtual Box**
 1. Install vagrant using the commands

```
wget https://releases.hashicorp.com/vagrant/1.9.3/vagrant_1.9.3_x86_64.deb
sudo dpkg -i vagrant_1.9.3_x86_64.deb
```
 2. Install VirtualBox using the command `sudo apt-get install virtualbox`
 3. Install the vagrant box `ubuntu/xenial64` using the command
     `vagrant box add ubuntu/xenial64`

**Set Up Pyroute with Vagrant**
 1. Clone this repo, we use `develop` branch for development.
 2. From the cloned repo run `vagrant up` this will setup everything (It will take some time to install everything)
 3. Once everything is installed run `vagrant ssh` to log into the machine

**Run the first Pyroute Test**
 1. Open a new Terminal in your Local Machine
 2. Run selenium standalone in your local machine using the following command
    `java -jar selenium-server-standalone-3_X_X.jar -role node -hub http://10.0.0.10:4444/grid/register`
 3. Go to the terminal where your virtual machine is logged in and type `pyrouteenv`
 4. Go to the directory /Test using the command `cd Test`
 5. Once the standalone is up and you are placed in the correct directory use:
    `pyroute run`
 6. This will run your first test.

 **NOTE**
 * Selenium Standalone Server must be up to date or at least 3.5.0 (On your local machine)
 * Selenium Standalone is running on the background (On your virtual machine)
 * To turn off Selenium Standalone run `ShutdownSelenium` (On your virtual machine)
 * If Selenium Standalone is not running or you Shut it down, just run `SeleniumOn` to turn it on again. (On your virtual machine)
