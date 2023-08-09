import requests, csv 
from bs4 import BeautifulSoup 
 
username = "yulandikasp@gmail.com" 
password = "123456" 
login_url = "https://sipmen.bps.go.id/st2023/login" 
scrap_page = "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/index-generate-box-kab" 
post_endpoint = "https://sipmen.bps.go.id/st2023/sipmen-terima-kab-pengolahan/insert_surat" 

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
    csrf=""
    failed_count = 0
    i=0
    data_size = len(data)

    with requests.session() as s: 
        req = s.get(login_url).text 
        html = BeautifulSoup(req,"html.parser") 
        _csrf = html.find("input", {"name": "_csrf"}).attrs["value"] 

        payload = { 
            "_csrf": _csrf, 
            "username": username, 
            "password": password
        } 
        res = s.post(login_url, data=payload)

        r = s.get(scrap_page)
        soup = BeautifulSoup (r.content, "html.parser") 
        csrf = soup.find('meta', {"name": "csrf-token"}).attrs['content'] 
        print("Mengirim " + str(data_size)+ " data....")
        print("")
        for row in data:
            i+=1
            # print(row['kode'])
            print("{0} Uploading : {1:s}--{2:s}".format(i, row['kode'], row['petugas']))
            send_data = s.post(post_endpoint, data = {'no_box_besar':row['kode'], 'petugas':row['petugas']}, headers={'X-Requested-With': 'XMLHttpRequest', 'X-Csrf-Token':csrf})

            if("berhasil" in str(send_data.content)):
                print("Status : Sukses")
            else:
                print("Status : Gagal")
                failed_count+=1
            
            print("================================================")
            
        print("Data dikirim : "+str(data_size))
        print("Sukses : "+str(data_size-failed_count))
        print("Gagal : "+str(failed_count))

   
send_data()



