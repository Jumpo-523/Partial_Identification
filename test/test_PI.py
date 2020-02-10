
import os,sys
# Add the ptdraft folder path to the sys.path list
# import pdb; pdb.set_trace()

sys.path.append(os.path.abspath("."))

# このrootdirで"pytest"を実行している。
ROOT_DIR = '/Users/junpei.takubo/Downloads/Partial_Identification'
from Partial_Identification import BasePI
import pandas as pd
import pytest
import pdb; pdb.set_trace()
print(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(ROOT_DIR+"/data/train.csv", low_memory=False)
pi = BasePI("Sales", "Promo", df)
def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0

class TestBasePI:

    def test_prob_z(self):
        assert pi.prob_z == {0: 0.6184854833175877, 1: 0.3815145166824124}