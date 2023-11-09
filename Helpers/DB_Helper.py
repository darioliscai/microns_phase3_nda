from microns_phase3 import nda
import datajoint as dj
import numpy as np


class DB_Helper:
    
    @staticmethod
    def get_condition_hash_of_repeated_stimuli(
        session:int,
        scan_idx:int, 
        n:int
    ) -> dj.expression.GroupBy:
        table = dj.U('condition_hash').aggr(nda.Trial & {'session':session, 'scan_idx':scan_idx},n='count(*)') & f'n={n}'
        return table