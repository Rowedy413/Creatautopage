NESSECRY PACKAGE

pkg update && pkg upgrade -y
pkg install python git -y

pip install requests colorama bs4


CMD 


rm -rf Creatautopage
git clone https://github.com/Rowedy413/Creatautopage.git
cd Creatautopage
python page.py
