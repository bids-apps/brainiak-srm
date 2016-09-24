#!/usr/bin/env python3
"""Brain Imaging Analysis Kit Shared Response Model runner"""

import argparse
import logging
import os.path

from pathlib import Path

import nibabel as nib
import nilearn.masking
import numpy as np

from scipy.stats import stats

import brainiak.funcalign.srm


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description="Shared Response Model runner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("bids_dir", help="Input directory")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("analysis_level",
                        help="Level of the analysis that will be performed",
                        choices=["group"])
    parser.add_argument("--participant_label",
                        help="Labels for participants to be analyzed",
                        nargs="+")
    parser.add_argument("--run", help="Run to be analyzed",
                        default="01")
    parser.add_argument("--task", help="Task to be analyzed, default is any",
                        default="*")
    parser.add_argument("--preproc", help="Preprocessing tag, default is any",
                        default="*")
    parser.add_argument("--mask", help="Mask tag", default="bmask")
    parser.add_argument("--iterations",
                        help="Number of iterations, default is SRM default",
                        type=int)
    parser.add_argument("--features",
                        help="Number of features, default is SRM default",
                        type=int)
    args = parser.parse_args()

    subject_dirs = Path(args.bids_dir, "derivatives").glob("sub-*")
    logger.info("Collecting subjects")
    if args.participant_label is not None:
        selected_subject_dirs = [s_dir for s_dir in subject_dirs if
                                 s_dir.name[4:] in args.participant_label]
    else:
        selected_subject_dirs = subject_dirs
    logger.info("Collecting files")
    subjects_files = [get_subject_files(s_dir, args)
                      for s_dir in selected_subject_dirs]
    logger.info("Masking")
    srm_input = process_input(subjects_files, args.mask)
    logger.info("Applying SRM")
    srm_attributes = apply_srm(srm_input, args.iterations, args.features)
    logger.info("Saving SRM attributes")
    np.savez(os.path.join(args.output_dir, "srm_attributes"),
             **srm_attributes)
    logger.info("Done")


def get_subject_files(subject_dir, args):
    """Compute input paths for each subject"""

    return (subject_dir / "func").glob(
        "*_task-{}_run-{}_{}.nii.gz".format(args.task, args.run, args.preproc))


def process_input(subjects_files, mask):
    """Process input to obtain data suitable for SRM"""

    mask_suffix = "_" + mask + ".nii.gz"
    srm_input = []
    for subject_files in subjects_files:
        srm_input_subject = []
        for path in subject_files:
            if path.name.endswith(mask_suffix):
                continue
            img = nib.load(str(path))
            mask_path = \
                str(path.with_suffix("").with_suffix("")) + mask_suffix
            mask = nib.load(str(mask_path))
            srm_input_subject.append(nilearn.masking.apply_mask(img, mask))
        srm_input.append(stats.zscore(np.concatenate(srm_input_subject),
                                      axis=0, ddof=1).T)
    return srm_input


def apply_srm(srm_input, iterations, features):
    """Apply SRM"""

    srm_args = {}
    if iterations is not None:
        srm_args["n_iter"] = iterations
    if features is not None:
        srm_args["features"] = features
    srm = brainiak.funcalign.srm.SRM(**srm_args)
    srm.fit(srm_input)
    return dict(s=srm.s_, w=srm.w_, sigma_s=srm.sigma_s_, mu=srm.mu_,
                rho2=srm.rho2_)


if __name__ == "__main__":
    main()
