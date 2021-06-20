from argparse import ArgumentParser
from os import pardir

from setting import change_setting
from suumo import scrape_and_save, slack

if __name__ == '__main__':
    parser = ArgumentParser(description='suumo scraper')
    subparsers = parser.add_subparsers(help='sub-commands')
    subparsers.required = True
    subparsers.dest = 'SUB_COMMAND'

    # 設定を変更
    parser_change_setting = subparsers.add_parser('set', help='設定を変更する')
    parser_change_setting.add_argument('--gui', type=str, help='GUIを開く')
    parser_change_setting.set_defaults(func=change_setting)

    # スクレイピングしてDBへ保存
    parser_scrape_and_save = subparsers.add_parser('scrape', help='スクレイピングしてDBへ保存')
    parser_scrape_and_save.set_defaults(func=scrape_and_save)

    # slackへ投稿
    parser_slack = subparsers.add_parser('slack', help='slackへ投稿')
    parser_slack.add_argument('DATE', type=str, help='データを取得した日付')
    parser_slack.set_defaults(func=slack)



    args = parser.parse_args()
    args.func(args)


