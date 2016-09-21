## The BrainIAK-SRM BIDS App
This is the BIDS-app version of the Shared Response Model (SRM)
implemented in [Brain Imaging Analysis Toolkit (BrainIAK)](https://github.com/IntelPNI/brainiak).

### Description
The Shared Response Model (SRM) is a method for aligning fMRI scans from several subjects by assuming
similar functional behavior in the brain. The voxels of each subject are mapped to voxels of other subjects
by projecting the information for each subject into a shared subspace. It is originally implemented
in Python as part of BrainIAK.

### Documentation
http://pythonhosted.org/brainiak/brainiak.funcalign.html

### How to report errors
Please go to BrainIAK git [repo](https://github.com/IntelPNI/brainiak) to report errors.
We also welcome any kind of contribution to BrainIAK, details can be found
[here](https://github.com/IntelPNI/brainiak/blob/master/CONTRIBUTING.rst)

### Acknowledgements
Please cite the following papers based on which SRM is implemented.
Chen et al. 2015.
[A Reduced-Dimension fMRI Shared Response Model](http://papers.nips.cc/paper/5855-a-reduced-dimension-fmri-shared-response-model)

Anderson et al. 2016.
[Enabling Factor Analysis on Thousand-Subject Neuroimaging Datasets](https://arxiv.org/abs/1608.04647)

### Usage
This App has the following command line arguments:

		usage: run.py [-h]
		              [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
		              bids_dir output_dir {participant,group}

		Example BIDS App entry point script.

		positional arguments:
		  bids_dir              The directory with the input dataset formatted
		                        according to the BIDS standard.
		  output_dir            The directory where the output files should be stored.
		                        If you are running a group level analysis, this folder
		                        should be prepopulated with the results of
		                        the participant level analysis.
		  {participant,group}   Level of the analysis that will be performed. Multiple
		                        participant level analyses can be run independently
		                        (in parallel).

		optional arguments:
		  -h, --help            show this help message and exit
		  --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
		                        The label(s) of the participant(s) that should be
		                        analyzed. The label corresponds to
		                        sub-<participant_label> from the BIDS spec (so it does
		                        not include "sub-"). If this parameter is not provided
		                        all subjects will be analyzed. Multiple participants
		                        can be specified with a space separated list.

To run it in participant level mode (for one participant):

    docker run -i --rm \
		-v /Users/filo/data/ds005:/bids_dataset:ro \
		-v /Users/filo/outputs:/outputs \
		bids/example \
		/bids_dataset /outputs participant --participant_label 01

After doing this for all subjects (potentially in parallel), the group level analysis
can be run:

    docker run -i --rm \
		-v /Users/filo/data/ds005:/bids_dataset:ro \
		-v /Users/filo/outputs:/outputs \
		bids/example \
		/bids_dataset /outputs group

### Special considerations
TBD
