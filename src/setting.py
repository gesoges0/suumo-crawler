from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.options import Options
from typing import NamedTuple, Generator, List, Dict, Any
import csv

ROOT = '/mnt/da1fb3ab-8bd1-4b98-983e-b45899e50c48/suumo/'

def change_setting(args):
    print('setting')

class SuumoIchiranPage(NamedTuple):
    """賃貸一覧ページの情報を表すクラス"""
    url: str = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&ae=02901&cb=0.0&ct=8.5&co=1&et=20&md=04&cn=15&mb=0&mt=9999999&kz=1&tc=0400102&tc=0400301&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&rn=0280&rn=0290&srch_navi=1"

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


    def save_to_db(self):
        pass

        
        


class ChintaiInformation(NamedTuple):
    """1物件に対して欲しい情報を表すクラス"""
    url: str # 物件のURL
    # 賃料
    chinryo: float # 物件の価格
    kari_kyoeki: int # 管理・共益費
    shiki: int # 敷金
    rekin: int # 礼金
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