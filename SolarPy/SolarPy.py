import glob
import sys
import os
from calendar import monthrange
import numpy as np
import pandas as pd


class SolarPy:
    """
    Helper function to parse Kp data
    """
    def __init__(self):
        # do init stuff
        self.df_kp   = None
        self.df_kp_all = None
        self.str_ext = ".tab" # filetype of Kp values

    def read_kp_all(self, str_dir):
        """ Read Kp values from a directory into a dataframe """
        list_files = self.get_filelist(str_dir)

        i_df = 0
        for kp_file in list_files:
            self.read_kp_tab(kp_file)

            if i_df == 0:
                self.df_kp_all = self.df_kp
            else:
                self.df_kp_all = pd.concat([self.df_kp_all, self.df_kp])
            
            i_df = i_df + 1
    
    def read_kp_year(self, str_dir, val_year):
        """ Read Kp values from a year into a dataframe """
        i_year = 0
        i_df = 0
        for year in val_year:
            list_files = self.get_filelist(str_dir, str(year))

            for kp_file in list_files:
                self.read_kp_tab(kp_file)

                if i_df == 0 and i_year == 0:
                    self.df_kp_all = self.df_kp
                else:
                    self.df_kp_all = pd.concat([self.df_kp_all, self.df_kp])
                
                i_df = i_df + 1
            i_year = i_year + 1

    def read_kp_tab(self, str_filepath):
        # Read the tab file of Kp values
        # Example line:
        # 000101  5+ 5- 4o 3+  4+ 3o 4+ 4-   33- D2  30 1.3
        # yymmdd
        # Kp value on third-scales: 5+ == 5 1/3, 5- == 5 2/3
        #
        # Column  Format  Description
        # ======  ======  ===========
        # 1- 2     i2    yy, last two digits of year
        # 3- 4     i2    mm, month (1-12)
        # 5- 6     i2    dd, day of month (1-31)
        # 8-19    4a3    3-hourly Kp indices, first 4 values
        # 21-32    4a3    3-hourly Kp indices,  last 4 values
        # 35-38     a4    Daily Kp sum (supplied only for tradition,
        #                             use Ap for scientific purposes!)
        # 39-42     a4    Most disturbed and quiet days;
        #                 Q: most quiet days (1-10, 10th quiet day is marked Q0)
        #                 D: most disturbed days (1-5)
        #                 A, K: not really quiet day
        #                 *: not really disturbed day
        # 43-45     i3    Ap index
        # 46-50     f5.2  Cp geomagnetic index.

        # Get number of days in month
        str_filename = os.path.basename(str_filepath).split('.')[0]
        num_days, date_val, date_kp_val = self.get_num_days_in_month(str_filename)

        vec_kp_dates = date_kp_val + pd.to_timedelta(np.arange(num_days*8)*3, 'H')
        vec_days     = date_val + pd.to_timedelta(np.arange(num_days), 'D')

        kp_vals = []
        ap_vals = []

        try:
            with open(str_filepath) as f:
                line_list = f.readlines()
                i_day = 1
                for str_line in line_list: # each day
                    # val_list = str_line.split(' ')
                    yy   = str_line[0:2]
                    mm   = str_line[2:4]
                    dd   = str_line[4:6]
                    if dd.isspace():
                        break # end of the month

                    kp_1 = self.convert_from_third(str_line[8:10])
                    kp_2 = self.convert_from_third(str_line[11:13])
                    kp_3 = self.convert_from_third(str_line[14:16])
                    kp_4 = self.convert_from_third(str_line[17:19])

                    kp_5 = self.convert_from_third(str_line[21:23])
                    kp_6 = self.convert_from_third(str_line[24:26])
                    kp_7 = self.convert_from_third(str_line[27:29])
                    kp_8 = self.convert_from_third(str_line[30:32])

                    kp_sum        = self.convert_from_third(str_line[35:38])
                    quiet_disturb = str_line[39:42]
                    ap_val        = str_line[43:45]
                    cp_val        = str_line[46:49]

                    kp_vals.extend([kp_1, kp_2, kp_3, kp_4, kp_5, kp_6, kp_7, kp_8])
                    ap_vals.append(ap_val)

                    i_day = i_day + 1
                    if(i_day > num_days):
                        break
                
                if len(kp_vals) < len(vec_kp_dates):
                    vec_kp_dates = date_kp_val + pd.to_timedelta(np.arange(len(kp_vals))*3, 'H')
                self.df_kp = pd.DataFrame({"Time":vec_kp_dates, "Kp":kp_vals})
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    
    def get_filelist(self, str_dir, str_year="", str_month=""):
        """ Gets the list of tab files in the directory """
        assert os.path.isdir(str_dir), "Please enter valid directory"
        if not str_year and not str_month:
            str_specific = ""
        elif not str_month:
            str_specific = "kp" + str_year[-2:]
        elif not str_year:
            str_specific = "kp*" + str_month
        else:
            str_specific = "kp" + str_year[-2:] + str_month

        str_search = str_dir + os.path.sep + str_specific + "*" + self.str_ext
        return glob.glob(str_search)
    
    def get_num_days_in_month(self, str_dateval):
        """ Gets the number of days in a month given a tab datetime string
            monthrange(2011, 2)
            (1, 28) """
        assert len(str_dateval) == 6, "Dateval needs to have six values"
        str_yy = str_dateval[2:4]
        str_mm = str_dateval[4:6]
        if(str_yy[0] == '9'):
            # 199x
            yy_val = int("19" + str_yy)
        else:
            yy_val = int("20" + str_yy)
        mm_val = int(str_mm)

        date_val     = pd.to_datetime(str(yy_val) + str_mm + "01 12:00:00")
        str_datetime = str(yy_val) + str_mm + "01 01:30:00"
        date_kp_val = pd.to_datetime(str_datetime)

        rng_month = monthrange(yy_val, mm_val)
        return rng_month[1], date_val, date_kp_val

    def convert_from_third(self, str_kp):
        """ Converts from the 'third' data format into float """
        if not str_kp or str_kp.isspace():
            return np.NaN # blank

        assert len(str_kp) >= 2, "Kp string length requirement not met"

        base_val = float(str_kp[:-1])

        if str_kp[-1] == '+':
            val_add = 0.333
        elif str_kp[-1] == '-':
            val_add = 0.666
        else:
            val_add = 0.0
        
        return base_val + val_add