dscl . -create /Users/research
dscl . -create /Users/research UserShell /bin/bash
dscl . -create /Users/research RealName "Research" 
dscl . -create /Users/research UniqueID "510"
dscl . -create /Users/research PrimaryGroupID 20
dscl . -create /Users/research NFSHomeDirectory /Users/research
dscl . -passwd /Users/research 

sudo systemsetup -setremotelogin on


/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install ganglia




su research

ssh-keygen

cd .ssh

wget https://gist.githubusercontent.com/hannorein/9699e70451526957d5c6e442399192d6/raw/4a770031e3fc4cd7a48dfce5b7a9f7ce59150856/authorized_keys

