import requests, csv 
from bs4 import BeautifulSoup 
 
username = "yulandikasp@gmail.com" 
password = "123456" 
login_url = "https://sipmen.bps.go.id/st2023/login" 
scrap_page = "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/tambah-generate-box-kab" 
post_endpoint = "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/insert_surat" 

def read_data():
    data = []
    data_source = "sipmen.csv"
    with open(data_source) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            data.append({"kode":row[0], "petugas":row[1]})
    
    return data

def read_csrf():
    with requests.session() as s: 
        req = s.get(login_url).text 
        html = BeautifulSoup(req,"html.parser") 
        _csrf = html.find("input", {"name": "_csrf"}).attrs["value"] 

        payload = { 
            "_csrf": _csrf, 
            "username": username, 
            "password": password
        } 
        res =s.post(login_url, data=payload) 
    
        r = s.get(scrap_page) 
        soup = BeautifulSoup (r.content, "html.parser") 

    
    return soup.find('meta', {"name": "csrf-token"}).attrs['content']

# print(table)
print(read_csrf())
print(read_data())



