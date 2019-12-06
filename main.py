# 词云
from wordcloud import WordCloud
import PIL .Image as Image
import numpy as np
# 结巴 分词
import jieba
import requests
import json
import bs4

# 构建请求头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Cookie': '_ga=GA1.2.2063358900.1556201729; '
              'device_id=5c4791e144154bdac4cac28eb44e8205;'
              'aliyungf_tc=AQAAACIUgAhVdwkA0l7gelelDQK2hRw6;'
              'xq_a_token=5e0d8a38cd3acbc3002589f46fc1572c302aa8a2;'
              'xq_a_token.sig=ZvtaY2gpozjtDgM9XQBm-U6v7VE;'
              'xq_r_token=670668eda313118d7214487d800c21ad0202e141;'
              'xq_r_token.sig=nB5LZeMGKYGGQHzx5fGb8InoJlQ;'
              'gid=GA1.2.1611213571.1556421100;'
              'u=281575539594633;'
              'Hm_lvt_1db88642e346389874251b5a1eded6e3=1575539596;'
              'Hm_lpvt_1db88642e346389874251b5a1eded6e3=1575613105'
}
url = "https://xueqiu.com"
param = {
         'count': 10,
         'page': 1
         }


def translate_to_chinese(string):
    word_list = jieba.cut(string)
    # 分词后在单独个体之间加上空格
    result = " ".join(word_list)
    return result;


def get_html_content(keyword):
    # 填入关键字
    param['q'] = keyword
    response = requests.get(url + "/statuses/search.json", params=param, headers=headers)
    print(response)
    # 获取链接数据
    link_data = json.loads(response.text)['list']
    index = 0
    for item in link_data:
        response = requests.get(url + item["target"], headers=headers)
        # 使用BeautifulSoup解析代码,并锁定页码指定标签内容
        html_content = bs4.BeautifulSoup(response.text, "html.parser")
        [s.extract() for s in html_content("img")]
        [s.extract() for s in html_content("br")]
        article_content = html_content.find(class_='article__bd__detail')
        # p = article_content.descendants
        # soup = bs4.BeautifulSoup(article_content.children, 'html.parser')
        # k = soup.find_all('p')
        # print(article_content.get_text())
        fh = open("word.txt", 'a', encoding='utf-8')
        fh.write(article_content.get_text())
        fh.write("\n")
        fh.close()
        index += 1
    print("获取文字并成功写入文件...")


def create_word_cloud():
    fp = open("word.txt", "rb")
    text = fp.read()
    text = translate_to_chinese(text)
    # print(text)
    mask = np.array(Image.open("img.jpg"))
    word_cloud = WordCloud(
        mask=mask,
        font_path="C:\\Windows\\Fonts\\simfang.ttf",
        background_color="white"
    ).generate(text)
    img = word_cloud.to_image()
    # img.show()
    word_cloud.to_file("result.png")
    print("词云已生成！")


def main():
    keyword = input('What is your search keyword?\n')
    total_page = get_html_content(keyword)
    for i in range(total_page):
        get_html_content(keyword)
    create_word_cloud()


if __name__ == '__main__':
    main()
