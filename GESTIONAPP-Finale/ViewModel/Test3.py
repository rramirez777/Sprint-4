import requests
def run():
    url = "https://picsum.photos/id/237/300/300"
    resp = requests.get(url)

    print("Status:", resp.status_code)
    print("Headers:", resp.headers)
    print("Content length:", len(resp.content))\
    
if __name__ == "__main__":
    a = run()
    
