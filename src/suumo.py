from setting import SuumoIchiranPage, SummoChintaiPage


def scrape_and_save(args):
    # 保存されたURLを取得する
    ichiran_page = SuumoIchiranPage() # 一覧ページ
    
    
    for _ in ichiran_page.get_house_description_url():
        _.get_information()



    # pageから各賃貸の情報を取得

