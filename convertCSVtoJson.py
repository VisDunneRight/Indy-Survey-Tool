import csv
import json

# Modify these for easier running
filename = 'Survey-Info.csv'
# The includeProp lets the parse know which data values and their types to process
# These are the required field.
includeProp = {
  "Name":"String",
  "Authors": "MultiSelect",
  "Bibtex": "String",
  "DOI": "String",
  "Year": "Timeline",
  # These are additional fields
  "Paper Type": "MultiSelect",
  "Type of Visualization shown": "MultiSelect",
  "Use of Color": "MultiSelect",
}

with open(filename, encoding='utf-8-sig') as csvfile:
  spamreader = csv.reader(csvfile)
  jsonfile = {"meta":[], "data":[]}
  header = []
  # Get header information
  for row in spamreader:
    for name in row:
      header.append(name)
      if name in includeProp:
        jsonfile["meta"].append({'name': name, "type":includeProp[name]})
    break

  propStructure = {}
  for prop in includeProp:
    propStructure[prop] = {"name":prop, "values":set()}

  for row in spamreader:
    entry = {}
    for index, prop in enumerate(row):
      if header[index] in includeProp:
        if includeProp[header[index]] == "MultiSelect":
          entry[header[index]] = [x.strip() for x in prop.split(",")] 
        else:
          entry[header[index]] = prop.strip()
        if includeProp[header[index]] == "MultiSelect":
          propList = [x.strip() for x in prop.split(",")] 
          for doc in propList:
            propStructure[header[index]]['values'].add(doc)
    jsonfile["data"].append(entry)
  
  json_object = json.dumps(jsonfile, indent=4)
  # Writing to sample.json
  with open("survey-data.json", "w") as outfile:
      outfile.write(json_object)

