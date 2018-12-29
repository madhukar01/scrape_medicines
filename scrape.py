from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import xlsxwriter
import pickle

#alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alphabets = ['l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
max_pages = 1000
url = 'https://www.medindia.net/drug-price/brand-index.asp?alpha={alphabet}&page={page_number}'
medicines_list = []
pages_crawled = 0
count = 1

for alpha in alphabets:
    workbook = xlsxwriter.Workbook('medicines_list_' + alpha + '.xlsx')
    worksheet = workbook.add_worksheet()
    for num in range(1, 1000):
        pages_crawled += 1
        page = urlopen(url.format(alphabet=alpha, page_number=num))
        html_data = bs(page, 'html.parser')

        try:
            table = html_data.find('table', 'table-bordered table')
        except:
            print('Skipping to next page')
            break
        else:
            rows = table.findAll('tr')
            if len(rows) < 3:
                break
            for row in rows:
                for column in row.findAll('td'):
                    eles = column.findChildren('a')
                    if len(eles) > 0:
                        medicine_name = eles[0].getText()
                        medicine_url = eles[0]['href']
                        print(medicine_name)
                        if ' ' in medicine_url:
                            medicine_url = medicine_url.replace(' ', '')

                        medicine_page = urlopen(medicine_url)
                        medicine_html = bs(medicine_page, 'html.parser')
                        try:
                            div = medicine_html.find('div', {'class':'bbox'})
                            spans = div.findAll('span')
                            generic_name = spans[2].getText().split(':')[1].strip()
                            dose = spans[3].getText().strip()
                        except:
                            continue
                        else:
                            medicines_list.append((medicine_name, generic_name, dose))
                            worksheet.write(count, 0, medicine_name)
                            worksheet.write(count, 1, generic_name)
                            worksheet.write(count, 2, dose)
                            count += 1
                            print(generic_name, dose, '\n')
        print('Total medicines obtained: ', count)
        print('Total pages crawled: ', pages_crawled)
    workbook.close()

'''
except:
    print('======================================= Error occurred =======================================')
    pickle.dump(medicines_list, open('medicines_list.dat', 'wb'))
    workbook.close()
else:
    workbook.close()
    pickle.dump(medicines_list, open('medicines_list.dat', 'wb'))
    print('Crawling completed !!!')

#print(html_data, file=open('data.html', 'w', encoding='utf-8'))'''