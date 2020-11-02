import re
import os
from typing import Tuple, Dict, List

class ParliamentDiscussionsDocumentParser:

    def __init__(self, document_path: str):
        self.document_path = document_path
        self.deputies_docs_unprocessed = {}
        self.documents_unprocessed_idx = {}
        self.documents_to_deputies = {}
        self.DATE_SECTION_REGEX = "(?i)\d+ de (\w+) de \d{4}"
        self.REGEX_TO_SPLIT_DOCUMENTS = "(O|A)+\s+Sr(\.|\.º|\.ª)\s+([A-zÀ-ú]|\s*)+(\(.*\))?: —"
        romanic_number = "(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})"
        self.SERIES_SECTION_REGEX = romanic_number + " (Série|SÉRIE) — (Número|NÚMERO) \d{1,3}"
        
    
    def parse(self) -> Tuple[Dict[str,List[int]], Dict[int, str], Dict[int, str]]:
        """
            This functions parses the file and returns three dictionary structures:
            - deputies_docs_unprocessed: This structute is a dictionary mapping the Intervinient 
                                         with the index of associated interventions.
                                         With the index of the intervetions, the intervetions can
                                         fetched from the dictionary `documents_unprocessed_idx`
            - documents_unprocessed_idx: This structure is a dictionary mapping an index with an intervention.
            - documents_to_deputies:     This structure is a dictionary that maps the index of a intervention with its Intervinient.
        """

        doc_idx = 0

        with open(self.document_path) as file:
            pattern = re.compile(self.REGEX_TO_SPLIT_DOCUMENTS)
            date_section_pattern = re.compile(self.DATE_SECTION_REGEX)
            series_section_pattern = re.compile(self.SERIES_SECTION_REGEX)
            numberic_pattern = re.compile("\d+")
            
            current_docs = ""
            current_deputy = None
            
            for line in file:
                date_section_match = date_section_pattern.search(line)
                series_section_match = series_section_pattern.search(line)
                if date_section_match is not None or series_section_match is not None:
                    #we are in a section, let's consume until a number appear
                    line_is_page_number = False
                    while not line_is_page_number:
                        #check if line is number
                        #if it is, then line_is_page_number = True
                        line = next(file)
                        numeric_match = numberic_pattern.search(line)
                        if numeric_match is not None:
                            line_is_page_number = True
                            line = next(file)
                match = pattern.search(line)
                if match is not None:
                    #a new document
                    #is this the first one? if it is, then we already consumed the summary section
                    if current_deputy is not None:
                        #save current document
                        self.documents_unprocessed_idx[doc_idx] = current_docs
                        if current_deputy not in self.deputies_docs_unprocessed:
                            self.deputies_docs_unprocessed[current_deputy] = []
                        self.deputies_docs_unprocessed[current_deputy].append(doc_idx)
                        self.documents_to_deputies[doc_idx] = current_deputy
                        doc_idx += 1
                    #docs stored. start processing new one
                    current_deputy = match.group()[0:-3]
                    current_docs = line.replace(current_deputy, '')
                else:
                    current_docs += line
            if current_deputy is not None:
                        #save current document
                        self.documents_unprocessed_idx[doc_idx] = current_docs
                        if current_deputy not in self.deputies_docs_unprocessed:
                            self.deputies_docs_unprocessed[current_deputy] = []
                        self.deputies_docs_unprocessed[current_deputy].append(doc_idx)
                        self.documents_to_deputies[doc_idx] = current_deputy
                        doc_idx += 1
        
        return self.deputies_docs_unprocessed, self.documents_unprocessed_idx, self.documents_to_deputies
