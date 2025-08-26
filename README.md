# Algorithmic Dissection of Optic Flow Memory in Larval Zebrafish
This respository will host the code (jupyter notebooks) to analyze the data for / recreate the figures presented in Tanaka & Portugues (2025) Algorithmic dissection of optic flow memory in larval zebrafish [(preprint)](https://www.biorxiv.org/content/10.1101/2025.04.15.648832v1.abstract).

## Dataset
The dataset to be analyzed by this repository will be uploaded to Zenodo (doi: 10.5281/zenodo.16085585) (in preparation). 

The dataset containts raw behavioral as well as preprocessed imaging data.

Data are arranged in directories corresponding to each notebook file. Put unpacked data directories under the `data` folder in the repository.

## Environment
We recommend you use anaconda to manage the environment to run the notebooks.
The notebooks on this repository depends on following packages:
- `python=3.10.6`
- `bouter=0.2.0`
- `colorcet=3.0.1`
- `flammkuchen=1.0.2`
- `ipykernel`
- `matplotlib=3.6.0`
- `napari=0.4.19rc5`
- `pandas=1.5.0`
- `pip`
- `scikit-learn=1.1.2`
- `scipy=1.9.1`
- `tifffile=2022.8.12`
- `tqdm=4.64.1`

Please create an anaconda environment using the yml file provided `conda env create -f environment.yml` (named `ofmemory`). This yml file does not include packages installed through `pip` as including these made resolving dependency impossibly slow. Please install following packages through pip: `pip install numpy==1.22.4 bouter==0.2.0 scipy==1.9.1 tqdm==4.64.1 flammkuchen==1.0.2 napari==0.4.19rc5`. There will be some dependency issues regarding `numpy` and some packages, but this is for some un-used functions and should be fine.

Enter the newly created conda environment, and run `python -m ipykernel install --user --name=ofmemory` to register it to the jupyter lab. 

## Output
The notebooks save the figures as SVG (in the `svgs` folder), as they appear in paper figures (with the exact sizes), which is why they appear small on the screen.
