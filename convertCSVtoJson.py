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
  "Opportunity": "MultiSelect",
  "Contribution Type": "MultiSelect",
  "Data Domain": "MultiSelect",
  "Dataset Types": "MultiSelect",
  "Dataset Generation": "MultiSelect",
  "Presentation": "MultiSelect",
  "Device": "MultiSelect",
  "Input": "MultiSelect",
  "Environment": "MultiSelect",
  "Space": "MultiSelect",
  "Embodiment": "MultiSelect",
  "Collaboration ": "MultiSelect",
  "Interaction": "MultiSelect",
  "Visualization": "MultiSelect",
  "Abstract/Natural": "MultiSelect",
  "Manipulate": "MultiSelect",
  "Position": "MultiSelect",
  "Scale": "MultiSelect",
  "2D or 3D": "MultiSelect"
}

with open(filename, encoding='utf-8-sig') as csvfile:
  spamreader = csv.reader(csvfile)
  jsonfile = {"meta":[], "filterBy":[], "detailView":[], "summaryView":[], "data":[]}
  header = []
  # Get header information
  for row in spamreader:
    for name in row:
      header.append(name)
      if name in includeProp:
        jsonfile["meta"].append({'name': name, "type":includeProp[name]})
        jsonfile["filterBy"].append(name)
        jsonfile["detailView"].append(name)
    break

  propStructure = {}
  for prop in jsonfile["filterBy"]:
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

  for i in range(len(jsonfile["filterBy"])):
    name = jsonfile["filterBy"][i]
    propStructure[name]['values'] = list(propStructure[name]['values'] )
    jsonfile["filterBy"][i] = propStructure[name]
  
  json_object = json.dumps(jsonfile, indent=4)
  # Writing to sample.json
  with open("survey-data.json", "w") as outfile:
      outfile.write(json_object)

