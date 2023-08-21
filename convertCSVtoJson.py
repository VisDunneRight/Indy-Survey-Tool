import csv
import json
import argparse

# Modify these for easier running
# The includeProp lets the parse know which data values and their types to process
# These are the required field.
includeProp = {
  "Name":"String",
  "Authors": "MultiSelect",
  "Bibtex": "String",
  "DOI": "String",
  "Year": "Timeline",
  # These are additional fields
  # The ones below are from the demo file and should be replaced when using your
  # own data.
  "Paper Type": "MultiSelect",
  "Type of Visualization shown": "MultiSelect",
  "Use of Color": "MultiSelect",
}
# System already assumes these exist therefore no need to have filter or view of them
excludeProp = ["Name", "Authors", "Year", "DOI", "Bibtex"]



def get_arguments():
    """ Get parsed CLI arguments """
    parser = argparse.ArgumentParser(description='Python script for converting csv to JSON for Indy.'
                                                 'Generates a config and data file.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input-file', type=str, default="Survey-Info.csv",
                        dest="filename", help='The files that gets parsered.')
    parser.add_argument('-d','--only-data', action='store_true', default=False,
                        dest="onlydata", help='generate only the data file')
  
    return parser.parse_args()


def main():
  args = get_arguments()
  with open(args.filename, encoding='utf-8-sig') as csvfile:
    spamreader = csv.reader(csvfile)
    jsonfile = {"meta":[], "data":[]}
    configfile = {"filterBy":[], "detailView":{
        "view" : "normal",
        "show":[] #Add properties that you want to view on summary view
      }, 
      "summaryView": {
        "view": "text",
        "showImg": True,
        "show":[] #Add properties that you want to view on summary view
      },
      "topView":{
        "title":"Example Survey",
        "description":"An example survey setup. Replace text in survey-config.json",
        "authors":"Provided by Data Visualization @ Khoury",
        "addEntry": {
          "description":["If you are an author of a peer-reviewed published work on example surveys that presents a contribution missing in our browser, please feel free to submit an entry. Filling out the form below will create a json entry that can be added as an issue to the github together with a 200x200px PNG thumbail.",
                        "The URL provided in the form should point to a DOI. Also, please acknowledge the fact that by submitting an entry, you provide us with permissions to use your image on this resource and in related publications."],
          "github":"https://github.com/VisDunneRight/indy-survey-tool/issues"
        }
      }
    }
    header = []
    # Get header information
    for row in spamreader:
      for name in row:
        header.append(name)
        if name in includeProp:
          jsonfile["meta"].append({'name': name, "type":includeProp[name]})
          if (includeProp[name] == 'MultiSelect' or includeProp[name] == 'String') and name not in excludeProp :
            configfile["filterBy"].append(name)
          if name not in excludeProp:
            configfile["detailView"]["show"].append(name)
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
    
    dataObject = json.dumps(jsonfile, indent=4)
    # Writing to survey-data.json
    with open("survey-data.json", "w") as outfile:
        outfile.write(dataObject)
    
    if args.onlydata == False:
      for i in range(len(configfile["filterBy"])):
        name = configfile["filterBy"][i]
        propStructure[name]['values'] = list(propStructure[name]['values'] )
        configfile["filterBy"][i] = propStructure[name]

      with open("survey-config.json", "w") as outfile:
          configObject= json.dumps(configfile, indent=4)
          outfile.write(configObject)

if __name__ == '__main__':
  main()