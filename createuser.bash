sudo xcodebuild -license accept
sudo dscl . -create /Users/research
sudo dscl . -create /Users/research UserShell /bin/bash
sudo dscl . -create /Users/research RealName "Research" 
sudo dscl . -create /Users/research UniqueID "510"
sudo dscl . -create /Users/research PrimaryGroupID 20
sudo dscl . -create /Users/research NFSHomeDirectory /Users/research
sudo dscl . append /Groups/com.apple.access_ssh user research
sudo dscl . append /Groups/com.apple.access_ssh groupmembers `dscl . read /Users/research GeneratedUID | cut -d " " -f 2`


sudo cp -R /System/Library/User\ Template/English.lproj /Users/research
sudo chown -R research:staff /Users/research

echo "================================"
echo "================================"
echo "================================"
echo "Enter new research user password"
echo "================================"
echo "================================"
echo "================================"
sudo dscl . -passwd /Users/research 

sudo systemsetup -setremotelogin on
sudo dseditgroup -o edit -a research -t user admin
sudo dseditgroup -o edit -a research -t user wheel

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install ganglia

curl -O https://raw.githubusercontent.com/uofthr/physicslab/master/gmond.conf
sudo mv gmond.conf /usr/local/etc/gmond.conf

curl -O https://raw.githubusercontent.com/uofthr/physicslab/master/su.cron
sudo crontab su.cron

curl -O https://raw.githubusercontent.com/uofthr/physicslab/master/metric.bash

sudo pmset autorestart 1
sudo -u research whoami
sudo sh -c 'echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers'
sudo sh -c '(crontab -l 2>/dev/null; echo "* * * * * /bin/bash /Users/research/metric.bash")| crontab -'

sudo -u research mkdir /Users/research/.ssh

sudo -u research ssh-keygen -q -N "" -f /Users/research/.ssh/id_rsa

sudo -u research curl https://raw.githubusercontent.com/uofthr/physicslab/master/authorized_keys --output /Users/research/.ssh/authorized_keys



sudo reboot
