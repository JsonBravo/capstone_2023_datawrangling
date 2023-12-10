import re
import string
import json

#This can be passed to the SOAM so there is control over what type of cleaning we do...
def provided_cleaning_method(s):
    #standardize on lower case
    s = s.lower()
    #put a space between each alpha and numeric ("abc123" becomes "abc 123")
    s = re.sub(r'([a-z])(\d)', r'\1 \2', s)
    #put a space between each numeric and alpha ("123abc" becomes "123 abc")
    s = re.sub(r'(\d)([a-z])', r'\1 \2', s)
    #replace all punctuation with a space (' '), except for the apostraphe "'"
    s = re.sub(r'[^\w\s\']|_', ' ', s)
    #trim all leading and trailing white space
    s = s.strip()
    #replace double spaces with single space
    s = re.sub(r'\s+', ' ', s)
    
    return(str(s))

#DEFAULT PRIORITIES AND COMMON NAMES (for name standardization logic)
provided_tag_priorities = ["m ", "ngc ", "ic "]
provided_common_name_tags = ["galaxy", "nebula", "cluster", "comet"]

class Soam:
    """
    The SOAM class is a "Space Object Alias Map". 
    It assumes each association that shares at least one name is a unique object.
    Once instantiated...
    Pass in a list of associations using the 'add_associations' method 
        -- associations being a sub list of related names: 
            [['m31','andromeda galaxy'],['b33','horse head nebula']]
        -- if 'cleaning method = False' 
            then it expects all associations to be pre-cleaned 
                (remove unwanted punct. and the like)
            otherwise it will clean all inputs according to the passed method...
    Builds three dicts (all standardized according to the cleaning method):
        -- The names dict will contain the names of all included objects in the SOAM and will
            be structured something like the following, where the key is the name and the value
            is an int which will refer to an index number in the alias dict.
        -- The alias dict will contain index keys and value pairs of alias lists
            (where each list is a unique collection of names for resepective space objects)
        -- The standard names dict will include the selected standard name from among all aliases
            this will always prioritize the longest all alpha character name (no numbers, no punctuation)
            additional prioritization can be prompted by setting prioritized_catalog_tags when creating your SOAM
            default prioritized_catalog_tags = ["m", "ngc", "ic"] 
    EXAMPLE:
        t = Soam()
        associations = [["a","b","c"],["c","d"],["e","f"]]
        t.add_associations(associations)
        print(t.all_names())
        print(t.all_aliases())
        print(f"'c' is also known as {t.get_aliases('c')}")
    RETURNS:
        {'d': 0, 'b': 0, 'a': 0, 'c': 0, 'f': 1, 'e': 1}
        {0: {'d', 'b', 'a', 'c'}, 1: {'f', 'e'}}
        'c' is also known as {'d', 'b', 'a', 'c'}
        
    SEARCH FOR ALIASES
        get_aliases
    """
    #Instantiate
    def __init__(self, cleaning_method = provided_cleaning_method, prioritized_common_name_tags = provided_common_name_tags, prioritized_catalog_tags = provided_tag_priorities):
        print("SOAM Started ---------------- ")
        self.names={}
        self.aliases={}
        self.standard_names = {}
        self.cleaning_method = cleaning_method
        self.prioritized_catalog_tags = prioritized_catalog_tags
        self.prioritized_common_name_tags = prioritized_common_name_tags
        s_test = "   #][!,@ ^&*NGc224-.99+9abc. ...   " # a messy string to test
        if self.cleaning_method != False:
            try:
                print("SOAM Cleaning Method Test -- ")
                print(f'original test string: "{s_test}"')
                print(f'cleaned test string: "{cleaning_method(s_test)}"')
            except Exception as e:
                print("Provided cleaning method must accept a single string arg.")
                print(e)
    #Methods
    def __str__(self):
        """For simple printing description of the SOAM."""
        return f'{len(self.names)} names / aliases mapped across {len(self.aliases)} objects.'
    def all_names(self):
        """Returns the names dict structure"""
        return(self.names)
    def all_aliases(self):
        """Returns the aliases dict structure"""
        return(self.aliases)
    def all_standard_names(self):
        """Returns the standard_name dict structure"""
        return(self.standard_names)
    def common_items(self,set1,set2):
        """
        Pass two lists that potentially contain identical items
        Returns true if any items match between the two lists, false if none
        """
        return(any(item1 == item2 for item1 in set1 for item2 in set2))  
    def next_available_key(self):
        """return the next available key value for a unique alias set"""
        keys = sorted(self.aliases.keys())
        i = 0
        key_found = False
        while not key_found and i<len(keys):
            key_found = keys[i] != i
            i = i + 1
        if key_found:
            i = i - 1
        return(i) # i is the next available key
    
    def set_standard_names(self):
        for alias_key in self.all_aliases():
            #each alias keyed set will have a name prioritized as the "standard name"
            prioritized_name = "" 
            #get the current looped set
            alias_set = self.all_aliases()[alias_key]
            #check if there are any strictly alpha-only strings (like a common name)
            alpha_options = [s for s in alias_set if not bool(re.search(r'\d', s))]
            if len(alpha_options)>0: #if there is strictly alpha-only string(s)
                for tag in self.prioritized_common_name_tags: #loop through each common name tag prioritized
                    for name in alpha_options: #loop and check out each name in the current alias set alphas
                        if tag in name: 
                            #if the prioritized tag was found in the name
                            prioritized_name = name #...that name should be prioritized
                            break
                    if prioritized_name != "": # if the prioritized name has been filled
                        break # ... break the common name loop
                if prioritized_name == "": #if the prioritized still has not been filled then...
                    #...return the longest one
                    prioritized_name = max(alpha_options,key=len)
            else:
                for tag in self.prioritized_catalog_tags: #loop through each catalog tag prioritized
                    for name in alias_set: #loop and check out each name in the current alias set 
                        if name.startswith(tag): 
                            #...then make the first tagged name the prioritized standard name 
                            prioritized_name = name
                            break # then break the alias name loop
                    if prioritized_name != "": # if the prioritized name has been filled
                        break #then break out of the tag loop
                if prioritized_name == "": # if the prioritized name has NOT been filled
                    #then just take the first, non-min/max, alias name stored as the standard name
                    lengths = [len(name) for name in alias_set]
                    if len(lengths)>2: #the following loop will need more than 2 name s to work (the min and max rule will cause issue with only two names)              
                        for name in alias_set:
                            if (len(name) != min(lengths)) and (len(name) != max(lengths)):
                                prioritized_name = name
                                break #stop looking, the standard name is found
                    else: #we have exhausted all priority options...
                        #... just take the smallest name out of the one or two alias options
                        prioritized_name = min(alias_set,key=len)
                        
                if prioritized_name == "": #if, for whatever reason, we still have no prioritized standard name
                    #take the first name in the aliase set as the "standard name"
                    prioritized_name = list(alias_set)[0]
            #set the standard name at the corresponding key of the alias set...
            self.standard_names[alias_key] = prioritized_name
        
    
    def add_associations(self,associations):
        """
        Pass in a list of associations
        associations = [["a","b","c"],["c","d"],["e","f"]]
        ... where 'a' is associated with 'b' and 'c' and 'd but not 'f' nor 'e'
        """
        for association_set in associations:
            #association_set = set(association_set) #standardize the passed association as a set
            #if a cleaning method was passed in... 
            if self.cleaning_method != False:
                association_set = {self.cleaning_method(name) for name in association_set} 
            else:
                association_set = set(association_set)
                
            #Scrub out all names less than 2 characters long (1 or 0 characters is not enough to id an object)
            association_set = {item for item in association_set if len(item)>1}
            
            #set up some helper variables
            # To store all indexes of alias sets that have a common item with the current association
            found_matches = [] 
            #loop through each alias set in current aliases
            for alias_key in self.aliases:
                alias_set = set(self.aliases[alias_key])
                #... and compare the looped alias set to the current association set
                if self.common_items(alias_set,association_set):
                    # ...if there is a common item,
                    found_matches.append(alias_key) #... then append the key of the alias set to found matches
            #Once all matches are found...
            found = len(found_matches)>0
            if found: #Then we need to merge all associated aliase key points found with matches
                #... merge the common aliases into the first most found match key of the alias sets
                merge_point = found_matches[0]
                # ... and note the points you need to delete once merged...
                delete_points = set(found_matches[1:]) # make it a set to remove duplicate matches
                # Loop through and merge all alias set key points to the merge point...
                for point_merging in delete_points:
                    self.aliases[merge_point] = self.aliases[merge_point]|self.aliases[point_merging]
                    #... then delete the alias key point that was merged at the merge point
                    del self.aliases[point_merging]
                    
                #Now, finally merge the current association to the alias set merge point
                self.aliases[merge_point] = self.aliases[merge_point]|association_set
            else: # This is a new associated set of names unique from all other alias sets. 
                #(new object found!)
                self.aliases[self.next_available_key()] = association_set

        #make a new names dict from the aliases dict
        self.names = {inner_value: key for key, value in self.aliases.items() for inner_value in value}
        
        #set all standard names from all the alias sets
        self.set_standard_names()
        
        #SET MAX WORD COUNT
        self.max_word_count = max(len(name.split()) for name in self.names)
        
    def get_aliases(self,name):
        """returns all aliases associated with the passed name"""
        name = self.cleaning_method(name)
        try:
            return(self.aliases[self.names[name]])
        except KeyError:
            #print(f"Alias names not found for '{name}'")
            error = name #silent exception
            
    def get_standard_name(self,name):
        """returns the standard name associated with the passed name"""
        name = self.cleaning_method(name)
        try:
            return(self.standard_names[self.names[name]])
        except KeyError:
            #print(f"Standard name not found for '{name}'")
            error = name #silent exception
            
    def alias_filter_on(self,condition, duplicates_only = False):
        """
        Pass in a function "condition" that returns a boolean based on text imput
         -- EXAMPLES
          -- condition = lambda s: s.startswith('m ') # TRUE if s starts with "m "
          -- condition = lambda s: len(s.split()) >= 2 # TRUE if s contains 2 or more words
        RETURNS a filtered alias dict of only alias set names that meet the passed "condition"
        """
        found_conditions = {}
        for alias_key, alias_set in self.all_aliases().items():
            set_names_found = [name for name in alias_set if condition(name)]
            if duplicates_only:
                if len(set_names_found)>1:
                    found_conditions[alias_key] = set_names_found
            else:
                found_conditions[alias_key] = set_names_found

        return found_conditions
    
    def export_soam(self,file_location = "data/", file_name = "my_exported_soam"):
        #WE need to have a set encoder to make all sets into a list for json ----------
        def set_encoder(obj):
            if isinstance(obj, set):
                return list(obj)
            raise TypeError(f"{obj} is not JSON serializable")
        # -----------------------------------------------------------------------------
        file_name = file_name+".json"
        file_location = file_location+file_name
        with open(file_location, 'w') as json_file:
            json.dump(self.aliases, json_file, default=set_encoder)
            
    def import_soam(self,file_location = "data/", file_name = "my_exported_soam"):
        #reset aliases, names, and standard names to the imported soam values
        self.aliases = {}
        self.names = {}
        self.standard_names = {}
        
        file_name = file_name+".json"
        file_location = file_location+file_name
        with open(file_location, 'r') as json_file:
            imported_aliases = json.load(json_file)
        
        #ADD IN IMPORTED ALIASES
        if self.cleaning_method != False:
            for key, names in imported_aliases.items():
                self.aliases[int(key)] = {self.cleaning_method(name) for name in names}
        else:
            for key, names in imported_aliases.items():
                self.aliases[int(key)] = set(names)
        
        #ADD IN IMPORTED NAMES
        #make a new names dict from the aliases dict
        self.names = {inner_value: key for key, value in self.aliases.items() for inner_value in value}
        
        #ADD IN IMPORTED NAMES
        #set all standard names from all the alias sets
        self.set_standard_names()
        
        #SET MAX WORD COUNT
        self.max_word_count = max(len(name.split()) for name in self.names)
        
    def generate_all_ngrams(self,sentence):
        """
        Returns all ngrams generated from the given string, up to the max word count in self names
        EXAMPLE:
        generate_all_ngrams("Can you jump?")
        returns:
        ['Can', 'you', 'jump?', 'Can you', 'you jump?']
        """
        words = sentence.split()
        ngrams = []
        for n in range(1,self.max_word_count+1):
            for i in range(len(words) - n + 1):
                ngram = " ".join(words[i:i + n])
                ngrams.append(ngram)
        return ngrams
        
    def switch_in_standard_names(self, sentence):
        """
        Takes in a string 'sentence' and generates all ngrams with 'sentence'
        Then looks through all ngrams and switch in the "standard names" of an name found in both the ngram and in the soam
        return the string with standard names switched in.
        EXAMPLE:
        switch_in_standard_names("Jump to m31")
        returns:
        'Jump to andromeda galaxy' #... assuming m31's standard name is 'andromeda galaxy'
        """
        sentence = self.cleaning_method(sentence)
        all_ngrams = self.generate_all_ngrams(sentence)
        standard_names = [self.get_standard_name(ngram) for ngram in all_ngrams]
        switches = dict(zip(all_ngrams,standard_names))  
        cleaned_switches = {key:value for key,value in switches.items() if value != None}
        
        for key, value in cleaned_switches.items():
            sentence = sentence.replace(key, value)
        return sentence
        
    def find_all_names(self, sentence):
        """
        Takes in a string 'sentence' and generates all ngrams with 'sentence'
        Then looks through all ngrams and returns a list of all identified names from the 'sentence'
        """
        sentence = self.cleaning_method(sentence)
        all_ngrams = self.generate_all_ngrams(sentence)
        return [ngram for ngram in all_ngrams if ngram in self.all_names()]