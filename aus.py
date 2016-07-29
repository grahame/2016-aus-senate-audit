# aus.py
# July 27, 2016
# python3
# code sketches for AUS senate audit by Bayesian audit method

import copy
import random
import os
import dividebatur.dividebatur.senatecount as sc
from  dividebatur.dividebatur.counter import Ticket
# random.seed(1)    # make deterministic

class Election:
    pass

class RealElection(Election):

    def __init__(self,sample_size=None):
        self.sample_size = sample_size
        self.set_data_from_config()
        self.prior_ballots = [ (c,) for c in self.candidates ]
      

    def set_data_from_config(self):
        config_file = './dividebatur/aec_data/fed2016/aec_fed2016.json'
        self.out_dir = './dividebatur/angular/data/'

        self.base_dir = os.path.dirname(os.path.abspath(config_file))
        config = sc.read_config(config_file)
        # global config for the angular frontend
        sc.cleanup_json(self.out_dir)
        sc.write_angular_json(config, self.out_dir)
        method_cls = sc.get_counting_method(config['method'])
        sc.counting_method_valid(method_cls)
        written = set()
        self.count = config['count'][0]
        try:
            del self.count['verified']
        except KeyError:
            pass
        s282_candidates = sc.s282_recount_get_candidates(self.out_dir, self.count, written)
        self.data = sc.get_data(method_cls, self.base_dir, self.count, s282_candidates=s282_candidates)
        self.candidates = self.data.get_candidate_ids()
        self.ballots = []
        for paper in self.data.tickets_for_count.papers:
            if self.sample_size  is not None and self.sample_size <= len(self.ballots):
                break
            self.ballots += paper.preference_flows

        random.shuffle(self.ballots)
        self.ballots = self.ballots[:sample_size]
        

    #Add ballot from tuple?
    #return Ticket((PreferenceFlow(tuple(prefs)), ))

    def get_candidates(self ):
        return self.candidates

    def draw_ballots(self, k):
        """ 
        return list of up to k paper ballots 
        """
        random.shuffle(self.ballots)
        sample = self.ballots[:k]
        return sample
        

    def scf(self, sample):
        """ Return result of scf (social choice function) on this sample. """
        ### call Bowland's code here
        pass 


class SimulatedElection(Election):

    def __init__(self, m, n):
        self.m = m                                 # number of candidates
        self.candidates = list(range(1,self.m+1))
        self.n = n                                 # number of cast ballots
        self.prior_ballots = [ (c,) for c in self.candidates ]

    def draw_ballots(self, k):
        """ 
        return list of up to k simulated ballots for testing purposes 
        or [] if no more ballots available
        """
        if random.random()<0.01:
            return []
        ballots = []
        for _ in range(k):
            ballot = list(self.candidates[:])
            random.shuffle(ballot)
            ballots.append(ballot)
        return ballots
    
    def scf(self, sample):
        """ Return result of scf (social choice function) on this sample. """
        # TBD
        return tuple(self.candidates)

##############################################################################
# A ballot is an abstract blob.
# Here implemented as a tuple.
# The only operations we need on ballots are:
#    -- obtaining them from election data
#    -- putting them into a list
#    -- copying one of them
#    -- making up a list of "prior ballots" expressing
#       our Bayesian prior

def copy_ballot(b):
    return copy.deepcopy(b)


##############################################################################
# Implementation of polya's urn

def urn(election, sample, r):
    """ 
    Return list of length r generated from sample and prior ballots 
    Don't return prior ballots, but sample is part of returned result.
    It may be possible to optimize this code using gamma variates.
    """
    L = election.prior_ballots + sample
    for _ in range(r-len(sample)):
        L.append(copy_ballot(random.choice(L)))
    return L[len(election.prior_ballots):]

def test_urn(election):
    k = 5
    r = 10
    print("test_urn",k, r)
    sample = election.draw_ballots(k)
    print(urn(election, sample, r))

#test_urn(SimulatedElection(3,36))

##############################################################################
# Implementation of audit

def audit(election):
    """ Bayesian audit of given election """

    print("audit")

    # get basic election info
    candidates = election.candidates
    n = election.n               

    # control parameters
    alpha = 0.05          # error tolerance
    k = 4                 # amount to increase sample size by
    trials = 20           # per sample

    # overall audit loop
    sample = []
    while True:

        sample_increment = election.draw_ballots(k)
        if sample_increment is None:
            print("Audit has looked at all ballots. Done.")
            break
        sample.extend(sample_increment)
        print("sample is:", sample)

        # run trials in Bayesian manner
        outcomes = []
        for t in range(trials):
            full_urn = urn(election, sample, n)
            outcomes.append(election.scf(full_urn))

        # figure out whether to stop or not based on outcomes
        # fake it for now
        if random.random()<(float(len(sample))/float(n)):
            print("Audit confirms outcome; stop.")
            break
        # TBD: stop if some outcome happened more than trials*(1-alpha) times

audit(SimulatedElection(4,100))

          
        
    
