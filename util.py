"""
Utility functions and classes (including default parameters).
Author: Sara Mathieson
Date: 2/4/21
"""

import numpy as np
import sys

def process_gt_dist(gt_matrix, dist_vec, S, filter=False, rate=None, neg1=True):
    """
    Take in a genotype matrix and vector of inter-SNP distances. Return a 3D
    numpy array of the given n (haps) and S (SNPs) and 2 channels.
    Filter singletons at given rate if filter=True
    """
    if filter:
        # mask
        singleton_mask = np.array([filter_func(row, rate) for row in gt_matrix])

        # reassign
        gt_matrix = gt_matrix[singleton_mask]
        dist_vec = np.array(dist_vec)[singleton_mask]

    num_SNPs = gt_matrix.shape[0] # SNPs x n
    n = gt_matrix.shape[1]
    if S == None:
        S = num_SNPs # for region_len fixed

    # double check
    if num_SNPs != len(dist_vec):
        print("gt", num_SNPs, "dist", len(dist_vec))
    assert num_SNPs == len(dist_vec)

    # set up region
    region = np.zeros((n, S, 2), dtype=np.float32)

    mid = num_SNPs//2
    half_S = S//2
    if S % 2 == 1: # odd
        other_half_S = half_S+1
    else:
        other_half_S = half_S

    # enough SNPs, take middle portion
    if mid >= half_S:
        minor = major_minor(gt_matrix[mid-half_S:mid+ \
            other_half_S,:].transpose(), neg1)
        region[:,:,0] = minor
        distances = np.vstack([np.copy(dist_vec[mid-half_S:mid+other_half_S]) \
            for k in range(n)])
        region[:,:,1] = distances

    # not enough SNPs, need to center-pad
    else:
        print("NOT ENOUGH SNPS", num_SNPs)
        print(num_SNPs, S, mid, half_S)
        minor = major_minor(gt_matrix.transpose(), neg1)
        region[:,half_S-mid:half_S-mid+num_SNPs,0] = minor
        distances = np.vstack([np.copy(dist_vec) for k in range(n)])
        region[:,half_S-mid:half_S-mid+num_SNPs,1] = distances

    return region # n X SNPs X 2

def major_minor(matrix, neg1):
    """Note that matrix.shape[1] may not be S if we don't have enough SNPs"""
    n = matrix.shape[0]
    for j in range(matrix.shape[1]):
        if np.count_nonzero(matrix[:,j] > 0) > (n/2): # count the 1's
            matrix[:,j] = 1 - matrix[:,j]

    # option to convert from 0/1 to -1/+1
    if neg1:
        matrix[matrix == 0] = -1
    # residual numbers higher than one may remain even though we restricted to
    # biallelic
    #matrix[matrix > 1] = 1 # removing since we filter in VCF
    return matrix

def parse_hapmap_empirical_prior(files):
    """
    Parse recombination maps to create a distribution of recombintion rates to
    use for real data simulations. Based on defiNETti software package.
    """
    print("Parsing HapMap recombination rates...")

    # set up weights (probabilities) and reco rates
    weights_all = []
    prior_rates_all = []

    for f in files:
        mat = np.loadtxt(f, skiprows = 1, usecols=(1,2))
        #print(mat.shape)
        mat[:,1] = mat[:,1]*(1.e-8)
        mat = mat[mat[:,1] != 0.0, :] # remove 0s
        weights = mat[1:,0] - mat[:-1,0]
        prior_rates = mat[:-1,1]

        weights_all.extend(weights)
        prior_rates_all.extend(prior_rates)

    # normalize
    prob = weights_all / np.sum(weights_all)

    # make smaller by a factor of 50 (collapse)
    indexes = list(range(len(prior_rates_all)))
    indexes.sort(key=prior_rates_all.__getitem__)

    prior_rates_all = [prior_rates_all[i] for i in indexes]
    prob = [prob[i] for i in indexes]

    new_rates = []
    new_weights = []

    collapse = 50
    for i in range(0,len(prior_rates_all),collapse):
        end = collapse
        if len(prior_rates_all)-i < collapse:
            end = len(prior_rates_all)-i
        new_rates.append(sum(prior_rates_all[i:i+end])/end) # average
        new_weights.append(sum(prob[i:i+end])) # sum

    new_rates = np.array(new_rates)
    new_weights = np.array(new_weights)

    return new_rates, new_weights

################################################################################
# UNUSED FUNCTIONS
################################################################################
# def filter_func(x, rate): # currently not used
#     """Keep non-singletons. If singleton, filter at given rate"""
#     # TODO since we haven't done major/minor yet, might want to add != n-1 too
#     if np.sum(x) != 1:
#         return True
#     return np.random.random() >= rate # keep (1-rate) of singletons


# def prep_real(gt, snp_start, snp_end, indv_start, indv_end):
#     """Slice out desired region and unravel haplotypes"""
#     region = gt[snp_start:snp_end, indv_start:indv_end, :]
#     both_haps = np.concatenate((region[:,:,0], region[:,:,1]), axis=1)
#     return both_haps

# def filter_nonseg(region):
#     """Filter out non-segregating sites in this region"""
#     nonseg0 = np.all(region == 0, axis=1) # row all 0
#     nonseg1 = np.all(region == 1, axis=1) # row all 1
#     keep0 = np.invert(nonseg0)
#     keep1 = np.invert(nonseg1)
#     filter = np.logical_and(keep0, keep1)
#     return filter

# def read_demo_file(filename, Ne):
#     """Read in a PSMC-like demography"""
#     demos = []
#     with open(filename, 'r') as demo_file:
#         for pop_params in demo_file:
#             time, pop = pop_params.strip().split()
#             demos.append(msprime.PopulationParametersChange(time=float(time) \
#                 * 4 * Ne, initial_size=float(pop) * Ne))
#     return demos

if __name__ == "__main__":
    # test major/minor and post-processing
    a = np.zeros((6,3))
    a[0,0] = 1
    a[1,0] = 1
    a[2,0] = 1
    a[3,0] = 1
    a[0,1] = 1
    a[1,1] = 1
    a[2,1] = 1
    a[4,2] = 1
    dist_vec = [0.3, 0.2, 0.4, 0.5, 0.1, 0.2]

    print(a)
    print(major_minor(a, neg1=True))

    process_gt_dist(a, dist_vec, 4, filter=True, rate=0.3)
