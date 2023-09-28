import requests
import os
import time

# Github Repo Info
repoOwner = 'yanglinfang'
repoName = 'npo_tech_wildlife_camera'
folderPath = 'testimage'

# GitHub API endpoint to list contents of the folder
apiUrl = f'https://api.github.com/repos/{repoOwner}/{repoName}/contents/{folderPath}'

# Retry times when failed to download image
maxRetry = 10

# Send HTTP GET request
response = requests.get(apiUrl)

#Check if request was successful(status code 200)
if response.status_code == 200:
    # print('Successfully get folder')

    # Turn the folder into a file 
    folderContents = response.json()

    # Create a dir to save downloaded images
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    # Loop through contents of folder
    for item in folderContents:
        if item['type'] == 'file':
            fileName = item['name']
            downloadUrl = item['download_url']

            for retry in range(maxRetry):
                try:
                    # Send an HTTP GET request to download the image
                    imageResponse = requests.get(downloadUrl, timeout=10)

                    if imageResponse.status_code == 200:
                        print(f'Load image {fileName} successfull')
                        break

                except requests.exceptions.RequestException as e:
                    time.sleep(1)
            else:
                print(f'Failed to downloadimage {fileName} after {maxRetry} retries')
            
            """ this code is for if want to download images to local"""
            # for retry in range(maxRetry):
            #     try:
            #         # Send an HTTP GET request to download the image
            #         imageResponse = requests.get(downloadUrl, timeout=10)

            #         if imageResponse.status_code == 200:
            #             with open(os.path.join(folderPath, fileName), 'wb') as f:
            #                 f.write(imageResponse.content)
            #             print(f'Successfully downloaded: {fileName}')
            #             break
            #     except (requests.ConnectionError, requests.Timeout):
            #         print(f'Retry #{retry + 1} failed to fetch image {fileName}. Retrying...')
            #         time.sleep(1)  # Wait for a moment before retrying
            # else:
            #     print(f'Failed to downloadimage {fileName} after {maxRetry} retries')
else:
    print(f'Failed to fetch folder: Status Code {response.status_code}')