import time
from astroquery.simbad import Simbad
import re

def online_alias_search(queue):
    associations = [] 
    bad_names = []
    #DONT RUN THIS LOOP UNLESS YOU ABSOLUTLY NEED TO !!!! 
    print("---- STARTING QUERY ----")
    for i, name in enumerate(queue):
        result_table = Simbad.query_objectids(name)
        if(result_table):
            #take all results as an associated set of names of a single object
            association = [str(x[0]) for x in result_table]  
            #remove all text between brackets (i.e. "[REMOVE This]") and remove the tag "NAME"
            association = [re.sub(r'\[.*?\]|NAME', '', word) for word in association]
            #remove names that have characters which are associated with names too long to be useful    
            #... associated with names like '3HWC J0534+220' and 'LBN 184.62-05.65'
            chars_to_exclude = ['+','.'] 
            association = [word for word in association if all(char not in word for char in chars_to_exclude)]
            #remove all excess spaces from the name ("M   31" becomes "M 31")
            association = [' '.join(string.split()) for string in association]
            #remove all names that are simply 'digits', those names are not usefull 
            association = [word for word in association if not word.isdigit()]
            #remove all names that start with 'M ', those names are captured elsewhere...
            association = [word for word in association if not word.startswith('M ')]
            #add the association of names to the associations list
            associations.append({"searched": name, "found_associations":association})
        else:
            bad_names.append(name)
            
        #Rest the search so we don't get black listsed from SIMBAD    
        if i % 3 == 0:
            time.sleep(3)
        else:
            time.sleep(1)
            
        #TRACKING PRINT   
        if i % 250 == 0:
            print(f'... {i+1} queries completed...')
            
    print("---- QUERY END ----")
    return({"queue":queue, "associations":associations,"bad_names":bad_names})