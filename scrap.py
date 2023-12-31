import requests, csv, time
from bs4 import BeautifulSoup

username        = "yulandikasp@gmail.com" 
password        = "123456" 
login_url       = "https://sipmen.bps.go.id/st2023/login" 
scrap_page      = "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/index-generate-box-kab" 
post_endpoint   = "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/insert_surat" 
session         = requests.session()

def read_data():
    data = []
    data_source = "sipmen.csv"
    with open(data_source) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            data.append({"kode":row[0], "petugas":row[1]})
    
    return data

def send_data():
    data = read_data()
    success_count = 0
    data_size = len(data)

    with session as s: 
        req = s.get(login_url).text 
        html = BeautifulSoup(req,"html.parser") 
        _csrf = html.find("input", {"name": "_csrf"}).attrs["value"] 

        payload = { 
            "_csrf": _csrf, 
            "username": username, 
            "password": password
        } 
        
        s.post(login_url, data=payload)

        r = s.get(scrap_page)
        soup = BeautifulSoup (r.content, "html.parser") 
        csrf = soup.find('meta', {"name": "csrf-token"}).attrs['content']

        print("Mengirim " + str(data_size) + " data....")
        print("")
        for row in data:
            success_count+=send(row, csrf)
            print("--------------------------------------------")
        # for row in data:
        #     i+=1
        #     print(row['kode'])
            
        #     send_data = s.post(post_endpoint, data = {'no_box_besar':row['kode'], 'petugas':row['petugas']}, headers={'X-Requested-With': 'XMLHttpRequest', 'X-Csrf-Token':csrf})
        print("================================================")
            
        print("Data dikirim : "+str(data_size))
        print("Sukses : "+str(success_count))
        print("Gagal : "+str(data_size-success_count))

def send(row, csrf):
        
    with session.post(post_endpoint, data = {'no_box_besar':row['kode'], 'petugas':row['petugas']}, headers={'X-Requested-With': 'XMLHttpRequest', 'X-Csrf-Token':csrf}) as resp:
        print("Uploading : {0:s}--{1:s}".format(row['kode'], row['petugas']))
        
        if("berhasil" in str(resp.content)):
            print(" Status : Ok")
            return 1
        else:
            print(" Status : Gagal")
            return 0
        

start_time = time.time()
send_data()
duration = time.time() - start_time
print(f"Proses berjalan : {duration} detik")