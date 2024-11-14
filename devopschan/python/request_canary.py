import requests
import re

def request_and_check(url, num_requests=1000):
    version_1_count = 0 
    version_2_count = 0 

    for _ in range(num_requests):
        response = requests.get(url)
    
        h1_tags = re.findall(r'(<h1[^>]*>.*?</h1>)', response.text, re.DOTALL)
            
        for h1 in h1_tags:
            if 'Version 1' in h1: 
                version_1_count += 1
            elif 'Version 2' in h1: 
                version_2_count += 1

    return version_1_count, version_2_count


# 실제 URL로 변경합니다.
url = 'http://localhost:8092'  
version_1, version_2 = request_and_check(url)

print(f"Version 1 : {version_1}")
print(f"Version 2: {version_2}")