import requests, csv, time
import concurrent.futures
import threading
from bs4 import BeautifulSoup

thread_local = threading.local()

username        = "yulandikasp@gmail.com" 
password        = "123456" 
login_url       = "https://sipmen.bps.go.id/st2023/login" 
scrap_page      = "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/index-generate-box-kab" 
post_endpoint   = "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/insert_surat" 

def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

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
    failed_count = 0
    data_size = len(data)
    session = get_session()

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
        thread_local.csrf = soup.find('meta', {"name": "csrf-token"}).attrs['content']

        print("Mengirim " + str(data_size) + " data....")
        print("")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(send, data)

        # for row in data:
        #     i+=1
        #     print(row['kode'])
            
        #     send_data = s.post(post_endpoint, data = {'no_box_besar':row['kode'], 'petugas':row['petugas']}, headers={'X-Requested-With': 'XMLHttpRequest', 'X-Csrf-Token':csrf})

        #     if("berhasil" in str(send_data.content)):
        #         print("Status : Sukses")
        #     else:
        #         print("Status : Gagal")
        #         failed_count+=1
            
        #     print("================================================")
            
        # print("Data dikirim : "+str(data_size))
        # print("Sukses : "+str(data_size-failed_count))
        # print("Gagal : "+str(failed_count))

def send(row):
    session = get_session()
    with session.post(post_endpoint, data = {'no_box_besar':row['kode'], 'petugas':row['petugas']}, headers={'X-Requested-With': 'XMLHttpRequest', 'X-Csrf-Token':thread_local.csrf}) as resp:
        print(" Uploading : {1:s}--{2:s}".format(row['kode'], row['petugas']))
    
        return resp.content

start_time = time.time()
send_data()
duration = time.time() - start_time
print(f"Proses berjalan : {duration} detik")