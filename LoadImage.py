import requests
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cv2

# Github Repo Info
repoOwner = 'yanglinfang'
repoName = 'npo_tech_wildlife_camera'
folderPath = 'dataset'

# GitHub API endpoint to list contents of the folder
apiUrl = f'https://api.github.com/repos/{repoOwner}/{repoName}/contents/{folderPath}'

# OAuth Token used for more data limit
headers = {
    'Authorization': 'token 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'
}

rate_limit_url = 'https://api.github.com/rate_limit'
response = requests.get(rate_limit_url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON to get rate limit information
    rate_limit_data = response.json()
    print("Rate Limit Data:")
    print(rate_limit_data)
else:
    print(f"Failed to check rate limit: Status Code {response.status_code}")

# Retry times when failed to download image
# maxRetry = 10

# # Dictionary to store image count inside each folder
# folderCounts = {}

# def load_image_from_folder(apiUrl, maxRetry = 10):
#     # Send HTTP GET request
#     response = requests.get(apiUrl, headers=headers)

#     #Check if request was successful(status code 200)
#     if response.status_code == 200:

#         # Turn the folder into a file 
#         folderContents = response.json()

#         # Loop through contents of folder
#         for item in folderContents:
#             if item['type'] == 'dir':
#                 subFolderUrl = item['url']
#                 load_image_from_folder(subFolderUrl, maxRetry)
#             elif item['type'] == 'file':
#                 folderName = os.path.basename(os.path.dirname(item['path']))
#                 folderCounts[folderName] = folderCounts.get(folderName, 0) + 1

#                 fileName = item['name']
#                 imageUrl = item['download_url']

#                 for retry in range(maxRetry):
#                     try:
#                         # Send an HTTP GET request to download the image
#                         imageResponse = requests.get(imageUrl, timeout=10)

#                         if imageResponse.status_code == 200:
#                             analyze_image_brightness(imageResponse.content)
#                             break

#                     except requests.exceptions.RequestException as e:
#                         time.sleep(1)
#                 else:
#                     print(f'Failed to downloadimage {fileName} after {maxRetry} retries')
#     else:
#         print(f'Failed to fetch folder: Status Code {response.status_code}')

# # Function to analyze image brightness
# def analyze_image_brightness(content):
#     # Decode image from bytes to an OpenCV image
#     imageNp = np.frombuffer(content, dtype = np.uint8)
#     image = cv2.imdecode(imageNp, cv2.IMREAD_COLOR)

#     # Convert image to grayscale
#     grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Calculate average brightness (mean pixel value)
#     brightness = np.mean(grayImg)

#     print(f'Image brightness is: {brightness}')

# load_image_from_folder(apiUrl, maxRetry)
# print(folderCounts)

# folderName = list(folderCounts.keys())
# imageCount = list(folderCounts.values())

