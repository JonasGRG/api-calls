import urllib.request as request
import json 
import contextlib
import csv
import re 
import pandas as pd

# Function taken from exampels on https://cvrapi.dk/examples
# The function takes a cvr number and a country Aplha-2 code and return a json object 
def cvrapi(cvr, country):
  request_a = request.Request(
    url='http://cvrapi.dk/api?search=%d&country=%s' % (cvr, country),
    headers={'User-Agent': 'test projektt1'})

  with contextlib.closing(request.urlopen(request_a)) as response:
    return json.loads(response.read())


# This function loads a csv file into a list
def csv_to_list(path_to_file):
  with open(path_to_file, newline='') as f:
    reader = csv.reader(f)
    cvrs = list(reader)
    return cvrs

# This function takes a cvr and splits it into country code and cvr number
def split_cvrs(cvr):
  split = re.split('(\d+)',cvr[0])
  split = list(filter(None, split))
  country_code = split[0]
  cvr_number = split[1]
  return country_code, cvr_number 


# Load the data from the api for the list of cvr numbers
cvrs = csv_to_list('/Users/jonas/Documents/SecureSpectrum/api-calls/data/data_in/CVR_Datasæt.csv')
names = []
adresses = []
owners = []
for cvr in cvrs[1:]:
  country_code, cvr_number = split_cvrs(cvr)
  # Chech if it is a danish VAT number
  if country_code == "DK":
    data_json = cvrapi(int(cvr_number), str(country_code)) 
  # Check of the json object contains the keys.
  # Append the value if so and empty string if not
  if "name" in data_json:
    names.append(data_json["name"])
  else:
    names.append("") 
  if "adresss" in data_json:
    names.append(data_json["adresss"])
  else:
    names.append("")
  if "owner" in data_json:
    names.append(data_json["owner"])
  else:
    names.append("")

# Collect the data in a pandas dataframe
master_data = pd.DataFrame()
master_data.assign(Name=names)
master_data.assign(Adress=adresses)
master_data.assign(Owner=owners)

# add ID_index column
master_data.insert(0, 'ID_index', range(0, len(master_data)))

# save data frame as csv
master_data.to_csv('/Users/jonas/Documents/SecureSpectrum/api-calls/data/data_out/master_data.txt', index=False)


