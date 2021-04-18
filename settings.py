import argparse
import parameter

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='PG-GAN entry point')

    parser.add_argument('-m', '--model', type=str, \
        help='exp, im, ooa2, ooa3', required=True)
    parser.add_argument('-p', '--params', type=str, \
        help='comma separated parameter list', required=True)
    parser.add_argument('-d', '--data_h5', type=str, help='real data file')
    parser.add_argument('-b', '--bed', type=str, help='bed file (mask)')
    parser.add_argument('-r', '--reco_folder', type=str, \
        help='recombination maps')
    parser.add_argument('-g', action="store_true", dest="grid",help='grid search')
    parser.add_argument('-t', action="store_true", dest="toy", help='toy example')
    parser.add_argument('-s', '--seed', type=int, default=1833, \
        help='seed for RNG')

    return parser.parse_args()

def parse_params(param_input):
    """See which params were desired for inference"""
    param_strs = param_input.split(',')
    parameters = []
    for _, p in vars(parameter.ParamSet()).items():
        if p.name in param_strs:
            parameters.append(p)

    assert len(parameters) == len(param_strs)
    for p in parameters:
        print(p)

    return parameters
