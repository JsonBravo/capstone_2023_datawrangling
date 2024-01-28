# capstone_2023_datawrangling
This holds all Jupyter Notebooks used during my 2023 MSDS Capstone Project, as well as all data, deliverables, classes, and methods. Will leave as a public repository while the Capstone gets graded.

# A Description of Notebook files:
* 0.0 -- A simple exploration notebook. The initial look at the title text data alonge with some comments regarding expected challenges.
* 0.1.0 -- The development Notebook for the Soam Python class. The methods explored here were distiled and finalized in the 'soam_class' file found in the 'classes_and_methods' folder.
* 0.1.1 -- The development Notebook for the final SOAM data structure. 
* 0.1.2 -- Doubles as an exploration as well as a development Notebook looking at Elasticsearch synonym filter application and file formatting. The final synonym filter was made at the end of this file.
* 0.2 -- An exploration Notebook looking at standardizing space object names and IDs in a string to a single standard name. No real benifit observed, so this approach was not used in this capstone project.
* 0.3 -- The development Notebook for the title data augmentation. The methods explored here were distiled and finalized in the 'title_data_augmenter_class' file found in the 'classes_and_methods' folder.
* 1.0 -- The development notebook which all subsequent scaled iterations (1.1, 1.2, 1.3) were based on.
* 1.1 -- This is the first scaled iteration of augmentation and modeling assessments
* 1.2 -- This is the second scaled iteration of augmentation and modeling assessments
* 1.3 -- This is the third scaled iteration of augmentation and modeling assessments
* 2.0 -- This is the development Notebook where final model tuning methods were explored and resulting models were assessed. The final model exported at the end of this Notebook was used in the subsequent '2.1_Tuned_Results' Notebook.
* 2.1 -- This is the development Notebook were the final Model results was assessed and reviewed.
* 3.0 -- This Notebook provide examples of each deliverable and how they can be utilized for implementation.
* AstroCatelogues -- This is the spread sheet where all SOAM seed source data was corralled.
* Synonym_Implementation_NOTES -- This is a PDF describeing some challenges (and possible solutions) for implementing the Synonym Filter file (the 'astrononimcal_synonyms_112923' file found in the 'deliverables' folder).
* Classification and Data Wrangling on the Amateur Astronomy Frontier 2023 Capstone Zach Jacobson -- The final paper submitted to the University of WI for graduation.

# The 'data' Folder (ZIPPED)
This folder contains the bulk data used and generated through out this capstone project. Some notable files include:
* 'astrobin_titles_to_subject_types' -- A csv file provided by AstroBin, used as the training data for classification modeling.
* 'Augement_Equipment_OPT' A txt file of astronomy equipment details scraped from the OPT website (https://optcorp.com/) used as supplement data for the training data augmentation method.
* 'Augement_NOCTILUCENT_CLOUDS_GPT' -- A txt file of ChatGPT generated descriptions of Noctilucent Clouds, used as supplement data for the training data augmentation method.
* 'Augement_NOCTILUCENT_CLOUDS_Wiki' -- A txt file scraped from Wikipedia (https://en.wikipedia.org/wiki/Noctilucent_cloud) regarding Noctilucent Clouds, used as supplement data for the training data augmentation method.
* 'Augement_NORTHERN_LIGHTS_GPT' -- A txt file of ChatGPT generated descriptions of Northern Lights / Aurora, used as supplement data for the training data augmentation method.

# The 'deliverables' Folder (ZIPPED)
This folder contains the data sets, files, and methods required for the deliverables, as described in the '3.0_Capstone_Deliverables' Notebook file     
