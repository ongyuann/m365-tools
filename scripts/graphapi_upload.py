import requests

# note: drive_id and folder_id are custom to the user, find em yourself (hint: graph api :D)
drive_id = "b!<...snipped...>"
folder_id = "<snip>"

full_filepath = "/path/to/file/you/want/to/upload/such/as/psexec.exe"
file_name = "psexec.exe"
content_type = "application/binary"

# note: m365 access token is valid for 60 minutes only
jwt = "eyJ0eXA<..snipped..MS access token..>"

contents = open(full_filepath, 'rb').read()

def upload():
	burp0_url = f"https://graph.microsoft.com:443/v1.0/drives/{drive_id}/items/{folder_id}:/{file_name}:/content"
	burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Content-Type": f"{content_type}", "Authorization": f"Bearer {jwt}", "Client-Request-Id": "cd15e961-7e11-ce39-40e8-59be1955c4fd", "Sdkversion": "graph-js/2.2.1 (featureUsage=6)", "Origin": "https://www.office.com.mcas.ms", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Te": "trailers"}
	burp0_data = contents
	r = requests.put(burp0_url, headers=burp0_headers, data=burp0_data)
	print(r.text)

upload()
