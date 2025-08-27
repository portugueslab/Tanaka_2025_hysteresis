# Data 

Please download data from Zenodo (doi: 10.5281/zenodo.16085585).

Unzip each folder (e.g., `fig1`, `fig2`) and put them directly under this data directory.

## Data structure
Under each data folder, there are folders for a single fish (with the exception of 2-photon data in `fig7`, where each folder corresponds to a single recording plane).

### Behavioral data
For the behavioral experiments, each fish folder contains following files:
- `metadata.json`

	This file contains experiment metadata, including the sequence and parameters of each stimulus epoch.

- `stimulus_log.hdf5`

	This file contains time traces of stimulus related parameters, including fish behaviors estimated online for closed-loop stimulation. We extensively use these online estimates as the readouts of the fish behavior. The time resolution of this file is about 60 Hz.

- `behavior_log.hdf5` (optional)

	This file contains the raw data from tail tracking at 200 Hz. Because this file tends to be heavy, we deleted them except where we need them for analyses.
	
The `behavior` folders in imaging data folders also contain the identical set of files.

In the analysis code, we use `bouter` package to load these behavior files. 

`EmbeddedExperiment()` method loads the metadata as a python dictionary, and the contents of `stimulus_log` and `behavior_log` are loaded as pandas DataFrame.

### Imaging data
Imaging data in `fig6` and `fig7` were preprocessed with `suite2p`. We do not share the raw imaging data because they are too heavy. h5 files named like `data_from_suite_suite2p` in each recording folder contains output of suite2p, which includes aligned anatomical stacks and ROI-wise florescence time traces.

For the light-sheet data in `fig6`, coordinates of ROIs after non-linear morphing to the [MapZBrain](https://mapzebrain.org/) atlas are saved as a separate h5 file (`mov_roi_coords_transformed.h5`).

For the two-photon data in `fig7`, following additional files are included:
- `scandata.json`

	The scan setting of the two photon microscope.
	
- `mask<timestamp>.json'

	Specifies the coordinates of a rectangular mask manually drawn around the inferior olive.
	
- `time.h5`

	Time vector for the imaging data.
