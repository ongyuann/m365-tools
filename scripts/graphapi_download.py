import requests
import json
import sys

# note: m365 access token is valid for 60 minutes only
jwt = "eyJ0eXA<..snipped..MS access token..>"

def get_drive_id():
	burp0_url = "https://graph.microsoft.com:443/v1.0/me/drive"
	burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Authorization": f"Bearer {jwt}", "Client-Request-Id": "83b22853-5826-f69d-dee5-8f75cc5d6bc6", "Sdkversion": "graph-js/2.2.1 (featureUsage=6)", "Origin": "https://www.office.com.mcas.ms", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Te": "trailers"}
	r = requests.get(burp0_url, headers=burp0_headers)
	raw = r.text
	raw_json = json.loads(raw)
	if "id" in raw_json:
		drive_id = (raw_json["id"])
		print("[+] drive_id = %s" % drive_id)
		return drive_id
	else:
		print("[+] error retrieving drive id. check jwt validity. exiting!")
		sys.exit()

def get_drive_folder_ids():
	burp0_url = f"https://graph.microsoft.com:443/v1.0/drives/{drive_id}/items/root/children"
	burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Authorization": f"Bearer {jwt}", "Client-Request-Id": "83b22853-5826-f69d-dee5-8f75cc5d6bc6", "Sdkversion": "graph-js/2.2.1 (featureUsage=6)", "Origin": "https://www.office.com.mcas.ms", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Te": "trailers"}
	r = requests.get(burp0_url, headers=burp0_headers)
	raw = r.text
	raw_json = json.loads(raw)
	folder_ids_one_level = []
	for ele in raw_json["value"]:
		print("======")
		if "@microsoft.graph.downloadUrl" in ele:
			print("[+] downloadable file: %s" % ele["name"])
			print("[+] downloadUrl: %s" % ele["@microsoft.graph.downloadUrl"])
		else:
			print("[+] folder name: %s" % ele["name"])
			print("[+] id: %s" % ele["id"])
			print("[+] webUrl: %s" % ele["webUrl"])
			folder_ids_one_level.append("%s-%s" % (ele["id"],ele["name"]))
	return folder_ids_one_level

def get_drive_folder_ids_one_level(folder_id):
	folder_id,folder_name = folder_id.split("-")
	burp0_url = f"https://graph.microsoft.com:443/v1.0/drives/{drive_id}/items/{folder_id}/children"
	burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Authorization": f"Bearer {jwt}", "Client-Request-Id": "83b22853-5826-f69d-dee5-8f75cc5d6bc6", "Sdkversion": "graph-js/2.2.1 (featureUsage=6)", "Origin": "https://www.office.com.mcas.ms", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Te": "trailers"}
	r = requests.get(burp0_url, headers=burp0_headers)
	raw = r.text
	raw_json = json.loads(raw)
	folder_ids_one_level = []
	for ele in raw_json["value"]:
		print("======")
		if "@microsoft.graph.downloadUrl" in ele:
			print("[+] downloadable file in folder id-name %s-%s: %s" % (folder_id,folder_name,ele["name"]))
			print("[+] downloadUrl: %s" % ele["@microsoft.graph.downloadUrl"])
		else:
			print("[+] sub-folder name in folder id-name %s-%s: %s" % (folder_id,folder_name,ele["name"]))
			print("[+] id: %s" % ele["id"])
			print("[+] webUrl: %s" % ele["webUrl"])
			folder_ids_one_level.append(ele["id"])
	return folder_ids_one_level

drive_id = get_drive_id()
folder_ids_one_level = get_drive_folder_ids()
for folder_id in folder_ids_one_level:
	print("======>")
	print(f"[*] looking into drive id {drive_id}, folder id-name {folder_id}")
	get_drive_folder_ids_one_level(folder_id)
