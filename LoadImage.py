import requests
import os
import time
import matplotlib.pyplot as plt

# Github Repo Info
repoOwner = 'yanglinfang'
repoName = 'npo_tech_wildlife_camera'
folderPath = 'dataset'

# GitHub API endpoint to list contents of the folder
apiUrl = f'https://api.github.com/repos/{repoOwner}/{repoName}/contents/{folderPath}'

# Retry times when failed to download image
maxRetry = 10

# Dictionary to store image count inside each folder
folderCounts = {}

def load_image_from_folder(apiUrl, maxRetry = 10):
    # Send HTTP GET request
    response = requests.get(apiUrl)

    #Check if request was successful(status code 200)
    if response.status_code == 200:

        # Turn the folder into a file 
        folderContents = response.json()

        # Loop through contents of folder
        for item in folderContents:
            if item['type'] == 'dir':
                subFolderUrl = item['url']
                # folderName = item['name']
                # folderCounts[folderName] = 0
                load_image_from_folder(subFolderUrl, maxRetry)
            elif item['type'] == 'file':
                folderName = os.path.basename(os.path.dirname(item['path']))
                folderCounts[folderName] = folderCounts.get(folderName, 0) + 1

                # fileName = item['name']
                # downloadUrl = item['download_url']

                # for retry in range(maxRetry):
                #     try:
                #         # Send an HTTP GET request to download the image
                #         imageResponse = requests.get(downloadUrl, timeout=10)

                #         if imageResponse.status_code == 200:
                #             # readImage = imageResponse.content
                #             print(f'Load image {fileName} successfull')
                #             break

                #     except requests.exceptions.RequestException as e:
                #         time.sleep(1)
                # else:
                #     print(f'Failed to downloadimage {fileName} after {maxRetry} retries')
    else:
        print(f'Failed to fetch folder: Status Code {response.status_code}')

load_image_from_folder(apiUrl, maxRetry)
print(folderCounts)

folderName = list(folderCounts.keys())
imageCount = list(folderCounts.values())

