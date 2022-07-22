
import sys 
import json 
import subprocess 

process = subprocess.run(["pip-tree", "--json", "--dump-root-only"], shell=True, text=True, stdout=subprocess.PIPE, check=True)
packageinfos = json.loads(process.stdout)

skippedpackageinfos = list()

for packageinfo in packageinfos:
  if "Home-page" in packageinfo:
    print("* {:s}: {:s}".format(packageinfo["Name"], packageinfo["Home-page"]))
  else:
    skippedpackageinfos.append(packageinfo) #error 

for packageinfo in skippedpackageinfos:
  print("Could not find 'Home-page' in {:s}. Please add its yourself.".format(packageinfo["Name"])) #error 
