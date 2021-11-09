"""
    This is the Database.py class for the Software Inventory Tool Project
    This is the file where all the backend database information is handled
    This file was entirely made by the Puffins Team
    Version:10.20.2021
"""

import os.path
import pandas as pd
import bs4
import requests


class CVSSScorer:

    def __init__(self):
        pass

    # Retrieves NVD CVE html text string from link with certain id
    def website_query(self, id):
        # Requests is used to retrieve the link to a webpage
        result = requests.get(f'https://services.nvd.nist.gov/rest/json/cve/1.0/{id}')
        # BS4 is beautiful soup which is used to parse html from the above request
        # lxml is the type of html parser used. Must pip install lxml to work
        soup = bs4.BeautifulSoup(result.text, 'html.parser')
        return self.get_scoring(str(soup))

    # Parses through above query and returns CVSS score
    def get_scoring(self, query):
        # Retrieves the body text and finds the base cvss score
        find = query.find('baseScore')
        return query[find+11:find+14]


"""
Columns:
Name 
Status
Vulnerability
References
Comments
"""


class CVEDataFrame:
    df: pd.DataFrame

    def __init__(self):
        pass

    # Reads information from cvedb.xlsx
    def read_excel(self):
        self.df = pd.read_excel('cvedb.xlsx')

    # ONLY TO BE RAN ONCE IF cve.db.metadata NOT ALREADY MADE
    # THIS IS FOR TIME EFFICIENCY
    def create_metadata(self):
        if not os.path.exists('cve.db.metadata'):
            self.read_excel()

            # Creates a file called cve.db.metadata and writes each record in
            # Metadata files tend to be a lot more efficient and time saving when looking up records
            # This being compared to pandas dataframes
            # The only down side being space. This json-txt file hybrid is almost 4x as large
            with open('cve.db.metadata', 'w', encoding='UTF-8') as f:
                for i in self.df.index:
                    # Only writing four columns from the original xlsx file. Felt that these were most important
                    f.write(f'{self.df["Name"][i]}~/~{self.df["Vulnerability"][i]}~/~'
                            f'{self.df["References"][i]}~/~{self.df["Comments"][i]}\n')
            f.close()

    def select_record_by_name(self, name: str):
        query_list = []
        with open('cve.db.metadata', encoding='UTF-8') as f:
            for record in f:
                if name.lower() in str(record).lower():
                    query_list.append(record.split('~/~'))
        f.close()
        return query_list


if __name__ == '__main__':
    cve = CVEDataFrame()
    cve.create_metadata()
    # print(cve.select_record_by_name('chrome'))
    # Create a CVSSScorer() obj and call .website_query wit the CVE tag as shown below to parse the cvss score
    cvss = CVSSScorer()
    print(cvss.website_query('CVE-1999-0001'))