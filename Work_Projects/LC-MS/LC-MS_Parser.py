# LC-MS_Parser.py
"""A file for cleaning and analyzing MS and LC-MS data."""

import os
import re
import csv
import numpy as np
import pandas as pd
from scipy import linalg as la
from scipy.sparse import linalg as spla
from scipy.sparse import csr_matrix
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import permutations as perm
from sklearn.decomposition import KernelPCA
from sklearn.model_selection import GridSearchCV



def xls_to_csv(path="C:\\Research\Data"):
    """Take every .xls file in the given directory and change it to 
    a .csv file in the current directory."""
    # Get the path from which the files are to be taken
    directory = os.path.abspath(path)
    # Get and parse all of the files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".xls"):
                out = filename.split('.')[0]+'.csv'
                df = pd.read_excel(path+"\\"+filename, 'Sheet1')
                df.to_csv(out, index=False)



def MFE_getter(file_list, outfile, MFE_ESI="MFE", combine=False, mz_tol=0.01, R_tol=1.0, parser="1"):
    """Takes every .csv file whose name is in file_list and creates a new 
    file out_file containing either the MFE spectra or the ESI spectra 
    from each file depending on whether MFE_ESI="MFE" or MFE_ESI="ESI". 
    If combine=True, then all the peaks that are the same between files 
    (as determined by mz_tol and R_tol) are combined into one list and 
    other peaks are ignored."""
    # Set up the information storage system
    n_files = len(file_list)
    C12 = [[] for _ in range(n_files)]
    C12_abundance = [[] for _ in range(n_files)]
    C13 = [[] for _ in range(n_files)]
    C13_abundance = [[] for _ in range(n_files)]
    C132 = [[] for _ in range(n_files)]
    C132_abundance = [[] for _ in range(n_files)]
    RT_peak = [[] for _ in range(n_files)]
    RT_window = [[] for _ in range(n_files)]
    
    # Set whether or not the current data is MFE/ESI and should be recorded
    record = True
    
    # Make regexes for identifying rows with MFE/ESI info
    MFE_checker = re.compile(r"MFE")
    ESI_checker = re.compile(r"ESI")
    
    # Make regexes for getting retention times
    RT_range_getter = re.compile(r"rt: (\d+\.\d\d\d)-(\d+\.\d\d\d)")
    RT_peak_getter = re.compile(r"Cpd \d+: (\d+\.\d\d\d)")
    
    # Iterate over each file name and get the relevant information
    for i, filename in enumerate(file_list):
        # Read in the file
        raw_data = np.zeros(1)
        with open(filename, "r") as file:
            csvreader = csv.reader(file)
            raw_data = np.array([row for row in csvreader])
        # Search for the useable data
        if parser == "1":
            # The value j here represents the index of the row we're currently looking through
            j = 0
            while j < len(raw_data):
                ESI_search = re.search(ESI_checker, raw_data[j][0])
                MFE_search = re.search(MFE_checker, raw_data[j][0])
                RT_range_search = re.search(RT_range_getter, raw_data[j][0])
                RT_peak_search = re.search(RT_peak_getter, raw_data[j][0])
                
                # Record the current RT values
                if RT_range_search:
                    current_RT_range = (float(RT_range_search.group(1)), float(RT_range_search.group(2)))
                if RT_peak_search:
                    current_RT_peak = (float(RT_peak_search.group(1)))
                
                # Check if we should record the next data based on if it's MFE or ESI
                if ESI_search and MFE_search:
                    if MFE_ESI == "MFE":
                        record = True
                    elif MFE_ESI == "ESI":
                        record = False
                    else:
                        raise ValueError("MFE_ESI argument must be \"MFE\" or \"ESI\", not \"{}\"".format(str(MFE_ESI)))
                elif ESI_search and not MFE_search:
                    if MFE_ESI == "MFE":
                        record = False
                    elif MFE_ESI == "ESI":
                        record = True
                    else:
                        raise ValueError("MFE_ESI argument must be \"MFE\" or \"ESI\", not \"{}\"".format(str(MFE_ESI)))
                
                # Record the data as appropriate
                elif raw_data[j][0][0] != "#" and record:
                    # Add the m/z and abundance values
                    C12[i].append(float(raw_data[j][1]))
                    C12_abundance[i].append(float(raw_data[j][2]))
                    # Add the RT peak as a float and the RT window as a tuple
                    RT_peak[i].append(current_RT_peak)
                    RT_window[i].append(current_RT_range)
                    # Add filler values for C13 and 2 C13 peaks
                    C13[i].append("")
                    C13_abundance[i].append("")
                    C132[i].append("")
                    C132_abundance[i].append("")
                    
                    # Check for isotope traces
                    mass_defect = 1.003
                    if j+1 < len(raw_data):
                        # Check for a C13 peak with m/z difference and abundances
                        if raw_data[j+1][0][0] != "#":
                            j1_diff = float(raw_data[j+1][1]) - C12[i][-1]
                            if j1_diff <= (mass_defect + mz_tol) and j1_diff >= (mass_defect - mz_tol) and C12_abundance[i][-1] > float(raw_data[j+1][2]):
                                C13[i][-1] = float(raw_data[j+1][1])
                                C13_abundance[i][-1] = float(raw_data[j+1][2])
                                # Skip forward a row to avoid considering this peak for status as a C12 peak
                                j += 1
                                
                                # Check for a 2 C13 peak
                                if j+1 < len(raw_data):
                                    if raw_data[j+1][0][0] != "#":
                                        j2_diff = float(raw_data[j+1][1]) - C12[i][-1]
                                        # Use abundance and m/z difference to determine if this is a 2 C13 peak
                                        if j2_diff <= 2*(mass_defect + mz_tol) and j2_diff >= 2*(mass_defect - mz_tol) and C13_abundance[i][-1] > float(raw_data[j+1][2]):
                                            C132[i][-1] = float(raw_data[j+1][1])
                                            C132_abundance[i][-1] = float(raw_data[j+1][2])
                                            # Skip forward a row to avoid considering this peak for status as a C12 peak
                                            j += 1
                                            
                                            # Check for further isotopes, but do not record them
                                            further_consideration = True
                                            k = 1
                                            while further_consideration:
                                                if j+1 < len(raw_data):
                                                    if raw_data[j+1][0][0] != "#":
                                                        jn_diff = float(raw_data[j+1][1]) - C12[i][-1]
                                                        if jn_diff <= (2+k)*(mass_defect + mz_tol) and jn_diff >= (2+k)*(mass_defect - mz_tol) and C132_abundance[i][-1] > float(raw_data[j+1][2]):
                                                            j += 1
                                                            k += 1
                                                        else:
                                                            further_consideration = False
                                                    else:
                                                        further_consideration = False
                                                else:
                                                    further_consideration = False
                
                # Move on to the next row
                j += 1
        
        elif parser == "2":
            # Skip the headers
            for row in raw_data[3:]:
                # This format gives only one peak per feature, all nicely organized by row
                C12[i].append(float(row[28]))
                C12_abundance[i].append(float(row[36]))
                RT_peak[i].append(float(row[48]))
                RT_window[i].append((float(row[50]), float(row[33])))
                # Add filler values for C13 and 2 C13 peaks
                C13[i].append("")
                C13_abundance[i].append("")
                C132[i].append("")
                C132_abundance[i].append("")
        
        else:
            raise ValueError("Parser", parser, "is not a valid parser.")
    # Make every peak list the same length
    n_peaks = np.max([len(C12[i]) for i in range(n_files)])
    for i in range(n_files):
        if len(C12[i]) != n_peaks:
            for _ in range(n_peaks - len(C12[i])):
                C12[i].append("")
                C12_abundance[i].append("")
                C13[i].append("")
                C13_abundance[i].append("")
                C132[i].append("")
                C132_abundance[i].append("")
                RT_peak[i].append("")
                RT_window[i].append(("",""))
                
    # Write the info to a file based on if we're combining peaks or not
    if combine and n_files > 1:
        # Create a list of peaks that are the same between files, using the first file as a base. 
        # We check the RT peak, C12 peak, and C13 peak for confirmation
        same_C12 = C12[0]
        same_C13 = C13[0]
        same_RT = RT_peak[0]
        # We keep track of the 2 C13 peaks and abundances
        same_C132 = C132[0]
        same_C132_abundance = C132_abundance[0]
        # We average together the abundances and RT windows
        same_C12_abundance = C12_abundance[0]
        same_C13_abundance = C13_abundance[0]
        same_RT_window = RT_window[0]
        # Trim down the list of peaks that are the same between files
        for file_idx in np.arange(1,n_files):
            # Keep track of the indices of the features that are the same between files
            # "same_indices" tracks the indices of values that were previously identified as being the same between files and that match the current file
            # "candidate_indices" tracks the indices of values in the current file that are identified as being the same as values in previous files
            same_indices = []
            candidate_indices = []
            # Go through each peak of the current file and only keep ones within mz_tol and R_tol of a peak in the "same" list
            for i in range(n_peaks):
                candidate_C12 = C12[file_idx][i]
                candidate_C13 = C13[file_idx][i]
                candidate_RT = RT_peak[file_idx][i]
                # Skip blank entries
                if type(candidate_C12) is str or type(candidate_RT) is str:
                    continue
                # Go through each peak of the "same" list for comparison
                for j in range(len(same_C12)):
                    if type(same_C12[j]) is str or type(same_RT[j]) is str:
                        continue
                    # Compare the C12 peaks
                    if np.abs(candidate_C12 - same_C12[j]) <= mz_tol:
                        # Compare the RT peaks
                        if np.abs(candidate_RT - same_RT[j]) <= R_tol:
                            # Compare the C13 peaks. They need to either both be blank or both be close to each other
                            if type(candidate_C13) == str and type(same_C13[j]) == str:
                                same_indices.append(j)
                                candidate_indices.append(i)
                                break
                            elif type(candidate_C13) == str or type(same_C13[j]) == str:
                                continue
                            else:
                                if np.abs(candidate_C13 - same_C13[j]) <= mz_tol:
                                    same_indices.append(j)
                                    candidate_indices.append(i)
                                    break
            
            # Average the current accepted peaks together and throw out the rest. That is, update the old average with the new peaks
            new_same_C12 = []
            new_same_C13 = []
            new_same_RT = []
            for idx in range(len(same_indices)):
                new_same_C12.append(same_C12[same_indices[idx]]*file_idx/(file_idx+1) + C12[file_idx][candidate_indices[idx]]/(file_idx+1))
                if type(same_C13[same_indices[idx]]) == str or type(C13[file_idx][candidate_indices[idx]]) == str:
                    new_same_C13.append("")
                else:
                    new_same_C13.append(same_C13[same_indices[idx]]*file_idx/(file_idx+1) + C13[file_idx][candidate_indices[idx]]/(file_idx+1))
                new_same_RT.append(same_RT[same_indices[idx]]*file_idx/(file_idx+1) + RT_peak[file_idx][candidate_indices[idx]]/(file_idx+1))
            same_C12 = new_same_C12
            same_C13 = new_same_C13
            same_RT = new_same_RT
            
            # Update the 2 C13 peaks, the abundances, and the RT windows
            new_same_C132 = []
            new_same_C132_abundance = []
            new_same_C12_abundance = []
            new_same_C13_abundance = []
            new_same_RT_window = []
            for idx in range(len(same_indices)):
                # The attributes here are as follows: 
                # "new_same_" is the list that we're filling with only the values that are the same between the current file and the previously considered files
                # The list with no prefix is the actual raw data extracted for each file
                # "same_" is the list that has the values that were the same between the previously considered files but perhaps not this current file 
                for attribute in [(new_same_C132, C132, same_C132), (new_same_C132_abundance, C132_abundance, same_C132_abundance), 
                                  (new_same_C12_abundance, C12_abundance, same_C12_abundance), (new_same_C13_abundance, C13_abundance, same_C13_abundance)]:
                    # If the previously considered lists or the actual raw data have a blank string (str) value, add a blank string value to prevent skewing the average
                    if type(attribute[2][same_indices[idx]]) == str or type(attribute[1][file_idx][candidate_indices[idx]]) == str:
                        attribute[0].append("")
                    # Otherwise, update the average and add it to the "new_same_" list
                    else:
                        attribute[0].append(attribute[2][same_indices[idx]]*file_idx/(file_idx+1) + attribute[1][file_idx][candidate_indices[idx]]/(file_idx+1))
                # Since the format for the RT_window is a little different, we update its values separately
                if type(same_RT_window[same_indices[idx]][0]) == str or type(RT_window[file_idx][candidate_indices[idx]][0]) == str:
                    new_same_RT_window.append(("", ""))
                else:
                    lower_bound = same_RT_window[same_indices[idx]][0]*file_idx/(file_idx+1) + RT_window[file_idx][candidate_indices[idx]][0]/(file_idx+1)
                    upper_bound = same_RT_window[same_indices[idx]][1]*file_idx/(file_idx+1) + RT_window[file_idx][candidate_indices[idx]][1]/(file_idx+1)
                    new_same_RT_window.append((lower_bound, upper_bound))
            same_C132 = new_same_C132
            same_C132_abundance = new_same_C132_abundance
            same_C12_abundance = new_same_C12_abundance
            same_C13_abundance = new_same_C13_abundance
            same_RT_window = new_same_RT_window
        # Write the collected info
        with open(outfile, 'x', newline='') as file:
            csvwriter = csv.writer(file)
            
            # Write the header
            row_to_write = []
            row_to_write += ["Average C12 MFE Peak (m/z) (accurate to within {})".format(mz_tol)]
            row_to_write += ["Average C12 abundance"]
            row_to_write += ["Average C13 MFE Peak (m/z) (accurate to within {})".format(mz_tol)]
            row_to_write += ["Average C13 abundance"]
            row_to_write += ["Average 2 C13 MFE Peak (m/z)"]
            row_to_write += ["Average 2 C13 abundance"]
            row_to_write += ["Total abundance"]
            row_to_write += ["Average RT peak (accurate to within {})".format(R_tol)]
            row_to_write += ["Average RT window start"]
            row_to_write += ["Average RT window end"]
            csvwriter.writerow(row_to_write)
            
            # Write the data
            for i in range(len(same_C12)):
                row_to_write = []
                row_to_write += [same_C12[i]]
                row_to_write += [same_C12_abundance[i]]
                row_to_write += [same_C13[i]]
                row_to_write += [same_C13_abundance[i]]
                row_to_write += [same_C132[i]]
                row_to_write += [same_C132_abundance[i]]
                # Sum the abundance values that actually exist; the ones that don't exist should be the empty string ""
                if type(same_C12_abundance[i]) != str:
                    if type(same_C13_abundance[i]) != str:
                        if type(same_C132_abundance[i]) != str:
                            row_to_write += [same_C12_abundance[i] + same_C13_abundance[i] + same_C132_abundance[i]]
                        else:
                            row_to_write += [same_C12_abundance[i] + same_C13_abundance[i]]
                    else:
                        row_to_write += [same_C12_abundance[i]]
                else:
                    row_to_write += [""]
                row_to_write += [same_RT[i]]
                row_to_write += [same_RT_window[i][0]]
                row_to_write += [same_RT_window[i][1]]
                csvwriter.writerow(row_to_write)
    
    else:
        with open(outfile, 'x', newline='') as file:
            csvwriter = csv.writer(file)
            
            # Write the header
            row_to_write = []
            for j in range(n_files):
                row_to_write += ["C12 Peak (m/z), file {}".format(file_list[j])]
                row_to_write += ["C12 Abundance"]
                row_to_write += ["C13 Peak (m/z)"]
                row_to_write += ["C13 Abundance"]
                row_to_write += ["2 C13 Peak (m/z)"]
                row_to_write += ["2 C13 Abundance"]
                row_to_write += ["RT"]
                row_to_write += ["RT window start"]
                row_to_write += ["RT window end"]
                row_to_write += [""]
            csvwriter.writerow(row_to_write)
            
            # Write the data
            for i in range(n_peaks):
                row_to_write = []
                for j in range(n_files):
                    row_to_write += [C12[j][i]]
                    row_to_write += [C12_abundance[j][i]]
                    row_to_write += [C13[j][i]]
                    row_to_write += [C13_abundance[j][i]]
                    row_to_write += [C132[j][i]]
                    row_to_write += [C132_abundance[j][i]]
                    row_to_write += [RT_peak[j][i]]
                    row_to_write += [RT_window[j][i][0]]
                    row_to_write += [RT_window[j][i][1]]
                    row_to_write += [""]
                csvwriter.writerow(row_to_write)



def MFE_PCA(filename, samples, d, digits=3, get_V=False):
    """Given a file of C12 peaks and abundances (generated from 
    MFE_getter and then trimmed by hand), creates a list of all given 
    features, creates a matrix of the abundances of each feature in 
    each list/column, and then performs PCA on it. Since missing 
    features are more a result of poor machine sensitivity and not 
    necessarily indicative of a true "0" for the abundance of a 
    feature, we replace all zeros with half of the minimum value for 
    that sample.
    
    Parameters:
        filename (str): A .csv file with columns of the form "m/z, 
            abundance, blank, m/z, abundance, blank, m/z, ..." etc., 
            for each sample.
        samples (int): The number of samples in the file.
        d (int): The number of principal components to look at.
        digits (int): The number of digits of accuracy to use after 
            the decimal place for determining if features are unique.
        get_V (bool): Whether or not to also return the projection 
            matrix Vt.
    
    Returns:
        projected_data (n-darray): An array of the samples projected 
            onto their principle components.
        data (n-darray): An array of the samples organized by feature.
        idx_dict (dict): A dictionary mapping indices to features in 
            the data matrix.
        Vt (n-darray): The projection matrix Vt."""
    
    # Get the data
    with open(filename, "r") as file:
        csvreader = csv.reader(file)
        raw_data = np.array([row for row in csvreader])
        # Skip the header
        raw_data = raw_data[1:,:]
    
    # Assert that their are at least "samples" number of samples here
    raw_num = (raw_data.shape[1] + 1)/3
    assert raw_num >= samples, "Only {} samples in file!".format(raw_num)
    
    # Get all of the m/z features
    feature_set = set()
    # Iterate over each sample
    for i in range(samples):
        idx = i*3
        # Iterate over each feature until we reach a blank feature
        j = 0
        while raw_data[j, idx] != "" and j + 1 < raw_data.shape[0]:
            feature_set.add(np.round(float(raw_data[j, idx]), digits))
            j += 1
    
    # Make a dictionary mapping features to indices
    n = len(feature_set)
    feature_dict = {feat:i for i,feat in enumerate(feature_set)}
    
    # Make a data matrix
    data = np.zeros((samples, n))
    # Iterate over each sample
    for i in range(samples):
        idx = i*3
        # Iterate over each feature until we reach a blank feature
        j = 0
        while raw_data[j, idx] != "" and j + 1 < raw_data.shape[0]:
            # Get the index for the feature in the data matrix
            raw_mz = float(raw_data[j, idx])
            feature_idx = feature_dict[np.round(raw_mz, digits)]
            # Fill in the matrix
            data[i, feature_idx] = float(raw_data[j, idx+1])
            j += 1
        # Get the minimum non-zero value
        zero_mask = data[i,:] == 0
        non_zero_data = data[i,:].copy()
        non_zero_data[zero_mask] = np.inf
        min_val = np.min(non_zero_data)
        # Fill in zeros with half of the minimum for the sample
        for k in range(n):
            if data[i,k] == 0:
                data[i,k] = min_val/2
        
    
    # Make a dictionary that's the reverse of the feature dictionary
    dict_features = list(feature_dict.keys())
    dict_indices = list(feature_dict.values())
    idx_dict = {dict_indices[i]:dict_features[i] for i in range(n)}
    
    # Do PCA on the centered data
    means = np.mean(data, axis=0)
    data_centered = data - means
    # Get the svd of the data
    U, S, Vt = la.svd(data_centered)
    # Project onto the principal component space
    projected_data = data.dot(Vt.T[:,:d])
    
    # Return the requested data
    if get_V:
        return projected_data, data, idx_dict, Vt
    return projected_data, data, idx_dict
    


class MSData():
    """A data structure containing a list of mass spectra, where each 
    mass spectrum is a dx2 array with rows of the form [m/z, counts].
    
    Initializes with the path of a directory from which to draw spectra 
    in csv format. The parser argument indicates in which style the data 
    in the files are organized so that the data can be properly parsed.
    
    Attributes:
        N (int): The number of spectra.
        data (list): A length N list of lists of the form (sex, CDR, 
            spectrum), where spectrum is an array of the form [m/z, 
            counts]. For example, typing data[0][0] will give 
            the sex of the person from whom the first spectrum was taken, 
            while data[0][2][0] will give the m/z value and counts of the 
            first peak of the first spectrum in the data.
        sex (nd-array): A length N array of strings corresponding to the sex 
            attributes of the data attribute. Indices match those of data.
        cdr (nd-array): A length N array of strings corresponding to the cdr 
            attributes of the data attribute. Indices match those of data.
        spectra (list): A length N list of arrays corresponding to the 
            spectrum attributes of the data attribute. Indices match those 
            of data.
    
    Functions:
        bin_data(mz_bins, RT_bins, method): Returns an array of the 
            MS counts for each bin. The method parameter determines 
            if the counts are summed or averaged.
        plot_bins(mz_bins, RT_bins, N_labels, method): Plots a graph 
            of the binned data.
        PCA(d): Project the binned spectra into a d-dimensional space 
            spanned by the first d principal components of the data.
        plot_PCA: Plot the binned spectra as projected into 2D or 3D 
            space by the PCA function. The data can be labeled by sex, by 
            CDR, by both, or by neither.
        """
    
    
    def __init__(self, path="C:\\Research\Data", parser="1"):
        # Initialize counters and data storage
        self.N = 0
        self.data = []
        self.sex = []
        self.cdr = []
        self.spectra = []
        
        # Make regexes for extracting data from file names
        if parser == "1":
            sex_finder = re.compile(r"\d* (B|F)")
            cdr_finder = re.compile(r"\d* \w?([1-4])")
        elif parser == "2":
            sex_finder = re.compile(r"\d*[_ ]+(M|F)\d* ")
            cdr_finder = re.compile(r"\d*[_ ]+\w([0-4]{1,2}) ")
        
        # Get the path from which the files are to be taken
        directory = os.path.abspath(path)
        
        # Get and parse all of the files
        for root, dirs, files in os.walk(directory):
            for filename in files:
                
                # Parse according to the specified method
                if parser == "1":
                    if filename.endswith(".csv"):
                        with open(path+"/"+filename, "r") as file:
                            self.N += 1
                            csvreader = csv.reader(file)
                            raw_data = np.array([row for row in csvreader])
                        # Set each data entry with the right default values
                        n = len(raw_data)-1
                        data_list = ["O", -1, np.zeros((n,2))]
                        # Look for sample sex
                        sex_search = re.search(sex_finder, filename)
                        if sex_search:
                            if sex_search.group(1) == "F":
                                data_list[0] = "F"
                            elif sex_search.group(1) == "B":
                                data_list[0] = "M"
                        # Look for sample CDR
                        cdr_search = re.search(cdr_finder, filename)
                        if cdr_search:
                            data_list[1] = int(cdr_search.group(1))
                        # Fill in the m/z values and counts
                        i = 0
                        j = 0
                        while j < n:
                            # Skip headers
                            if raw_data[i][0].replace(".","",1).isdigit():
                                data_list[2][j,0] = float(raw_data[i][0])
                                data_list[2][j,1] = float(raw_data[i][2])
                                j += 1
                            else:
                                pass
                            i += 1
                        # Add the data list to the data holders
                        self.data.append(data_list)
                        self.sex.append(data_list[0])
                        self.cdr.append(data_list[1])
                        self.spectra.append(data_list[2])
                
                elif parser == "2":
                    if filename.endswith(".csv"):
                        with open(path+"\\"+filename, "r") as file:
                            self.N += 1
                            csvreader = csv.reader(file)
                            raw_data = np.array([row for row in csvreader])
                        # Set each data entry with the right default values
                        n = len(raw_data)-3
                        data_list = ["O", -1, np.zeros((n,2))]
                        # Look for sample sex
                        sex_search = re.search(sex_finder, filename)
                        if sex_search:
                            data_list[0] = sex_search.group(1)
                        # Look for sample CDR
                        cdr_search = re.search(cdr_finder, filename)
                        if cdr_search:
                            # Check for non-integer CDR values
                            cdr_str = cdr_search.group(1)
                            if len(cdr_str) == 1:
                                data_list[1] = int(cdr_search.group(1))
                            elif len(cdr_str) > 1:
                                first_digit = int(cdr_str[0])
                                second_digit = int(cdr_str[2])
                                data_list[1] = first_digit + 0.1*second_digit
                        # Fill in the m/z values and counts
                        for i in range(n):
                            data_list[2][i,0] = float(raw_data[i+3][28])
                            data_list[2][i,1] = float(raw_data[i+3][36]) #51 is vol
                        # Add the data list to the data holders
                        self.data.append(data_list)
                        self.sex.append(data_list[0])
                        self.cdr.append(data_list[1])
                        self.spectra.append(data_list[2])
                            
                else:
                    raise ValueError("Parser", parser, "is not a valid parser")
        self.sex = np.array(self.sex)
        self.cdr = np.array(self.cdr)
    
    
    def bin_data(self, mz_bins, thresh=1.0, method="sum", normalize=None, 
                 tracking=False):
        """Returns an array of the MS counts for each bin. The method 
        parameter determines if the counts are summed or averaged. If 
        a spectrum has a value that does not fall into any bin, that 
        value is discarded. Optionally, takes bins above a certain 
        threshold for count numbers and sets them to zero.
        
        Parameters: 
            mz_bins (list): The m/z values that delimit the m/z bins. 
                The bins are intervals of the form [i, i+1).
            thresh (float): A number in (0,1]. Assuming that low-abundance 
                molecules are the most interesting, any m/z peaks with 
                abundance strictly greater than the threshold value times 
                the maximum abundance value for a given spectrum are not  
                counted for binning.
            method (str): Available values are "sum" and "mean".
            normalize (str, None): If None, bins are not normalized. 
                If "scale_ind", each spectrum is scaled to have a 
                maximum value of 1. If "scale_all", each spectrum is 
                scaled by the same amount such that the maximum value 
                across all spectra is 1. If "norm", then each spectrum 
                is scaled to have a Euclidean norm of 1.
            tracking (bool): Whether or not to print checkpoints. 
                Checkpoints include, but are not limited to, when a 
                value is discarded.
        
        Returns:
            binned_counts (nd-array): An Nxm array of the MS counts for 
                each bin, where N is the number of spectra and m is the 
                number of bins."""
        # Determine the counts for each bin in each spectrum
        binned_counts = np.zeros((self.N, len(mz_bins)-1))
        for i in range(self.N):
            num_peaks = len(self.spectra[i])
            # Track number of peaks per bin if method is by means
            if method == "mean":
                peak_count = np.zeros(len(mz_bins)-1)
            # Get the maximum value for the spectrum for thresholding
            max_counts = np.max([self.spectra[i][j][1] for j in range(num_peaks)])
            for j in range(num_peaks):
                included = False
                # Skip values above the threshold
                if self.spectra[i][j][1] > thresh*max_counts:
                    continue
                mz_val = self.spectra[i][j][0]
                for k in range(len(mz_bins)-1):
                    if mz_val >= mz_bins[k] and mz_val < mz_bins[k+1]:
                        binned_counts[i,k] += self.spectra[i][j][1]
                        included = True
                        # Determine counts for each bin
                        if method == "mean":
                            peak_count[k] += 1
                            binned_counts[i,k] += self.spectra[i][j][1]
                        elif method == "sum":
                            binned_counts[i,k] += self.spectra[i][j][1]
                        else:
                            raise ValueError(method + "is not a valid method.")
                        break
                if not included:
                    if tracking:
                        print("M/Z value at position " + str(j) + \
                              " of spectrum at index " + str(i) + \
                              " discarded for not being in a bin.")
            # If method is by means, divide by peak count per bin
            if method == "mean":
                for k in range(len(mz_bins)-1):
                    if peak_count[k] != 0:
                        binned_counts[i,k] /= peak_count[k]
        # Normalize data
        if normalize is None:
            pass
        elif normalize == "scale_ind":
            binned_counts /= np.max(binned_counts, axis=1)
        elif normalize == "scale_all":
            binned_counts /= np.max(binned_counts)
        elif normalize == "norm":
            binned_counts /= np.array([la.norm(binned_counts, axis=1)]).T
        else:
            raise ValueError("Input", normalize, "is not a valid normalization method.")
        return binned_counts
    
    
    def plot_bins(self, mz_bins, spectra=None, thresh=1.0, N_labels=None, method="sum", 
                  normalize=None, tracking=False):
        """Plots a graph of the binned data. If spectra is None, then 
        all of the spectra are plotted. If spectra is a list, then all 
        of the spectra in the list are plotted. The spectra argument 
        must be a list or None. If N_labels is None, then the x-axis is 
        labeled from 0 to 100. Otherwise, a number of labels equal to 
        N_labels is generated based on the data. See bin_data docstring 
        for more detailed information."""
        # Get the binned data
        binned_data = self.bin_data(mz_bins, thresh, method, normalize, tracking)
        # Plot the data
        if spectra is None:
            spectra = np.arange(self.N)
        subplot_dim = np.ceil(np.sqrt(len(spectra)))
        for i in spectra:
            plt.subplot(subplot_dim, subplot_dim, i+1)
            plt.title("Spectrum {}, {}, {}".format(i, self.sex[i], self.cdr[i]))
            plt.bar(np.arange(len(mz_bins)-1), binned_data[i])
            if N_labels is not None:
                labels = [np.round(mz_bins[int(i*len(mz_bins)/N_labels)],2) for i in range(N_labels)]
                plt.xticks(np.linspace(0,len(binned_data[i]),N_labels), labels, rotation="vertical")
            # Scale the y-axis as necessary
            if normalize == "scale_ind" or normalize == "scale_all":
                plt.ylim([0,1])
        plt.show()
    
    
    def PCA(self, mz_bins, d=2, thresh=1.0, sex_segregate=None, method="sum", 
            normalize=None, tracking=False):
        """Project the binned spectra into a d-dimensional space 
        spanned by the first d principal components of the data. 
        Returns an Nxd array of projected data. If sex_segregate 
        is "M" or "F", only male or female data, respectively, are 
        considered. See the bin_data docstring for more detailed 
        information."""
        # Get the data
        data = self.bin_data(mz_bins, thresh, method, normalize, tracking)
        if sex_segregate == "M":
            data = data[self.sex == "M"]
        elif sex_segregate == "F":
            data = data[self.sex == "F"]
        # Center the data
        means = np.mean(data, axis=0)
        data -= means
        # Get the svd of the data
        U, S, Vt = la.svd(data)
        # Project onto the principal component space
        projected_data = data.dot(Vt.T[:,:d])
        return projected_data
    
    
    def plot_PCA(self, mz_bins, d=2, thresh=1.0, sex_segregate=None, labels=None, 
                 method="sum", normalize=None, tracking=False):
        """Plot the binned spectra as projected into 2D or 3D space 
        by the PCA function. The data can be labeled by sex, by CDR, 
        by both, or by neither. Allowed values for d are 2 and 3. 
        Allowed values for labels are "sex", "cdr", "both", and None. 
        If sex_segregate="M", then the plot only includes male data. 
        The reverse is true if sex_segregate="F". See the bin_data 
        docstring for more detailed information."""
        # Check for allowed dimensionality
        if d > 3:
            raise ValueError("Cannot plot data with more than 3 dimensions.")
        elif d < 2:
            raise ValueError("Cannot plot data with fewer than 2 dimensions.")
        # Get the projected data
        data = self.PCA(mz_bins, d, thresh, sex_segregate, method, normalize, tracking)
        # Change titles based on segregation
        if sex_segregate == "F":
            mask = self.sex == "F"
            #data = data[mask]
            title = "PCA Analysis, Female, Threshold = {}".format(thresh)
        elif sex_segregate == "M":
            mask = self.sex == "M"
            #data = data[mask]
            title = "PCA Analysis, Male, Threshold = {}".format(thresh)
        else:
            mask = self.sex != "Z"
            title = "PCA Analysis, Threshold = {}".format(thresh)
        
        # Plot the data if 2-D
        if d == 2:
            # Plot based on labels
            if labels == "sex":
                mask_female = self.sex[mask] == "F"
                mask_male = self.sex[mask] == "M"
                mask_other = self.sex[mask] == "O"
                plt.scatter(data[mask_female,0], data[mask_female,1], label="Female")
                plt.scatter(data[mask_male,0], data[mask_male,1], label="Male")
                plt.scatter(data[mask_other,0], data[mask_other,1], label="Other")
                plt.legend()
            elif labels == "cdr":
                cdr_masks = [self.cdr[mask] == cdr for cdr in range(5)]
                for i in range(5):
                    plt.scatter(data[cdr_masks[i],0], data[cdr_masks[i],1], label="CDR: "+str(i))
                plt.legend()
            elif labels == "both":
                # Make sure that there are enough colors to uniquely label each label
                colors = [np.array(color) for color in perm([0,255,85,170],3)]
                cdr_masks_female = [(self.cdr[mask] == cdr)*(self.sex[mask] == "F") for cdr in range(5)]
                cdr_masks_male = [(self.cdr[mask] == cdr)*(self.sex[mask] == "M") for cdr in range(5)]
                cdr_masks_other = [(self.cdr[mask] == cdr)*(self.sex[mask] == "O") for cdr in range(5)]
                # Iterate through the colors, too
                j = 0
                for i in range(5):
                    plt.scatter(data[cdr_masks_female[i],0], data[cdr_masks_female[i],1], color=[colors[j]/255.], label="Female, CDR: "+str(i))
                    j += 1
                    plt.scatter(data[cdr_masks_male[i],0], data[cdr_masks_male[i],1], color=[colors[j]/255.], label="Male, CDR: "+str(i))
                    j += 1
                    plt.scatter(data[cdr_masks_other[i],0], data[cdr_masks_other[i],1], color=[colors[j]/255.], label="Other, CDR: "+str(i))
                    j += 1
                plt.legend()
            else:
                plt.scatter(data[:,0], data[:,1])
            plt.title(title)
            plt.xlabel("Principal Component 1")
            plt.ylabel("Principal Component 2")
            plt.show()
        
        # Plot the data if 3-D
        if d == 3:
            # Set up the axes
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")
            # Plot based on labels
            if labels == "sex":
                mask_female = self.sex[mask] == "F"
                mask_male = self.sex[mask] == "M"
                mask_other = self.sex[mask] == "O"
                ax.scatter(data[mask_female,0], data[mask_female,1], data[mask_female,2], label="Female")
                ax.scatter(data[mask_male,0], data[mask_male,1], data[mask_male,2], label="Male")
                ax.scatter(data[mask_other,0], data[mask_other,1], data[mask_other,2], label="Other")
                plt.legend()
            elif labels == "cdr":
                cdr_set = set(self.cdr)
                cdr_masks = [self.cdr[mask] == cdr for cdr in cdr_set]
                for i, cdr in enumerate(cdr_set):
                    ax.scatter(data[cdr_masks[i],0], data[cdr_masks[i],1], data[cdr_masks[i],2], label="CDR: "+str(cdr))
                plt.legend()
            elif labels == "both":
                # Make sure that there are enough colors to uniquely label each label
                colors = [np.array(color) for color in perm([0,255,85,170],3)]
                cdr_masks_female = [(self.cdr[mask] == cdr)*(self.sex[mask] == "F") for cdr in range(5)]
                cdr_masks_male = [(self.cdr[mask] == cdr)*(self.sex[mask] == "M") for cdr in range(5)]
                cdr_masks_other = [(self.cdr[mask] == cdr)*(self.sex[mask] == "O") for cdr in range(5)]
                # Iterate through the colors, too
                j = 0
                for i in range(5):
                    ax.scatter(data[cdr_masks_female[i],0], data[cdr_masks_female[i],1], data[cdr_masks_female[i],2], color=[colors[j]/255.], label="Female, CDR: "+str(i))
                    j += 1
                    ax.scatter(data[cdr_masks_male[i],0], data[cdr_masks_male[i],1], data[cdr_masks_male[i],2], color=[colors[j]/255.], label="Male, CDR: "+str(i))
                    j += 1
                    ax.scatter(data[cdr_masks_other[i],0], data[cdr_masks_other[i],1], data[cdr_masks_other[i],2], color=[colors[j]/255.], label="Other, CDR: "+str(i))
                    j += 1
                plt.legend()
            else:
                ax.scatter(data[:,0], data[:,1], data[:,2])
            plt.title(title)
            ax.set_xlabel("Principal Component 1")
            ax.set_ylabel("Principal Component 2")
            ax.set_zlabel("Principal Component 3")
            plt.show()



class LC_MSData():
    """A data structure containing an array with rows of the form 
    [RT-start, RT-end, datapoints], where datapoints is a list of 
    tuples of the form (m/z, counts). In other words, this holds 
    a list of mass spectra along with the RT-interval over which 
    each spectrum was taken. 
    
    Initializes with the name of a datafile in .csv format. The 
    parser argument indicates in which style the data in the file 
    are organized so that the data can be properly parsed.
    
    RT is retention time in minutes.
    
    Parameters:
        N (int): The number of spectra.
        data (array): A length N array with rows of the form 
            (RT-start, RT-end, RT-peak, datapoints), where datapoints 
            is a list of tuples of the form (m/z, counts). For example, 
            typing data[0][1] will give the final RT of the first 
            interval, and data[0][2] will give the list of m/z 
            values and associated counts for the first spectrum.
        RT_start (array): A length N array of initial RT values. 
            For example, RT_start[10] gives the initial RT value of 
            the spectrum at index 10.
        RT_end (array): A length N array of final RT values. For 
            example, RT_start[10] gives the final RT value of the 
            spectrum at index 10.
        RT_peak (array): A length N array of peak RT values. For 
            example, RT_peak[10] gives the peak RT value of the 
            spectrum at index 10.
        spectra (array): A length N array of MS spectra. Each 
            spectrum consists of (m/z, counts) tuples. For example, 
            spectra[0][10] gives the (m/z, counts) tuple at index 10 
            of the first spectrum.
    
    Functions:
        bin_data(mz_bins, RT_bins, method): Returns an array of the 
            MS counts for each bin. The method parameter determines 
            if the counts are summed or averaged.
        plot_bins(mz_bins, RT_bins, N_labels, method): Plots a graph 
            of the binned data.: 
        """
    
    
    def __init__(self, filename, parser="1"):
        # Read in the file
        with open(filename, "r") as file:
            csvreader = csv.reader(file)
            raw_data = np.array([row for row in csvreader])
        data = []
        
        # Search for the useable data the right way
        if parser == "1":
            # Set up regexes to determine retention time windows and peaks
            RT_window_getter = re.compile(r"rt: (\d+\.\d\d\d)-(\d+\.\d\d\d)")
            RT_peak_getter = re.compile(r"Cpd \d+: (\d+\.\d\d\d)")
            for row in raw_data:
                if row[0][0] == "#":
                    search = re.search(RT_window_getter, row[0])
                    # If a new RT is found, add another row to data
                    if search:
                        peak = float(re.search(RT_peak_getter, row[0]).group(1))
                        data.append(np.array([float(search.group(1)), 
                                              float(search.group(2)), 
                                              peak, 
                                              []]))
                # If the row contains m/z values instead of RT values, add the mz values to the last row of data
                else:
                    data[-1][3].append((float(row[1]), float(row[2])))
        
        elif parser == "2":
            # Skip the headers
            for row in raw_data[3:]:
                # This format gives only one peak per feature, all nicely organized by row
                data.append(np.array([float(row[50]), 
                                      float(row[33]), 
                                      float(row[48]), 
                                      [(float(row[28]), float(row[36]))]]))
        
        else:
            raise ValueError("Parser {} is not a recognized parsing method.".format(parser))
        # Fill in the different data holders
        self.data = np.array(data)
        self.N = len(data)
        self.RT_start = self.data[:,0]
        self.RT_end = self.data[:,1]
        self.RT_peak = self.data[:,2]
        self.spectra = self.data[:,3]
    
    
    def bin_data(self, mz_bins, RT_bins, flat=True, thresh=1.0, method="sum", normalize=None, tracking=False):
        """Returns an array of the MS counts for each bin. The method 
        parameter determines if the counts are summed or averaged. If 
        a spectrum has a value that does not fall into any bin, that 
        value is discarded.
        
        Parameters: 
            mz_bins (list): The m/z values that delimit the m/z bins. 
                The bins are intervals of the form [i, i+1). 
            RT_bins (list): The RT values that delimit the RT bins. 
                The bins are intervals of the same form as the m/z 
                bins.
            flat (bool): If true, returns a 1D array of bins. If false, 
                returns a 2D array where rows are RT bins and columns 
                are mz bins.
            thresh (float): A number in (0,1]. Assuming that low-abundance 
                molecules are the most interesting, any m/z peaks with 
                abundance strictly greater than the threshold value times 
                the maximum abundance value for a given spectrum are not  
                counted for binning.
            method (str): Available values are "sum" and "mean".
            normalize (str, None): If None, bins are not normalized. 
                If "scale_ind", each RT bin is scaled to have a 
                maximum value of 1. If "scale_all", each RT bin is 
                scaled by the same amount such that the maximum value 
                across all bins is 1. If "norm", then each RT bin is 
                scaled to have a Euclidean norm of 1. If "norm" and 
                flat=True, then the flattened vector is normalized.
            tracking (bool): Whether or not to print checkpoints. 
                Checkpoints include, but are not limited to, when a 
                value is discarded."""
        
        # Get the maximum value for the spectrum for thresholding
        max_counts = np.max([np.max([self.spectra[i][j][1] for j in range(len(self.spectra[i]))]) for i in range(self.N)])
        # Set up the framework for storing the counts for each bin
        binned_counts = np.zeros((len(RT_bins)-1, len(mz_bins)-1))
        if method == "mean":
            num_in_bin = np.full((len(RT_bins)-1, len(mz_bins)-1), np.inf)
        
        # Determine the RT bin for each spectrum
        RT_centers = self.RT_peak
        RT_bindex = np.zeros(self.N)
        if tracking:
            print("Working on RT bins")
        # Iterate over each spectrum
        for i in range(self.N):
            if tracking and i%(self.N//100 + 1) == 0:
                print("Spectrum {} of {}".format(i, self.N))
            included = False
            # Iterate over each RT bin
            for j in range(len(RT_bins)-1):
                if RT_centers[i] >= RT_bins[j] and RT_centers[i] < RT_bins[j+1]:
                    RT_bindex[i] = j
                    included = True
                    break
            if not included:
                RT_bindex[i] = -1
                if tracking:
                    print("Spectrum at index {} discarded for not being in a bin.".format(i))
        
        # Determine the m/z bin for each value in each spectrum and add the value to that bin
        mz_bindex = [[] for _ in range(self.N)]
        if tracking:
            print("Working on m/z bins")
        # Iterate over each spectrum
        for i in range(self.N):
            if tracking and i%(self.N//100 + 1) == 0:
                print("Spectrum {} of {}".format(i, self.N))
            # Iterate over each (m/z, counts) tuple
            for j in range(len(self.spectra[i])):
                included = False
                mz_val = self.spectra[i][j][0]
                counts = self.spectra[i][j][1]
                # Iterate over each potential m/z bin
                for k in range(len(mz_bins)-1):
                    if mz_val >= mz_bins[k] and mz_val < mz_bins[k+1]:
                        # Track the bin for each (m/z, counts) pair, just in case
                        mz_bindex[i].append(k)
                        # Add the counts to the appropriate bin aggregate if it meets the threshold criteria
                        if counts <= thresh*max_counts and RT_bindex[i] != -1:
                            if method == "sum":
                                binned_counts[int(RT_bindex[i]), k] += counts
                            elif method == "mean":
                                binned_counts[RT_bindex[i], k] += counts
                                # num_in_bin defaults to infinity to prevent division by zero errors
                                if num_in_bin[RT_bindex[i], k] == np.inf:
                                    num_in_bin[RT_bindex[i], k] = 0
                                num_in_bin[RT_bindex[i], k] += 1
                            else:
                                raise ValueError("{} is not a valid method.".format(method))
                        included = True
                        break
                if not included:
                    mz_bindex[i].append(-1)
                    if tracking:
                        print("M/Z value at position " + str(j) + \
                              " of spectrum at index " + str(i) + \
                              " discarded for not being in a bin.")
        mz_bindex = np.array(mz_bindex)
        # Divide if necessary for averaging
        if method == "mean":
            binned_counts /= num_in_bin
        
        # Normalize data
        if normalize is None:
            pass
        elif normalize == "scale_ind":
            for i in range(len(RT_bins)-1):
                binned_counts[i] /= np.max(binned_counts[i])
        elif normalize == "scale_all":
            scale = np.max(binned_counts)
            for i in range(len(RT_bins)-1):
                binned_counts[i] /= scale
        elif normalize == "norm" and not flat:
            for i in range(len(RT_bins)-1):
                binned_counts[i] /= la.norm(binned_counts[i])
        elif normalize == "norm" and flat:
            pass
        else:
            raise ValueError("Input", normalize, "is not a valid normalization method.")
        if flat:
            binned_counts = np.ravel(binned_counts)
            if normalize == "norm":
                binned_counts /= la.norm(binned_counts)
        return binned_counts
    
    
    def plot_bins(self, mz_bins, RT_bins, thresh=1.0, N_labels=None, method="sum", normalize=None, tracking=False):
        """Plots a graph of the unflattened binned data. If N_labels 
        is None, then the x-axis is labeled from 0 to 100. Otherwise, 
        a number of labels equal to N_labels is generated based on the 
        data. See bin_data docstring for more detailed information."""
        # Get the binned data
        binned_data = self.bin_data(mz_bins, RT_bins, flat=True, thresh=thresh, method=method, normalize=normalize, tracking=tracking)
        # Plot the data
        subplot_dim = np.ceil(np.sqrt(len(RT_bins)-1))
        for i in range(len(RT_bins)-1):
            plt.subplot(subplot_dim, subplot_dim, i+1)
            plt.title("RT bin:{} to {} min.".format(RT_bins[i], RT_bins[i+1]))
            plt.bar(np.arange(len(mz_bins)-1), binned_data[i])
            if N_labels is not None:
                labels = [np.round(mz_bins[int(i*len(mz_bins)/N_labels)],2) for i in range(N_labels)]
                plt.xticks(np.linspace(0,len(binned_data[i]),N_labels), labels, rotation="vertical")
        plt.show()
    
    
    def plot_diffs(self, mz_bins, RT_bins, method="sum", normalize=None, tracking=False):
        # Get the binned data
        binned_data = self.bin_data(mz_bins, RT_bins, False, method, normalize, tracking)
        RT_len = len(RT_bins)-1
        for i in range(RT_len):
            for j in range(RT_len):
                plt.subplot(RT_len, RT_len, 1+RT_len*i+j)
                diff_ij = binned_data[i]-binned_data[j]
                plt.plot(diff_ij/binned_data[i])
                plt.title("RT bins {} and {}".format(i,j))
        plt.show()



def LC_MS_getter(path="C:\\Research\Data", parser="1", more_info=False, tracking=False):
    """Takes the name "path" of a directory and returns a list of LC_MSData 
    objects created from all of the .csv files in the path. The "parser" 
    argument indicates the structure of the stored data to make sure that the 
    files are parsed correctly. If more_info=True, then two additional lists 
    are returned. The first of the new lists contains floats representing the 
    CDR (Clinical Dementia Rating) of each sample. The second contains the sex 
    of each patient contributing the samples. Note that the method for extracting 
    this information depends on the parser."""
    # Initialize the list for storing data
    LCMS_list = []
    # If specified, make regexes and lists for extracting data from file names
    if more_info:
        cdr_finder = re.compile(r"\d*[_ ]+\w([0-4]{1,2}) ")
        sex_finder = re.compile(r"\d*[_ ]+(M|F)\d* ")
        cdr = []
        sex = []
    # Get the path from which the files are to be taken
    directory = os.path.abspath(path)
    # Get and parse all of the files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if tracking:
                print(filename)
            if filename.endswith(".csv") or filename.endswith(".CSV"):
                # Add the data to the list
                LCMS_list.append(LC_MSData(path+"\\"+filename, parser=parser))
                # If specified, get the sex and CDR corresponding to each sample
                if more_info:
                    if parser == "1" or parser == "2":
                        # Look for sample cdr
                        cdr_search = re.search(cdr_finder, filename)
                        if cdr_search:
                            # Check for non-integer CDR values
                            cdr_str = cdr_search.group(1)
                            if len(cdr_str) == 1:
                                cdr.append(float(cdr_search.group(1)))
                            elif len(cdr_str) > 1:
                                first_digit = int(cdr_str[0])
                                second_digit = int(cdr_str[2])
                                cdr.append(first_digit + 0.1*second_digit)
                            else:
                                cdr.append(-1)
                        # Append -1 if no CDR is found
                        else:
                            cdr.append(-1)
                        # Look for sample sex
                        sex_search = re.search(sex_finder, filename)
                        if sex_search:
                            sex.append(sex_search.group(1))
                        # Append "O" for "Other" if no sex is found
                        else:
                            sex.append("O")
                    else:
                        raise ValueError("Parser {} is not a valid parser".format(parse))
    # Return the data as appropriate
    if more_info:
        return LCMS_list, cdr, sex
    return LCMS_list



def LC_MS_binner(data, mz_bins, RT_bins, thresh=1.0, method="sum", normalize=None, tracking=False):
    """Returns an n-darray of the binned data from each LC_MSData object in "data"."""
    N = len(data)
    r = len(RT_bins)-1
    m = len(mz_bins)-1
    binned_data = np.zeros((N, r*m))
    for i in range(N):
        if tracking:
            print(i)
        binned_data[i] = data[i].bin_data(mz_bins, RT_bins, True, thresh, method, normalize, tracking)
    return binned_data



def LC_MS_PCA(data, d, mz_bins, RT_bins, thresh=1.0, method="sum", normalize=None, 
              pre_binned=False, get_V=False, tracking=False):
    """Does PCA on a given set of LC_MSData objects. Uses sparse matrices for SVD.
    If "pre_binned" is True, then assumes that "data" is a numpy array. If "get_V" 
    is true, then the projection matrix Vt is also returned.
    Parameters:
        data (list): A list of LC_MSData objects
        d (int): The number of principal components to use"""
    # Get the useful information out of the data
    if pre_binned:
        binned_data = data
    else:
        binned_data = LC_MS_binner(data, mz_bins, RT_bins, thresh, method, normalize, tracking)
    # Center the data
    means = np.mean(binned_data, axis=0)
    binned_data -= means
    # Sparsify
    sparse_data = csr_matrix(binned_data)
    # Get the svd of the data
    if tracking:
        print("SVD")
    U, S, Vt = spla.svds(sparse_data)
    if tracking:
        print("Shape of U:",U.shape)
        print("Shape of S:",S.shape)
        print("Shape of Vt:",Vt.shape)
    # Project onto the principal component space
    if tracking:
        print("Projecting")
    projected_data = binned_data.dot(Vt.T[:,:d])
    if get_V:
        return projected_data, Vt
    return projected_data



def LC_MS_kPCA(data, labels, mz_bins, RT_bins, thresh=1.0, method="sum", classifier="RF", normalize=None, tracking=False):
    """Bins the given LC_MSData objects in "data", then uses a parameter 
    gridsearch to find the best hyperparameters for kPCA and the given 
    classifier to predict the labels of the data. Returns the best 
    hyperparameters for the kPCA and the classifier.
    Supported classifiers are "RF" for Random Forest, and more to come."""
    raise NotImplementedError("I haven't finished this one yet...")
    # Get the useful information out of the data
    N = len(data)
    r = len(RT_bins)-1
    m = len(mz_bins)-1
    binned_data = np.zeros((N, r*m))
    for i in range(N):
        if tracking:
            print(i)
        binned_data[i] = data[i].bin_data(mz_bins, RT_bins, True, thresh, method, normalize, tracking)