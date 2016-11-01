sudo dscl . -create /Users/research
sudo dscl . -create /Users/research UserShell /bin/bash
sudo dscl . -create /Users/research RealName "Research" 
sudo dscl . -create /Users/research UniqueID "510"
sudo dscl . -create /Users/research PrimaryGroupID 20
sudo dscl . -create /Users/research NFSHomeDirectory /Users/research
sudo dscl . -passwd /Users/research 

sudo systemsetup -setremotelogin on


/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install ganglia

wget https://raw.githubusercontent.com/uofthr/physicslab/master/su.cron
sudo crontab su.cron

su research

ssh-keygen

cd .ssh

wget https://raw.githubusercontent.com/uofthr/physicslab/master/authorized_keys
