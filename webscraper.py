from bs4 import BeautifulSoup
import requests
import re
#import pdb; pdb.set_trace()


class Webscraper:
    def __init__(self):
        self.html_code = None

    def validate_url(self, url):
        # URL validation logic using regular expression
        pattern = r'^(http|https):\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/\S*)?$'
        if re.match(pattern, url):
            return True
        else:
            return False

    def get_html_code(self, url):
        response = requests.get(url)
        self.html_code = response.text
        return self.html_code

    def get_elements(self):
        soup = BeautifulSoup(self.html_code, "html.parser")
        
        elements = [str(element) for element in soup.find_all()]
        return elements

    def scrape_data(self, selected_elements):
        soup = BeautifulSoup(self.html_code, "html.parser")
        data = []
        for selected_element in selected_elements:
            tag_match = re.match(r"<(\w+)", selected_element)
            if tag_match:
                tag = tag_match.group(1)
            else:
                # Invalid selected element format
                continue
            
            attributes_match = re.findall(r'(\w+)="([^"]*)"', selected_element)
            attributes = {attr: value for attr, value in attributes_match}
            
            element = soup.find(tag, attrs=attributes)
            if element:
                element_data = {
                    "tag": element.name,
                    "data": element.get_text()
                }
                if attributes:
                    element_data["attributes"] = attributes
                    element_data["attribute_count"] = len(attributes)
                else:
                    element_data["attribute_count"] = 0
                data.append(element_data)
        return data

