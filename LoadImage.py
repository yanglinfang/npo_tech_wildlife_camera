import requests
import os
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime
import cv2
import authInfo
import psycopg2 as ps

# Github Repository Information
repoOwner = 'yanglinfang'
repoName = 'npo_tech_wildlife_camera'
folderPath = 'dataset'
myToken = authInfo.token

# GitHub API endpoint to list contents of the folder
apiUrl = f'https://api.github.com/repos/{repoOwner}/{repoName}/contents/{folderPath}'

# OAuth Token used for more data limit
headers = {
    'Authorization': f'token {myToken}'
}

# # Database information
# dbName = authInfo.dbName
# dbUser = authInfo.dbUser
# dbPassWord = authInfo.dbPassWord
# dbHost = authInfo.dbHost
# dbPort = authInfo.dbPort

# try:
#     conn = ps.connect(
#         dbname = dbName,
#         user = dbUser,
#         password = dbPassWord,
#         host = dbHost,
#         port = dbPort
#     )

#     cursor = conn.cursor()

#     # Define the table schema
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS ImageData (
#         id SERIAL PRIMARY KEY,
#         image_name VARCHAR(255),
#         image_path VARCHAR(255),
#         ave_brightness FLOAT,
#         red_val FLOAT,
#         green_val FLOAT,
#         blue_val FLOAT
#     );
#     '''

#     cursor.execute(create_table_query)

#     conn.commit()

#     # Sample data (replace with actual data)
#     image_name = 'image1.jpg'
#     image_path = '/path/to/image1.jpg'
#     ave_brightness = 0.5
#     red_val = 0.2
#     green_val = 0.8
#     blue_val = 0.4

#     # SQL INSERT statement
#     insert_query = '''
#     INSERT INTO ImageData (image_name, image_path, ave_brightness, red_val, green_val, blue_val)
#     VALUES (%s, %s, %s, %s, %s, %s);
#     '''

#     # Execute the INSERT query with data
#     cursor.execute(insert_query, (image_name, image_path, ave_brightness, red_val, green_val, blue_val))

#     # Commit the changes to the database
#     conn.commit()

#     # Close the cursor and connection
#     cursor.close()
#     conn.close()

# except Exception as e:
#     print("Error:", e)

# # Retry times when failed to download image
# maxRetry = 10

# # Dictionary to store image count inside each folder
# folderCounts = {}

# # List to store values for all images
# brightnessVal = []
# redVal = []
# greenVal = []
# blueVal = []

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
#                 # store directory path into dictionary, count how many images under same directory name
#                 folderName = os.path.basename(os.path.dirname(item['path']))
#                 folderCounts[folderName] = folderCounts.get(folderName, 0) + 1
                
#                 fileName = item['name']
#                 imageUrl = item['download_url']
                
#                 for retry in range(maxRetry):
#                     try:
#                         # Send an HTTP GET request to download the image
#                         imageResponse = requests.get(imageUrl, timeout=10)

#                         if imageResponse.status_code == 200:
#                             image_analyze(imageResponse.content)
#                             break

#                     except requests.exceptions.RequestException as e:
#                         time.sleep(1)
#                 else:
#                     print(f'Failed to downloadimage {fileName} after {maxRetry} retries')
#     else:
#         print(f'Failed to fetch folder: Status Code {response.status_code}')

# # Function to call all analyzation of an image
# def image_analyze(content):
#     average_brightness_curve(content)
#     RGB_Distribution(content)

# # Function to analyze image brightness
# def average_brightness_curve(content):
#     # Decode image from bytes to an OpenCV image
#     imageNp = np.frombuffer(content, dtype = np.uint8)
#     image = cv2.imdecode(imageNp, cv2.IMREAD_COLOR)

#     # Convert image to grayscale
#     grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Calculate average brightness (mean pixel value)
#     brightness = np.mean(grayImg)

#     # Append brightness values into the list
#     brightnessVal.append(brightness)

# def RGB_Distribution(content):
#     # Decode image from bytes to an OpenCV image
#     imageNp = np.frombuffer(content, dtype = np.uint8)
#     image = cv2.imdecode(imageNp, cv2.IMREAD_COLOR)

#     # Convert image to grayscale
#     blueChannel, greenChannel, redChannel = cv2.split(image)

#     # Calculate average brightness (mean pixel value)
#     avgBlue = np.mean(blueChannel)
#     avgGreen = np.mean(greenChannel)
#     avgRed = np.mean(redChannel)

#     # Append brightness values into the list
#     blueVal.append(avgBlue)
#     greenVal.append(avgGreen)
#     redVal.append(avgRed)

# load_image_from_folder(apiUrl, maxRetry)

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