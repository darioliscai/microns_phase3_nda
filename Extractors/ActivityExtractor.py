import datajoint as dj
from microns_phase3 import nda
import numpy as np
from Helpers.DB_Helper import DB_Helper

class ActivityExtractor:

    ORACLE_HASHES = ['KXdTNAGMo1gCWz2Ge8zr',
                     'ecUQJtcERZJGdqza1k7h',
                     '7UETOWO5Z8aWuHDBJ2GG',
                     'GjCMo2GkJp6y5vricadg',
                     'Oup5uAZxF2G7zEJkT+ui',
                     '5zQTb77qI+ig8rigx1XU']
    
    def __init__(self):
        pass
        
    @staticmethod
    def extract_start_end_index_from_condition_hash(
        session:int, 
        scan_idx:int,
        condition_hash: str
    ):
        # key = compose_key(session, scan_idx, condition_hash)
        key = {'session':session, 'scan_idx':scan_idx, 'condition_hash':condition_hash}
        start_idxs, end_idxs = (nda.Trial & key).fetch('start_idx', 'end_idx')
        return start_idxs, end_idxs
    
    def fetch_activity_from_condition_hashes(
        self,
        session:int, 
        scan_idx:int,
        condition_hashes: list,
        limit: int = None
    ) -> list:
        ses_scan_trace = self.fetch_session_and_scan_activity(session, scan_idx, limit)
        output = []
        for ch in condition_hashes:
            start_idxs, end_idxs = self.extract_start_end_index_from_condition_hash(session, scan_idx, ch)
            output.append(np.stack(self.subset_activity(ses_scan_trace, start_idxs, end_idxs)))
        return output
    
    @staticmethod
    def subset_activity(
        trace:np.array,
        start_idxs: list,
        end_idxs: list
    ) -> list:
        output = []
        add_idx = np.min(np.array(end_idxs) - np.array(start_idxs))
        for s, e in zip(start_idxs, end_idxs):
            output.append(trace[:, s:s+add_idx+1])
        return output

    # def fetch_oracle_activity(
    #     self,
    #     session:int, 
    #     scan_idx:int,
    #     limit: int = None
    # ) -> np.array:
    #     trace = self.fetch_session_and_scan_activity(session, scan_idx, limit)
    #     output = []
    #     for ch in self.ORACLE_HASHES:
    #         start_idxs, end_idxs = self.extract_start_end_index_from_condition_hash(session, scan_idx, ch)
    #         output.append(np.stack(self.subset_activity(trace, start_idxs, end_idxs)))
    #     return np.concatenate(output, axis=2)

    @staticmethod
    def fetch_session_and_scan_activity(
        session: int, 
        scan_idx:int, 
        limit:int = None
    ) -> np.array:
        return np.stack((nda.Activity & {'session': session, 'scan_idx':scan_idx}).fetch('trace', limit=limit))
    
    def fetch_repeated_activity(
        self,
        session:int, 
        scan_idx:int,
        n:int, 
        limit: int = None
    ) -> np.array:
        condition_hashes = DB_Helper.get_condition_hash_of_repeated_stimuli(session, scan_idx, n).fetch('condition_hash')
        if condition_hashes:
            trace = self.fetch_session_and_scan_activity(session, scan_idx, limit)
        else:
            raise Exception(f'No activity with {n} repetitions.')
        output = []
        for ch in condition_hashes:
            start_idxs, end_idxs = self.extract_start_end_index_from_condition_hash(session, scan_idx, ch)
            output.append(np.stack(self.subset_activity(trace, start_idxs, end_idxs)))
        return np.concatenate(output, axis=2)
    
    def fetch_spontaneous_activity(
        self,
        
    ) -> np.array:
        pass

    

        
    
    