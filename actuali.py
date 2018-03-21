import pandas as pd
import numpy as np
from tqdm import tqdm
from config import config
from data.datafeeder import DataFeeder

data = DataFeeder()

def main():
    data.checker()



if __name__ == '__main__':
    main()
    
