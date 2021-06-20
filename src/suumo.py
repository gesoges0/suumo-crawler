from setting import SuumoIchiranPage, SummoChintaiPage
import os
from pathlib import Path
import subprocess
ROOT = Path('/mnt/da1fb3ab-8bd1-4b98-983e-b45899e50c48/suumo/')

def scrape_and_save(args):
    # 保存されたURLを取得する
    ichiran_page = SuumoIchiranPage() # 一覧ページ
    
    # 一覧ページにある物件を保存する
    for _ in ichiran_page.get_house_description_url():
        _.get_information()


def slack(args):
    # 呟く日
    d = args.DATE

    # 呟く日のdirecotry
    dir = ROOT / d
    if not dir.exists():
        assert f'directory {dir} is not exists!'
    
    # slackで呟く
    for i, chintai_dir in enumerate(os.listdir(dir)):
        chintai_dir_path = dir / chintai_dir
        description_path = chintai_dir_path / 'description.txt'

        with open(description_path, 'r') as f:
            rows = f.read().split('\n')
            for i, row in enumerate(rows):
                if i == 0:
                    url = row
                elif i == 1:
                    code = row
                elif i == 2:
                    name = row
                elif i == 3:
                    chinryo = row
                elif i == 4:
                    kanri_kyoeki = row
                elif i == 5:
                    shiki_rei = row
                elif i == 6:
                    gaikan_img = row.split(' : ')[0]
                elif i == 7:
                    madori_img = row.split(' : ')[0]
        text = f'{url}\n{chinryo}\n{kanri_kyoeki}\n{shiki_rei}\n{description_path}'
        image_url = f'{madori_img}'
        # attachment 書き込み
        subprocess.run(['python', '/home/gesogeso/デスクトップ/Slack-Tools/src/slack.py', 'write_attachment', '--color', 'good', '--title', f'{code}', '--text', f'{text}', '--image_url', f'{image_url}'])
        # payload 送信
        subprocess.run(['python', '/home/gesogeso/デスクトップ/Slack-Tools/src/slack.py', 'send_attachments', '-n', '0', '--text', f'{name}', '--icon_emoji', ':house:', '--username', '賃貸情報'])





        

    
    
        
    
