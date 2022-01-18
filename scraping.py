import requests as req
import urllib
import urllib.request
import json
import os
#import csv
import sys
import wget

from os import path
from importlib import reload

# url respon
url1 = "https://shopee.co.id/api/v4/search/search_items?by=pop&entry_point=ShopByPDP&limit=30&match_id={}&newest={}&order=desc&page_type=shop&scenario=PAGE_OTHERS&version=2"
url2 = "https://shopee.co.id/api/v4/item/get?itemid={}&shopid={}"
url3 = "http://cf.shopee.co.id/file/"

# respon search url


def product_id(match_id, newest):
    url = (url1).format(match_id, newest)
    resp = urllib.request.urlopen(url)
    parsed = json.load(resp)
    return parsed

# respon produk detail


def product_detail(itemid, shopid):
    url = (url2).format(itemid, shopid)
    resp = req.get(url).json()
    return resp


# membuat folder
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


# main
if __name__ == "__main__":

    user_id = input('Masukkan ID: ')
    range_id = int(input('Masukkan data yang diambil: '))
    for i in range(0, range_id, 30):
        products = product_id(user_id, i)

        for j in range(30):
            item_id = products['items'][j]['item_basic']
            shop_id = item_id['shopid']
            # nama = products['items'][i]['name']
            ite_m = product_detail(item_id['itemid'], item_id['shopid'])

            # parsing data
            iditem = ite_m['data']['itemid']
            prod = ite_m['data']['name']
            # bran = ite_m['data']['brand']
            deskrip = ite_m['data']['description']
            price_min = ite_m['data']['price_min']
            price_max = ite_m['data']['price_max']
            stok = ite_m['data']['stock']
            harga = ite_m['data']['price']
            gambar = ite_m['data']['images']
            variasi = ite_m['data']['tier_variations']
            kategori = ite_m['data']['categories']
            """
            data = {"details": [{
                "Id": iditem,
                "produk": prod,
                "brand": bran,
                "deskripsi": deskrip,
                "price_min": price_min,
                "price_max": price_max,
                "stok": stok,
                "harga": harga,
                "gambar": gambar
            }]}
            """
            # dalam data
            createFolder('./%s/%s/images' % (str(shop_id), str(prod)))
            path1 = str(shop_id)
            path2 = str(prod)
            exists = path.isdir('./' + path1 + '/' + path2)
            if exists:
                path3 = './' + path1 + '/' + path2
                # csv_data = open(path3 + '/Data.csv', 'w')
                """
                # membuat csv
                reload(sys)
                data = data['details']
                tulis_data = open(path3 + '/Data.csv', 'w')

                csvwriter = csv.writer(tulis_data)
                count = 0
                for emp in data:
                    if count == 0:
                        header = emp.keys()
                        csvwriter.writerow(header)
                        count += 1
                    csvwriter.writerow(emp.values())
                tulis_data.close()
                """
                for s in range(len(kategori)):
                    cat_id = kategori[s]['catid']
                    displayname = kategori[s]['display_name']
                    displaynames = (str(cat_id) + ":" + displayname)
                    # lin = 'Kategori = ' + displaynames
                    # save txt
                    line = ['ID Item = ' + str(iditem), 'Produk = ' + prod, 'Deskripsi = ' + deskrip, 'price_min = ' +
                            str(price_min), 'price_max = ' + str(price_max), 'Harga = ' +
                            str(harga), 'Nama = ' +
                            str(variasi[0]['name']
                                ), 'Kategori = ' + displaynames,
                            'Opsi = ' + str(variasi[0]['options']), 'Gambar = ' + str(gambar), 'Gambar varian = ' + str(variasi[0]['images'])]
                    with open(path3 + '/data.txt', 'w') as text:
                        for lines in line:
                            text.write(lines)
                            text.write('\n')
                            # text.close()

                # Gambar
                pars_gambar = {"Gambar": gambar}
                p_gambar = pars_gambar['Gambar']
                my_image_len = len(p_gambar)
                path4 = path3 + '/images'

                for r_image in range(my_image_len):
                    gambark = p_gambar[r_image]
                    dirgambar = path4 + '/%s' % (gambark)
                    exist = os.path.isfile(dirgambar)
                    url_mage = (url3) + gambark
                    # download url_mage
                    if exist:
                        try:
                            os.remove(dirgambar)
                        except OSError:
                            pass
                    wget.download(url_mage, path4 + "/%s.jpg" % (gambark))
            else:
                print("data nggak ada")
                # text.close()
