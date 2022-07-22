
import sys 
import json 
import subprocess 

process = subprocess.run(["pip-tree", "--json"], shell=True, text=True, stdout=subprocess.PIPE, check=True)
packageinfos = json.loads(process.stdout)

skippedpackageinfos = list()

for packageinfo in packageinfos:
  if packageinfo.get("License", "UNKNOWN") != "UNKNOWN":
    print("* {:s}: [{:s}](./LICENSE_THIRD_PARTY)".format(packageinfo["Name"], packageinfo["License"]))
  else:
    skippedpackageinfos.append(packageinfo) #error 

for packageinfo in skippedpackageinfos:
  print("Could not find 'License' in {:s}. Please add its yourself.".format(packageinfo["Name"])) #error 
