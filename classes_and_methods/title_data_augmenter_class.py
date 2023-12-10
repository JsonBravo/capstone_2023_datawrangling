from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import classes_and_methods.soam_class as soam #contains a text cleaning method
import re
import random
import math
import pandas as pd

#HELPER METHODS
def smooth_towards_center(numbers, smoothing_factor):
    """
    TAKES:
    a list of numbers
    smoothing_factor of 0-1 (0 being no smoothing)
    RETURNS a list of smoothed_numbers
    """
    smoothed_numbers = []
    central_value = sum(numbers) / len(numbers)
    for number in numbers:
        # Calculate a weighted average
        smoothed_value = round((smoothing_factor * central_value) + (1 - smoothing_factor) * number)
        smoothed_numbers.append(smoothed_value)

    return smoothed_numbers

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    synonyms = [soam.provided_cleaning_method(x) for x in synonyms]
    return synonyms

def synonym_replacement(text, iterations=1):
    #print(f'----{text}')# ------- TESTING
    words = text.split()
    augmented_text = words.copy()
    # Iterate 'n' times to perform synonym replacement
    for _ in range(iterations):
        # Choose a random index to replace a word with a synonym
        word_index = random.randint(0, len(words) - 1)
        # Get a list of synonyms for the selected word
        synonym_list = get_synonyms(words[word_index])
        # If synonyms are available, choose one randomly and replace the original word
        if synonym_list:
            synonym = random.choice(synonym_list)
            augmented_text[word_index] = synonym
    #return synonym replaced string
    return ' '.join(augmented_text)

def random_split(input_string, n):
    #print(f'{n}: {input_string}') #--- TESTING
    # Get indices of whitespace in the input string
    whitespace_indices = [i for i, char in enumerate(input_string) if char.isspace()]
    # Choose n-1 random indices from the whitespace positions
    split_indices = random.sample(whitespace_indices, n-1) + [len(input_string)]
    # Sort the split indices for consistency
    split_indices.sort()
    # Initialize variables to keep track of split portions
    split_parts = []
    prev_index = 0
    # Iterate over split indices
    for index in split_indices:
        split_parts.append(input_string[prev_index:index].strip())
        prev_index = index
    return split_parts

def splicer(str1, str2):
    """
    Takes two strings makes n number of cuts to each
    make (the wrong) assumption that all portions are equal in size 
    randomly select portions from each str until you get a "whole"
    returns the spliced result of the selected portions
    """
    n_cuts = math.floor(min(str1.count(' '),str2.count(' '))/2)
    n_portions = n_cuts+1 #... if you cut twice you get three portions
    #portion out the string
    #print(f'STRINGS 1:{str1} ----- 2:{str2}')#--- TESTING
    if n_cuts>0:
        portions1 = random_split(str1,n_portions)
        portions2 = random_split(str2,n_portions)
    else:
        portions1 = [str1]
        portions2 = [str2]
    #...and shuffle the portions
    random.shuffle(portions1)
    random.shuffle(portions2)
    #return spliced string
    spliced_str = ""
    for i in range(0,n_portions):
        if(i%2==0): #all even numbered iterations take from str1
            spliced_str = spliced_str +" "+ portions1[i]
        else: #all uneven numbered iteration take from str2
            spliced_str = spliced_str +" "+ portions2[i]
    return(spliced_str.strip())

def portion_sampler(s, portion_size = 5, sample_size = 1):
    # Split the text into words
    words = s.split()
    # Ensure n is a valid size
    if portion_size <= 0 or portion_size > len(words):
        return []
    # Generate and return the sampled portions
    portions = [' '.join(words[i:i+portion_size]) for i in range(len(words) - portion_size + 1)]
    sampled_portions = random.sample(portions,sample_size)
    return sampled_portions

#requires from nltk.corpus import stopwords AND import classes_and_methods.soam_class as soam #contains a text cleaning method
english_stopwords = stopwords.words('english')
def clean_and_remove_stops(strings, english_stopwords = english_stopwords, cleaning_method = soam.provided_cleaning_method):
    #clean strings in a standard way
    strings = [cleaning_method(s) for s in strings]
    #split strings into tokens 
    tokenized_strings = [s.split() for s in strings]
    # Remove stop words from each list of words
    filtered_strings = [
        ' '.join([w for w in words if w not in english_stopwords]) for words in tokenized_strings
    ]
    return filtered_strings#english_stopwords
    
# GET SUPLEMENTAL EQUIPMENT DATA
# This file is a copy-paste of the https://optcorp.com/ catalog for:
# TELESCOPES
# MOUNTS
# CAMERAS
#... all pages

file_name = 'Augement_Equipment_OPT'
with open(f'data/{file_name}.txt', 'r') as file:
    # Read the file line by line and store each line in a list
    file_lines = file.readlines() 

#IGNORE HEADERS 
headers = '-------'
#Ignore short text lines
n = 18
#ignore pricing text lines
usd = '$'
# JUST EQUIPMENT text NAMES SHOULD REMAIN
equipment_text = {x for x in file_lines if (headers not in x) and (len(x)>n) and (usd not in x)}
#ignore new line characters
equipment_text = {re.sub('\n','', x) for x in equipment_text}
#equipment_text
print(f'{len(equipment_text)} lines from "{file_name}" file downloaded for supplement')


# GET SUPLEMENTAL NOCTILUCENT_CLOUDS TEXT
file_name = 'Augement_NOCTILUCENT_CLOUDS_Wiki'
with open(f'data/{file_name}.txt', 'r') as file:
    # Read the file line by line and store each line in a list
    file_text = file.read() 

noctilucent_string = re.sub('[0-9]','',file_text)
#noctilucent_string
print(f'"{file_name}" string downloaded for supplement')

# GET SUPLEMENTAL NOCTILUCENT_CLOUDS DATA
#generated a variaty of NOCTILUCENT CLOUD descriptions using ChatGPT
file_name = 'Augement_NOCTILUCENT_CLOUDS_GPT'
with open(f'data/{file_name}.txt', 'r') as file:
    # Read the file line by line and store each line in a list
    file_lines = file.readlines() 

#ChatGPT NOCTILUCENT CLOUD lines
noctilucent_text = {x for x in file_lines if len(x)>1}
#ignore new line characters
noctilucent_text = {re.sub('\n','', x) for x in noctilucent_text}
#noctilucent_text
print(f'{len(noctilucent_text)} lines from "{file_name}" file downloaded for supplement')

# GET SUPLEMENTAL NORTHERN_LIGHTS DATA
#generated a variaty of NOCTILUCENT CLOUD descriptions using ChatGPT
file_name = 'Augement_NORTHERN_LIGHTS_GPT'
with open(f'data/{file_name}.txt', 'r') as file:
    # Read the file line by line and store each line in a list
    file_lines = file.readlines() 

#ChatGPT NOCTILUCENT CLOUD lines
northernlights_text = {x for x in file_lines if len(x)>1}
#ignore new line characters
northernlights_text = {re.sub('\n','', x) for x in northernlights_text}
#northernlights_text
print(f'{len(northernlights_text)} lines from "{file_name}" file downloaded for supplement')

#NEXT clean up all suplemental data prior to augmentations
english_stopwords = stopwords.words('english') #a list of all english stop words...
equipment_text = clean_and_remove_stops(equipment_text, english_stopwords)
northernlights_text = clean_and_remove_stops(northernlights_text, english_stopwords)
noctilucent_string = clean_and_remove_stops([noctilucent_string], english_stopwords)[0]
noctilucent_text = clean_and_remove_stops(noctilucent_text, english_stopwords)

supplement_params = {
    'DEEP_SKY': {
        'supplement_str':False,
        'supplement_list':False,
        'supplement_synonyms':True},
    'SOLAR_SYSTEM': {
        'supplement_str':False,
        'supplement_list':False,
        'supplement_synonyms':True},
    'WIDE_FIELD': {
        'supplement_str':False,
        'supplement_list':False,
        'supplement_synonyms':True},
    'OTHER': {
        'supplement_str':False,
        'supplement_list':False,
        'supplement_synonyms':True},
    'GEAR': {
        'supplement_str':False,
        'supplement_list':equipment_text,
        'supplement_synonyms':True},
    'STAR_TRAILS': {
        'supplement_str':False,
        'supplement_list':False,
        'supplement_synonyms':True},
    'NORTHERN_LIGHTS': {
        'supplement_str':False,
        'supplement_list':northernlights_text,
        'supplement_synonyms':True},
    'NOCTILUCENT_CLOUDS': {
        'supplement_str':noctilucent_string,
        'supplement_list':noctilucent_text,
        'supplement_synonyms':True},
}
 
def title_data_augmenter(df, counts_table, smoothing_factor, supplement_params,verbose = False):
    """
    Where:
        df holds the un-augmented source data
        counts_table has a 'Subject' col that matches 'subject_types' in df col
        counts_table has a 'Count' col that holds the aggregated count of each corresponding 'Subject'
        smoothing factor is a float 0-1 (0 is no smoothing)
        supplement_params is a dict with 'subject_types' keys holding settings and data for:
            ['supplement_list'] #... this is a list or False
            ['supplement_str'] #... this is a string or False
            ['supplement_synonyms'] #... this is True or False
        verbose is not implemented at this time...
    """
    #Get Augmented Data Set
    augmented_data = {
        'title':[],
        'subject_type':[],
        'augmentation':[]
    }
    #get smoothed table counts
    counts_table['Smoothed_Count'] = smooth_towards_center(counts_table['Count'],smoothing_factor)
    
    for category in supplement_params:
        # Make sure that the subject_type category actually contains data...
        if(len(df[df['subject_type']==category])>0):
            
            # ... Then if there is data, augment it as needed...
            
            #print(f' ----------- {category}') # ------ TESTING
            #collect the astrobin category data
            source_data = list(df[df['subject_type']==category]['cleaned_title'])
            #print(f'   source_data length = {len(source_data)} -- ')  # ------ TESTING

            #randomly trim data down to n IF title count exceeds n
            n = int(counts_table[counts_table['Subject']==category]['Smoothed_Count'])
            if len(source_data)> n: 
                augment_titles = random.sample(source_data,n) #...this is the trim
                augmented_data['title'] = augmented_data['title']+augment_titles
                augmented_data['subject_type'] = augmented_data['subject_type']+[category]*n
                augmented_data['augmentation'] = augmented_data['augmentation']+['sampled']*n
                # ------ TESTING
                #print(f'     {n} titles sampled, {len(source_data)-len(augment_titles)} titles trimmed away, not used.')
                #--------------
            else: #... otherwise, evenly distribute augmentations into the augmented_data based on set params
                #determine how many augmentations are needed to get up to n titles in the given category
                total_n_needed = n - len(source_data)
                #unpack the supplement data
                supplement_list = supplement_params[category]['supplement_list'] #... this is a list or False
                supplement_str = supplement_params[category]['supplement_str'] #... this is a string or False
                supplement_synonyms = supplement_params[category]['supplement_synonyms'] #... this is True or False
                #diversify augmentations across supplemental data option equally
                augmentation_parts = 1 #... we will use n number of augmentation parts
                #DETERMINE n augmentation parts
                if supplement_list: #given a list of strings
                    if supplement_str: #... and a long descriptive string
                        #... add an augment portion for blending spliced list strings with descriptive string w/ source data
                        augmentation_parts = augmentation_parts + 1
                    # add  augment portion for blending spliced source data with list strings
                    augmentation_parts = augmentation_parts + 1
                if supplement_str and not supplement_list: #given only a long descriptive string...
                    #... add an augment portion for blending spliced descriptive string portions w/ source data
                    augmentation_parts = augmentation_parts + 1
                if supplement_synonyms: # are allowed...
                    # add  augment portion for blending some synonyms into a portion of all supplement and source data
                    augmentation_parts = augmentation_parts + 1

                augmentation_n = round(total_n_needed / augmentation_parts)
                total_n_needed = augmentation_n*augmentation_parts
                
                #GET starting population
                ###### SOURCE SAMPLED PORTION ##########################
                augmented_data['title'] = augmented_data['title']+source_data
                augmented_data['subject_type'] = augmented_data['subject_type']+[category]*len(source_data)
                augmented_data['augmentation'] = augmented_data['augmentation']+['sampled']*len(source_data)
                ###### SOURCE RESAMPLED PORTION ########################
                #ALWAYS re-sample a straight portion of the source data 
                all_resamples = random.choices(source_data,k=total_n_needed)
                #pop off the resample portion needed for this augmntation...
                resample_portions = [all_resamples.pop() for _ in range(augmentation_n)]
                augmented_data['title'] = augmented_data['title']+resample_portions
                augmented_data['subject_type'] = augmented_data['subject_type']+[category]*len(resample_portions)
                augmented_data['augmentation'] = augmented_data['augmentation']+['resampled']*len(resample_portions)
                #then SET augmentation parts ... as needed
                if supplement_list: #given a list of strings
                    if supplement_str: #... and a long descriptive string
                        ########## WIKI - CHATGPT BLEND PORTION ########
                        #... add an augment portion for blending spliced list strings with descriptive string w/ source data
                        str_portions = [portion_sampler(supplement_str)[0] for _ in range(augmentation_n)]
                        list_portions = random.choices(supplement_list, k=augmentation_n)
                        blended_portions = [splicer(list_portions[i],str_portions[i]) 
                                            for i in range(augmentation_n)]
                        #pop off the resample portion needed for this augmntation...
                        resample_portions = [all_resamples.pop() for _ in range(augmentation_n)]
                        spliced_portions = [splicer(resample_portions[i],blended_portions[i]) 
                                            for i in range(augmentation_n)]
                        augmented_data['title'] = augmented_data['title']+spliced_portions
                        augmented_data['subject_type'] = augmented_data['subject_type']+[category]*len(spliced_portions)
                        augmented_data['augmentation'] = augmented_data['augmentation']+['wiki_chatgpt']*len(spliced_portions)
                    ######## CHATGPT PORTION ###########################
                    # add  augment portion for blending spliced source data with list strings
                    # ------ TESTING
                    #print(f'n = {n} -- datalength = {len(source_data)} -- augportion = {augmentation_n}')
                    #--------------
                    resample_portions = [all_resamples.pop() for _ in range(augmentation_n)]
                    list_portions = random.choices(supplement_list, k=augmentation_n)
                    spliced_portions = [splicer(resample_portions[i],list_portions[i]) 
                                        for i in range(augmentation_n)]
                    augmented_data['title'] = augmented_data['title']+spliced_portions
                    augmented_data['subject_type'] = augmented_data['subject_type']+[category]*len(spliced_portions)
                    augmented_data['augmentation'] = augmented_data['augmentation']+['chatgpt']*len(spliced_portions)
                ######## WIKI ONLY PORTION ###########################
                if supplement_str and not supplement_list: #given only a long descriptive string...
                    #... add an augment portion for blending spliced descriptive string portions w/ source data
                    #... add an augment portion for blending spliced list strings with descriptive string w/ source data
                    str_portions = [portion_sampler(supplement_str)[0] for _ in range(augmentation_n)]
                    #pop off the resample portion needed for this augmntation...
                    resample_portions = [all_resamples.pop() for _ in range(augmentation_n)]
                    spliced_portions = [splicer(resample_portions[i],str_portions[i]) 
                                        for i in range(augmentation_n)]
                    augmented_data['title'] = augmented_data['title']+spliced_portions
                    augmented_data['subject_type'] = augmented_data['subject_type']+[category]*len(spliced_portions)
                    augmented_data['augmentation'] = augmented_data['augmentation']+['wiki']*len(spliced_portions)
                ######## SYNONYM SWAP PORTION ###########################
                if supplement_synonyms: # if allowed...
                    # add  augment portion for blending some synonyms into a portion of all supplement and source data
                    source_data_choices = random.choices(source_data, k = augmentation_n)
                    synonym_swaps = [synonym_replacement(s) for s in source_data_choices if len(s)>=1]
                    synonym_swaps_choices = random.choices(synonym_swaps, k = augmentation_n)
                    synonym_augments = [splicer(source_data_choices[i],synonym_swaps_choices[i]) 
                                        for i in range(augmentation_n)]
                    #add synonym mixed data
                    augmented_data['title'] = augmented_data['title']+synonym_augments
                    augmented_data['subject_type'] = augmented_data['subject_type']+[category]*len(synonym_augments)
                    augmented_data['augmentation'] = augmented_data['augmentation']+['synonym_swap']*len(synonym_augments)
                # ------ TESTING
                #print(f'     {len(source_data)} available, {total_n_needed} needed to reach {len(source_data)+total_n_needed}')
                # --------------
    df_augmented = pd.DataFrame(augmented_data)
    df_augmented['subject_type'] = df_augmented['subject_type'].astype('category')
    df_augmented['augmentation'] = df_augmented['augmentation'].astype('category')
    df_augmented['title'] = df_augmented['title'].astype(str)
    #df_augmented['data_type'] = []
    #print(df_augmented.describe())# ------ TESTING
    #print(df_augmented.info())# ------ TESTING
    #print(pd.DataFrame(df_augmented['subject_type'].value_counts()).reset_index())# ------ TESTING
    return(df_augmented)
