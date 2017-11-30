#!/bin/sh

set -e

if [ -e /.installed ]; then
  echo '============== Packages are installed ================'

else
	#=========================================================
	echo "==============Install the packages...==============="
	sudo apt-get update
	sudo apt-get -y install unzip vim tmux default-jdk python

	#=========================================================
	echo "==============Installing Python3.6...==============="
	sudo add-apt-repository -y ppa:jonathonf/python-3.6
	sudo apt-get update
	sudo apt-get -y install python3.6

	#=========================================================
	echo "=============== Installing Pipenv...================"
	sudo apt -y install python-pip
	sudo pip install pipenv==8.2.7

	#=========================================================
	echo "=============Installing geckodriver...=============="
	wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz 
	sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.19.1-linux64.tar.gz -O > /usr/bin/geckodriver'
	sudo chmod +x /usr/bin/geckodriver
	sudo rm geckodriver-v0.19.1-linux64.tar.gz

	#=========================================================
	echo "============ Installing chromedriver...============="
	CHROMEDRIVER_VERSION=$(curl "http://chromedriver.storage.googleapis.com/LATEST_RELEASE")
	wget "http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
	unzip chromedriver_linux64.zip
	sudo mv chromedriver /usr/bin/chromedriver
	sudo chmod +x /usr/bin/chromedriver
	sudo rm chromedriver_linux64.zip

	#=========================================================
	echo "======== Downloading Slenium StandAlone... ========="
	wget "https://selenium-release.storage.googleapis.com/3.5/selenium-server-standalone-3.5.0.jar"
	sudo mv selenium-server-standalone-3.5.0.jar /usr/bin/selenium_standalone.jar
	chmod +x /usr/bin/selenium_standalone.jar

	#=========================================================
	echo "=============Adding Pyroute to PATH...=============="
	echo "# ——— PYROUTE ——— #
export PYROUTEPATH=\$HOME/Pyroute/

pyroute_activate(){
    ssh-add ~/.ssh/id_rsa
    cd \$PYROUTEPATH
    pipenv shell
}
alias pyrouteenv=pyroute_activate" | sudo tee -a .bashrc >/dev/null

  touch /.installed
fi

#=========================================================
echo "==========Building Configuration Files...==========="
#======================Pipenv Files=======================
touch conf.sh
echo "#!/bin/sh
cd /home/ubuntu/Pyroute
pipenv --python /usr/bin/python3.6
pipenv install '-e .' --dev" >> conf.sh
mv conf.sh /usr/bin/config_pyroute.sh
chmod +x /usr/bin/config_pyroute.sh

#======================Selenium===========================
#=====================Standalone==========================
touch sel.sh
echo "
#!/bin/sh
tmux start-server
tmux new-session -d -s selenium
tmux send-keys -t selenium:0 'java -jar /usr/bin/selenium_standalone.jar -role hub' C-m" >> sel.sh
mv sel.sh /usr/bin/sel_up.sh
chmod +x /usr/bin/sel_up.sh

#================Setting Config.JSON=====================
#===============And First Pyroute Test===================
touch pyr_conf.sh
echo "#!/bin/sh
echo \"============== Setting Pyroute Config ==============\"
cd ~/Pyroute
mkdir Test
cd ~/Pyroute/Test
mkdir tests
mkdir config
touch config/config.json
touch tests/my_first_test.py
echo \"{
    \\\"tests\\\": {
        \\\"path\\\": [
            \\\"tests/my_first_test\\\"
             ]
    },
    \\\"modules\\\": {
        \\\"webdriver\\\": {
            \\\"desired_capabilities\\\": {
                \\\"browserName\\\": \\\"firefox\\\"
            },
            \\\"host\\\": \\\"http://127.0.0.1:4444/wd/hub\\\",
            \\\"url\\\": \\\"https://www.google.com\\\"
        }
    }
}\" >> config/config.json

echo \"============== Setting Pyroute Test ===============\"
echo \"from pyroute.tester import I
import time


def test():
    I.open_a_webpage('https://www.google.com')
    I.fill_field({'name' : 'q'}, 'Enroute')
    time.sleep(5)
    I.close()
\" >> tests/my_first_test.py" >> pyr_conf.sh
mv pyr_conf.sh /usr/bin/pyr_conf.sh
chmod +x /usr/bin/pyr_conf.sh


#=========================================================
echo "==========Adding Commands to .bashrc...============="
#=========================================================
echo "
pyroute_config(){
	echo 'Installing Pyroute...'
	sel_up.sh
	config_pyroute.sh 
	sleep 2
	pyr_conf.sh
}
alias Install_Pyroute=pyroute_config

alias ShutdownSelenium=\"tmux send-keys -t selenium:0 '^C' C-m\"
alias SeleniumOn=\"tmux send-keys -t selenium:0 'java -jar /usr/bin/selenium_standalone.jar -role hub' C-m\"

if [ \$(find ~ -name '.installed' | wc -l) -gt 0 ]; then
	sel_up.sh
	pyrouteenv
else
	sudo touch ~/.installed
	Install_Pyroute
fi" | sudo tee -a .bashrc >/dev/null

#=========================================================
echo "============= Pyroute is Ready to Use =============="

echo "===================================================="

echo "=========== Type 'vagrant ssh' to start ============"
