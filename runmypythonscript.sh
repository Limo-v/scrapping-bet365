# !/bin/bash
echo "my cronjob is working!" >> ./file.txt
cd /home/betuser/scrapping_bet365/
pip install -r requirements.txt
source scrapper/bin/activate
python3 crwbet365.py