import requests

country = input("Enter a country: ")
year = input("Enter a year: ")

# Build the API request URL
url = f"https://news.google.com/search?q={country}&tbs=cdr:1,cd_min:{year},cd_max:{year}&tbm=nws&hl=en-US&gl=US&ceid=US:en"

# Make the API request
response = requests.get(url)

# Parse the HTML response
html = response.text

# Find the first headline
start_index = html.find("<a class=\"DY5T1d\"")
end_index = html.find("</a>", start_index)
headline = html[start_index:end_index]

# Print the headline
print(headline)