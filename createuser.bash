sudo xcodebuild -license accept
sudo dscl . -create /Users/research
sudo dscl . -create /Users/research UserShell /bin/bash
sudo dscl . -create /Users/research RealName "Research" 
sudo dscl . -create /Users/research UniqueID "510"
sudo dscl . -create /Users/research PrimaryGroupID 20
sudo dscl . -create /Users/research NFSHomeDirectory /Users/research

echo "Enter new research password"
sudo dscl . -passwd /Users/research 

sudo systemsetup -setremotelogin on


/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install ganglia

curl -O https://raw.githubusercontent.com/uofthr/physicslab/master/gmond.conf
sudo mv gmond.conf /usr/local/etc/gmond.conf

curl -O https://raw.githubusercontent.com/uofthr/physicslab/master/su.cron
sudo crontab su.cron

whoami
echo "su to research"

su research

whoami

cat /dev/zero | ssh-keygen -q -N ""

cd .ssh

curl -O https://raw.githubusercontent.com/uofthr/physicslab/master/authorized_keys
