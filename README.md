## BrainIAK-SRM BIDS app

Shared Response Model (SRM) from the
[Brain Imaging Analysis Kit (BrainIAK)](https://github.com/brainiak/brainiak).

### Description

The Shared Response Model (SRM) is a method for aligning fMRI scans from several
subjects by assuming similar functional behavior in the brain. The voxels of
each subject are mapped to voxels of other subjects by projecting the
information from each subject into a low-dimensional space.

### Documentation

http://brainiak.org/docs/brainiak.funcalign.html

### How to report errors

Open a GitHub issue in [BrainIAK](https://github.com/brainiak/brainiak) (if the
issue is about SRM) or here (if the issue is about this wrapper app). We also
welcome all kinds of
[contributions to BrainIAK](http://brainiak.org/docs/contributing.html).

### Acknowledgements

Please cite the following papers based on which SRM is implemented.

"A Reduced-Dimension fMRI Shared Response Model", P.-H. Chen, J. Chen, Y.
Yeshurun-Dishon, U. Hasson, J. Haxby, P. Ramadge, Advances in Neural Information
Processing Systems (NIPS), 2015.
http://papers.nips.cc/paper/5855-a-reduced-dimension-fmri-shared-response-model

"Enabling Factor Analysis on Thousand-Subject Neuroimaging Datasets", Michael J.
Anderson, Mihai Capotă, Javier S. Turek, Xia Zhu, Theodore L. Willke, Yida Wang,
Po-Hsuan Chen, Jeremy R. Manning, Peter J. Ramadge, Kenneth A. Norman, IEEE Big
Data, 2016. https://doi.org/10.1109/BigData.2016.7840719

### Usage

This App has the following command line arguments:

    usage: run.py [-h]
                  [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
                  [--run RUN] [--task TASK] [--preproc PREPROC] [--mask MASK]
                  [--iterations ITERATIONS] [--features FEATURES]
                  bids_dir output_dir {participant,group}

    Shared Response Model runner

    positional arguments:
      bids_dir              Input directory
      output_dir            Output directory
      {group}   Level of the analysis that will be performed

    optional arguments:
      -h, --help            show this help message and exit
      --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
                            Labels for participants to be analyzed (default: None)
      --run RUN             Run to be analyzed (default: 01)
      --task TASK           Task to be analyzed, default is any (default: *)
      --preproc PREPROC     Preprocessing tag, default is any (default: *)
      --mask MASK           Mask tag (default: bmask)
      --iterations ITERATIONS
                            Number of iterations, default is SRM default (default:
                            None)
      --features FEATURES   Number of features, default is SRM default (default:
                            None)

### Special considerations

This app requires preprocessed data with all volumes of a subject registered. It
also requires masks to be present in the input data; all to-be-analyzed volumes
of a subject must use the same mask.

SRM works only on group level because it is a method for aligning fMRI scans
from multiple subjects.

The data must be time-synchronized, i.e., all subjects must be presented with
the same stimuli with the same duration in the same order.

Multiple runs and tasks can be given ("\*") if the number of voxels is the same
within subject (the number of voxels can differ across subjects).
