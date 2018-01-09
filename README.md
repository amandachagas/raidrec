# RaidRec
## Aggregation techniques for recommendation

This repository will implement Aggregation Techniques on Python in the context of groups. The product of this work will be reused henceforth in a Group Recommender project.

## Environment Setup

On this project we will use the GraphLab Create lib. You can get a free student license [here](https://turi.com/download/academic.html). Once you recieved the email with your license you can proceed with their tutorial or follow the steps below(retrieved from their website):

#### Step 1: Create and activate a new virtual environment (recommended)

```
# Create a virtual environment named e.g. gl-env
virtualenv gl-env

# Activate the virtual environment
source gl-env/bin/activate
```

#### Step 2: Ensure pip version >= 7

```
# Make sure pip is up to date
pip install --upgrade pip
```

#### Step 3: Ensure installation of IPython and IPython Notebook

```
# Install IPython Notebook (optional)
pip install "ipython[notebook]"
```

#### Step 4: Install GraphLab Create

```
# Install your licensed copy of GraphLab Create
pip install --upgrade --no-cache-dir https://get.graphlab.com/GraphLab-Create/2.1/(YOUR_EMAIL)/(YOUR_LICENSE)/GraphLab-Create-License.tar.gz
```