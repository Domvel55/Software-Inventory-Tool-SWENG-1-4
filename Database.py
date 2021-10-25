"""
    This is the Database.py class for the Software Inventory Tool Project
    This is the file where all the backend database information is handled
    This file was entirely made by the Puffins Team
    Version:10.20.2021
"""

import os.path
import pandas as pd

"""
Columns:
Name 
Status
Vulnerability
References
Phase
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
        with open('cve.db.metadata', encoding='UTF-8') as f:
            for record in f:
                if name.lower() in str(record).lower():
                    print(record)
        f.close()


if __name__ == '__main__':
    cve = CVEDataFrame()
    cve.create_metadata()
    cve.select_record_by_name('excel')
