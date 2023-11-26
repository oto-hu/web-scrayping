import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_website(url, keyword, tag=None):
    patterns = {
        '電話番号': r'\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}',
        'メールアドレス': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        #ここに追加
    }

    def scrape_single_page(url, keyword, tag):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            if keyword in patterns:
                text = soup.get_text()
                pattern = patterns[keyword]
                matches = re.findall(pattern, text)
                return matches, ""
            else:
                if tag is None:
                    return None, "タグを指定してください"
                sentences = []
                elements = soup.find_all(tag)
                for element in elements:
                    text = element.get_text()
                    sentences.extend(re.findall(r'[^。]*?{}[^。]*。'.format(re.escape(keyword)), text))
                return sentences, ""
        except requests.RequestException:
            return None, "無効なURLです"
        except Exception as e:
            return None, str(e)

    results, message = [], ""
    # 最初に指定されたURLから抽出
    main_results, main_message = scrape_single_page(url, keyword, tag)
    if main_results:
        results.extend([(url, result) for result in main_results])

    # 内部リンクを探す
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]
        for link in links:
            link_results, link_message = scrape_single_page(link, keyword, tag)
            if link_results:
                results.extend([(link, result) for result in link_results])
    except requests.RequestException:
        return None, "無効なURLです"
    except Exception as e:
        return None, str(e)

    return results, message
