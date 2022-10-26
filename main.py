# if the bot fails to work- change the selenium driver!


class Millioner:
    def __init__(self):
        self.group_url = 'https://finviz.com/groups.ashx?g=sector&v=140&o=name'

    def get_successful_group(self):
        # the group url is known
        from bs4 import BeautifulSoup
        import requests
        import pandas as pd

        pd.set_option('display.max_columns', None)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        }
        # Try parsing
        try:
            response = requests.get(self.group_url, headers=headers).text
            soup = BeautifulSoup(response, 'html.parser')
            # table = soup.find('table', attrs={'class': 'table-light'})

            # list of names for columns
            columns = [col.text for col in soup.findAll('td', {'class': 'table-top cursor-pointer'})]
            columns.insert(1, "Name")

            all_rows_in_one_str = [row.text for row in soup.findAll('td', {'class': 'body-table'})]

            # I need to split list into chunks of 13 (columns), and each list will become a new row
            chunk_size = 13
            rows = [all_rows_in_one_str[i:i + chunk_size] for i in range(0, len(all_rows_in_one_str), chunk_size)]

            df = pd.DataFrame(columns=columns)
            for row in rows:
                # Add each row to the end of df
                df.loc[len(df)] = row
            # Drop column 'No.'
            df = df.drop(['No.'], axis=1)
            # I have a dataframe at this point
            print(df)

            # Parse links for every sector in the table
            links_for_sector = []
            for row in soup.findAll('td', {'class': 'body-table'}):
                try:
                    a = row.a
                    # href = href.find('a.href')
                    if a:
                        # base_url + href = full link, append each link to list
                        links_for_sector.append('https://finviz.com/' + a.get('href'))
                except:
                    # ignore every item except the one that contains tag <a>
                    continue
            print(f"Links for sector: {links_for_sector}")

            # Append links to dataframe

            df['Url'] = links_for_sector

            # get rid of "%" in some columns
            df['Perf Week'] = df['Perf Week'].str.replace('%', '')
            df['Perf Month'] = df['Perf Month'].str.replace('%', '')
            df['Perf Quart'] = df['Perf Quart'].str.replace('%', '')

            print('Successfully removed %')

            df['Perf Week'] = pd.to_numeric(df['Perf Week'])
            df['Perf Month'] = pd.to_numeric(df['Perf Month'])
            df['Perf Quart'] = pd.to_numeric(df['Perf Quart'])

            print('Successfully converted to numeric')

            df['Sum'] = df['Perf Week'] + df['Perf Month'] + df['Perf Quart']
            print('Successfully added columns for comparison')

            # sort df to show biggest 'Sum' first
            sorted = df.sort_values('Sum', ascending=False)
            print(sorted)
            print('Successfully sorted df')

            # winner's url:

            winner_url = sorted['Url'].iloc[0]
            print(f'Winner url: {winner_url}')
            return winner_url

        # If parsing website change- catch the error to prevent program crash
        except Exception as e:
            return e

    def run_in_order(self):
        self.get_successful_group()


if __name__ == '__main__':
    millioner = Millioner()
    millioner.run_in_order()

# driver.get('https://finviz.com')
#
# time.sleep(3)

# # Accept privacy
# driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[3]').click()
# time.sleep(2)
# # switch to Groups
# driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[5]/a').click()
# time.sleep(1000)

#---------------------
# from selenium import webdriver
# # selenium 4.5.0
# from selenium.webdriver.common.by import By
#
# import time
#
# driver = webdriver.Chrome()
#
# groups_url = 'https://finviz.com/groups.ashx'
# driver.get(groups_url)
# time.sleep(3)
# # Accept privacy
# driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[3]').click()
# time.sleep(2)