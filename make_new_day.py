"""
Makes a new day for the advent of code
Usage: python make_new_day.py <day>
"""

import json
import sys
import requests
from bs4 import BeautifulSoup


class PuzzleTemplateGenerator:
    """Generates a new puzzle template"""

    def get_template(self):
        """Returns the template for the new day"""
        with open("./template.ipynb", "r", encoding="utf-8") as f:
            return json.load(f);

    def find_code(self, element, min_length):
        """Finds code in the element"""
        codes = element.find_all("code")
        for code in codes:
            if len(code.get_text()) >= min_length:
                return code.get_text()
       
    def fill_template(self, template, day):
        """Fills the template with the day"""
        
        # fetches the description of the day
        soup = self.request_soup(day)
        articles = soup.find_all("article", class_="day-desc")
        part1_description = articles[0].prettify()
        test_puzzle_input_part_1 = self.find_code(articles[0], 5)
        test_puzzle_input_solution = soup.find_all("code")[-1].get_text()
        
        # loops every cell and replaces {{DAY}} with the day
        for cell in template["cells"]:
            if "source" in cell:
                for i, line in enumerate(cell["source"]):
                    cell["source"][i] = line.replace("{{DAY}}", str(day))
                    cell["source"][i] = cell["source"][i].replace("{{DESCRIPTION}}", part1_description)
                    cell["source"][i] = cell["source"][i].replace("{{TEST_PUZZLE_INPUT_PART_1}}", test_puzzle_input_part_1)
                    cell["source"][i] = cell["source"][i].replace("{{TEST_PUZZLE_INPUT_SOLUTION}}", test_puzzle_input_solution)

        return template

    def write_template(self, template, day):
        """Writes the template to the file"""
        with open(f"./{str(day).zfill(2)}.ipynb", "w", encoding="utf-8") as f:
            json.dump(template, f, ensure_ascii=False, indent=4)

    def make_new_day(self, day):
        """Makes a new day"""
        template = self.get_template()
        template = self.fill_template(template, day)
        self.write_template(template, day)

    def request_soup(self, day):
        """requests the soup of the website"""
        url = f"https://adventofcode.com/2023/day/{day}"
        response = requests.get(url, timeout=5)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            return BeautifulSoup(response.text, 'html.parser')
        
        raise f"Failed to retrieve the webpage. Status code: {response.status_code}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        input_day = 2
    else:
        input_day = sys.argv[1]

    PuzzleTemplateGenerator().make_new_day(input_day)
