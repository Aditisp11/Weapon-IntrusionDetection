from simple_image_download import simple_image_download

# Correctly reference the `Downloader` class if it exists
response = simple_image_download.Downloader()

keywords = ["guns", "knife", "shotgun"]

for keyword in keywords:
    response.download(keyword, 200)  # Downloads 200 images for each keyword
