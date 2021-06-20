from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from typing import NamedTuple, Generator, List, Dict, Any
import csv
from time import sleep
from selenium import webdriver
import os
import subprocess
import datetime

ROOT = Path('/mnt/da1fb3ab-8bd1-4b98-983e-b45899e50c48/suumo/')

def change_setting(args):
    print('setting')

class SuumoIchiranPage(NamedTuple):
    """賃貸一覧ページの情報を表すクラス"""
    # url: str = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&ae=02901&cb=0.0&ct=8.5&co=1&et=20&md=04&cn=15&mb=0&mt=9999999&kz=1&tc=0400102&tc=0400301&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&rn=0280&rn=0290&srch_navi=1"
    url: str = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&cb=0.0&ct=8.5&et=9999999&md=04&cn=9999999&mb=0&mt=9999999&kz=1&tc=0400102&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&rn=0280'

    def _get_page_soup(self) -> BeautifulSoup:
        """一覧ページのsoupを返す"""
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup

    def get_house_description_url(self) -> Generator[Any, None, None]:
        """各物件のURLを取得する"""
        soup = self._get_page_soup()
        for inner_html in soup.find_all('td', class_='ui-text--midium ui-text--bold'):
            url = 'https://suumo.jp' + inner_html.find('a').get('href')
            yield SummoChintaiPage(url)


class SummoChintaiPage(NamedTuple):
    """賃貸1物件あたりの情報を表すクラス"""
    url: str

    def _get_page_soup(self) -> BeautifulSoup:
        """賃貸1物件あたりのsoupを返す"""
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup

    def get_information(self):
        """欲しい情報を返す"""
        soup = self._get_page_soup()

        # soup から欲しい情報を抽出する
        info = {}

        # メタ
        name = soup.find('h1', class_='section_h1-header-title').text
        url = self.url
        code = self.url.split('=')[-1]
        
        # 賃料
        chinryo = soup.find('span', class_='property_view_note-emphasis').text
        kanri_kyoeki = soup.find('div', class_='property_view_note-list').find_all('span')[1].text.split(' ')[-1]
        shiki_rei = soup.find_all('div', class_='property_view_note-list')[1].text.replace('\n', ', ')[2:-2]
        
        # 大きい画像
        img_elements = [_.find('img') for _ in soup.select('a.property_view_object.js-view_gallery-object.js-lazyload')]
        img_descriptiions = [_.get('alt') for _ in img_elements]
        img_srcs = [_.get('data-src') for _ in img_elements]
        
        # 保存先ディレクトリ
        date_dir = ROOT / f"{datetime.datetime.now().strftime('%Y%m%d')}"
        if not date_dir.exists():
            os.mkdir(date_dir)
        file_dir = date_dir / f'{code}'
        if not file_dir.exists():
            os.mkdir(file_dir)
        else:
            return

        # 画像ダウンロード
        for i, (img_description, img_src) in enumerate(zip(img_descriptiions, img_srcs)):
            res = requests.get(img_src, allow_redirects=False)
            image = res.content
            file_path = file_dir / f'file_name_{i}.jpg'
            with open(file_path, 'wb') as f:
                f.write(image)

        # 画像の説明を書き込み
        description_path = file_dir / 'description.txt'
        with open(description_path, 'w') as f:
            f.write(f'{self.url}\n')
            f.write(f'{code}\n')
            f.write(f'{name}\n')
            f.write(f'賃料：{chinryo}\n')
            f.write(f'管理共益：{kanri_kyoeki}\n')
            f.write(f'敷金礼金：{shiki_rei}\n')
            for i, (img_description, img_src) in enumerate(zip(img_descriptiions, img_srcs)):
                f.write(f'{img_src} : {img_description}\n')
        
        # 小さい画像
        # imgs_elements = [_.find('img') for _ in soup.select('a.property_view_thumbnail.js-view_gallery-thumb.js-lazyload')]
        # img_descriptiions = [_.get('alt') for _ in imgs_elements]
        # img_srcs = [_.get('data-src') for _ in imgs_elements]
        # print(img_srcs)
        
        # 部屋の特徴・設備のスクショ
        # 物件概要スクショ
        download_directory = f'{file_dir}'
        prefs = {'profile.default_content_setting_values.automatic_downloads': 1, "download.default_directory" : download_directory}
        options = Options()
        options.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome('./chromedriver', chrome_options=options)
        browser.get(self.url)
        with open('html2canvas.js', 'r') as h2c, open('jquery-3.6.0.min.js', 'r') as jq, open('screenshot.js', 'r') as f:
            browser.execute_script(h2c.read())
            browser.execute_script(jq.read())
            browser.execute_script(f.read())
        sleep(10)

        # 「ダウンロード」から/mnt/da1fb3ab-8bd1-4b98-983e-b45899e50c48/suumo へファイルをmv
        # print(f'{file_dir}')
        # subprocess.run(['mv', '/home/gesogeso/ダウンロード/screenshot_00.png', f'{file_dir}'])
        # subprocess.run(['mv', '/home/gesogeso/ダウンロード/screenshot_01.png', f'{file_dir}'])


        # slack
        # python slack.py write_attachment --color 'good' --title 
        
        

        






        


class ChintaiInformation(NamedTuple):
    """1物件に対して欲しい情報を表すクラス"""
    name: str # 物件の名前
    url: str # 物件のURL
    # 賃料
    chinryo: str # 物件の価格
    kanri_kyoeki: str # 管理・共益費
    shiki_rei: str # 敷金
    # 所在地
    shozaichi: str # 所在地
    ekitoho: List[str] # 駅徒歩
    madori: str # 間取り
    # 部屋の特徴・設備
    tokucho: List[str] # 部屋の特徴
    # 物件概要
    madori: str # 間取り
    kaisu: str # 階数
    sunpo: str # 損保
    nyukyo: str # 相談
    code: int # 物件コード
    architecture: str # 構造
    chiku: str # 築年数
    img_paths: List[Path] # 画像を保存するためのPath
    img_urls: List[str] # 画像のhref





    

    # def get_information(self):
    #     soup = self.get_page_soup()

        # IDを取得


        # 画像一覧を取得


        # html2canvasで所在地などの表を画像化してpathを返す

        # 部屋の特徴をstrで取得

        # 物件概要をhtml2canvasで画像化してpathを返す

        # 周辺情報をhtml2canavsで画像化



# ra=013
# pc=30&smk=&po1=25&po2=99&ra=013&md=04 # 1LDK

# "https://suumo.jp/jj/chintai/ichiran/"
# "FR301FC001/" # 京王線 & 京王相模原線
# "?ar=030"
# "&bs=040"
# "&fw2="
# "&pc=30"
# "&po1=25"
# "&po2=99"
# "&ra=013"
# "&rn=0280"
# "&rn=0290"
# "&ek=028014740"
# "&ek=028034190"
# "&ek=028024440"
# "&ek=028029060"
# "&ek=028026310"
# "&ek=028038820"
# "&ek=028023640"
# "&ek=029024440"
# "&ek=029013340"
# "&ek=029037360"
# "&ek=029023480"
# "&ek=029030490"
# "&md=04"
# "&cb=0.0" # 賃料下限 (万円)
# "&ct=8.5" # 賃料上限 (万円)
# "&et=9999999"
# "&mb=0"
# "&mt=9999999"
# "&cn=15"
# "&ae=02901"
# "&co=1"
# "&kz=1"
# "&tc=0400102"
# "&tc=0400301"
# "&shkr1=03"
# "&shkr2=03"
# "&shkr3=03"
# "&shkr4=03"