####################
# İŞLEMLER

# OLUŞTURDUĞUMUZ TXT DOSYASINA FİYAT VE BAŞLIĞINI ALMAK İSTEDİĞİMİZ
# ÜRÜNLERİN LİNKLERİNİ VERECEĞİZ. BU TXT DOSYASINDAN URL LERİ OKUYARAK BU
# LİNKLERE GİDECEĞİZ VE BİLGİLERİ ALIP VERİTABANINA KAYDEDECEĞİZ.

# YANİ KONSOL EKRANINDAN PY DOSYAMIZI ÇALIŞTIRDIĞIMIZ ZAMAN TXT DOSYASINDAN OKUMA YAPACAK VE KAYDEDECEK

# 1- SİTEDEN FİYAT VE BAŞLIĞIN ALINMASI
# 2- VERİLERİN VERİTABANINA KAYIT EDİLMESİ

# ÖRNEK OLARAK GŞRECEĞİN AMAZON SİTESİ
# https://www.amazon.co.uk/laptop/s?k=laptop

#######################

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from colorama import Fore, Style

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 "
                  "Safari/537.36"}


def get_data(url):
    # girilen url i soup olarak döndür
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def read_urls():
    # txt dosyasını oku
    with open('Files/urls.txt') as f:
        urls = f.readlines()
    return urls


def parse(urllist):
    # txt den gelenleri işle
    for dt in urllist:
        # her satırı 2 ye bölüp fiyat ve linki alma
        veri = dt.split("price:")
        if len(veri) >= 2:
            ul = veri[0]
            check_price = float(veri[1])
        else:
            ul = veri[0]
            check_price = 0

        # zamanı al
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")

        print("PRODUCT URL : ", ul)
        # linke get - parse
        soup = get_data(ul)

        # gerekli bilgileri al
        try:
            title = soup.find("span", attrs={"id": "productTitle"}).text.strip()
        except:
            title = None

        if soup.find("span", attrs={"id": "price_inside_buybox"}):
            price = float(soup.find("span", attrs={"id": "price_inside_buybox"}).text.strip().replace("£", ""))
        elif soup.find("div", attrs={"id": "buyNew_noncbb"}):
            price = float(soup.find("div", attrs={"id": "buyNew_noncbb"}).text.strip().replace("£", ""))
        elif soup.find("span", attrs={"id": "newBuyBoxPrice"}):
            price = float(soup.find("span", attrs={"id": "newBuyBoxPrice"}).text.strip().replace("£", ""))
        else:
            price = None

        # alınan bilgileri yazdır
        print("\n", "PRODUCT INFO : ", "\n", "title : ", title, "\n", "Price : ", price, "\n", "CHECK_PRICE : ",
              check_price, "\n", "Check Time : ", current_time, "\n")

        # fiyat kontrolü - eğer istediğin fiyattan aşağı düşerse kırmızı olarak yazdır
        if price is not None:
            if check_price > price:
                print(Fore.RED + "FİYAT DÜŞTÜ")
                print(Style.RESET_ALL)

        print("-----------------------------------------")


def main():
    # tüm işlemleri sırayla çalıştır
    url_list = read_urls()
    data = parse(url_list)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(5)
