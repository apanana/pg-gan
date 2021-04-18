##Refactoring util.py:
(This is part of a larger refactoring to clean up some of the accumulated tech debt).

The util.py file contains multiple functionalities (some of which aren't used anywhere else in the project) that should be separated. 

#Locations where util is used:
~/Desktop/pg-gan $grep -r "util." *.py
pg_gan.py:    opts = util.parse_args()
pg_gan.py:    all_params = util.ParamSet()
pg_gan.py:    parameters = util.parse_params(opts.params, all_params) # desired params

real_data_random.py:            after = util.process_gt_dist(hap_data, dist_vec, len(dist_vec), \

simulation.py:            self.prior, self.weights = util.parse_hapmap_empirical_prior(files)
simulation.py:        sim_params = util.ParamSet()
simulation.py:        return util.process_gt_dist(gt_matrix, dist_vec, num_snps, filter=True,\
simulation.py:        return util.process_gt_dist(gt_matrix, dist_vec, num_snps, neg1=neg1)
simulation.py:    params = util.ParamSet()

summary_stats.py:    all_params = util.ParamSet()
summary_stats.py:    parameters = util.parse_params(opts.params, all_params) # desired params
summary_stats.py:    opts = util.parse_args()

##New files
#parameter.py:
parameter
paramset

#settings.py:
parse_args
A bunch of other stuff can go in here like the globals used in pg_gan.py and in summary_stats.py

#all_params:
~/Desktop/pg-gan $grep -r "all_params" *.py
pg_gan.py:    all_params = util.ParamSet()
pg_gan.py:    parameters = util.parse_params(opts.params, all_params) # desired params
summary_stats.py:    all_params = util.ParamSet()
summary_stats.py:    parameters = util.parse_params(opts.params, all_params) # desired params
util.py:def parse_params(param_input, all_params):
util.py:    for _, p in vars(all_params).items():

#parse_params
parse_params makes no sense right now

#other funcs:
process_gt_dist (real_data_random.py, simulation.py)
parse_hapmap_empirical_prior (simulation.py)
major_minor (only used in process_gt_dist)

#unused funcs:
filter_func
filter_nonseg
prep_real
read_demo_file
