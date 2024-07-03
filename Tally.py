from clr_loader import get_coreclr
import pythonnet  # to use dll in python
import sys  # to add dll directory to path
path = r"./net6"
sys.path.append(path)
rt = get_coreclr("TallyConnector.json") #Json we created earlier
pythonnet.set_runtime(rt)
pythonnet.load()

import clr
clr.AddReference("TallyConnector") # Load Assembly
from TallyConnector import Tally
tally = Tally() #Intiating Tally class
#tally = TallyConnector.Tally("http://localhost",9000) #Intiating Tally class with url and Port
tally.Setup("http://localhost",9000) #changing url after initiating class
IsTallyRunning = tally.Check().Result #Check Tally is running on given url and port
#returns true if Tally is running
companyName = tally.GetActiveTallyCompany().Result
print(f'Active Company in Tally - {companyName}')
companies = tally.GetCompaniesList().Result
company:Company
for company in companies:
    print(f'Name - {company.Name:<20} Starting From - {company.StartingFrom} Country - { company.Country}')

    if IsTallyRunning:
        print(f'Active Company in Tally - {companyName}')

        tally.FetchAllTallyData().Wait()

        # Groups = tally.GetMasters(TallyObjectType.Groups)
        mastertype: MastersMapping
        for mastertype in MastersMapping.MastersMappings:
            Masters: List[BasicTallyObject] = tally.GetMasters(mastertype.MasterType)
            # Masters contains list of basicTallyObject that has properties GUID,TallyId
            t = f'{mastertype.MasterType.ToString():<15} in Company'
            # Printing Number of masters by type
            print(f'Number of  {t:<25} - {companyName:<10} = {Masters.Count}')
if IsTallyRunning:
   companyName = tally.GetActiveTallyCompany().Result
   print(f'Active Company in Tally - {companyName}')

   companies = tally.GetCompaniesList().Result
   company:Company

   for company in companies:
       print(f'Name - {company.Name:<20} Starting From - {company.StartingFrom} Country - { company.Country}')
       companyName = company.Name
       tally.ChangeCompany(company.Name)
       tally.FetchAllTallyData().Wait()
       mastertype:MastersMapping
       for mastertype in MastersMapping.MastersMappings:
           Masters:List[BasicTallyObject] = tally.GetMasters(mastertype.MasterType)
           #Masters contains list of basicTallyObject that has properties GUID,TallyId
           t = f'{mastertype.MasterType.ToString():<15} in Company'
           #Printing Number of masters by type
           print(f'Number of  {t:<25} - {companyName:<10} = {Masters.Count}')