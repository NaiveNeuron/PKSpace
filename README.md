# PKSpace
Estimate the number of free/occupied parking spaces in your parking lot using a cheap webcam.

### Dataset

The FMPH dataset related to the PKSpace package can be found
[here](https://zenodo.org/record/572368).

## Installation and Setup

### Installing requirements
First of all, install all dependencies included in `requirements.txt`. To do so,
run

`$ pip install -r requirements.txt`

### Setting up global variables

Default settings are stored in `configapp/config_default.json` file. We don't
recommend overwriting these, but insted create a file `configapp/config.json`
where you are able to overwrite part of these variables. 

* `IMAGE_PATH` - Path to folder containing images to be used as background when creating mask.
* `IMAGE_SUFFIX` - Suffix of images taken from camera.
* `DATASET_PATH` - Path to dataset folder. Note that dataset folder should contain subfolders named by date `yyyy-mm-dd` and these contain images named `hh_mm_ss.IMAGE_SUFFIX`.
* `IMAGES_TO_PREDICT_PATH` - Path to folder containing images which are about to be predicted. The subfolder structure looks the same like `DATASET_PATH`.
* `MASK_PATH` - Path to folder containing masks for labeling images.
* `PREDICTION_PATH` - Path to folder containing predicted images. The subfolder structure looks the same like `IMAGES_TO_PREDICT_PATH`.
* `PICTURE_WIDTH` - Width of captured pictures.
* `PICTURE_HEIGHT` - Height of captured pictures.

### Creating your own dataset

Start the flask application by running the command below from the root of PKSpace directory

`$ python wsgi.py`

Navigate your webbrowser to `localhost:5000`

#### Creating a mask

* Select **Mask Creator** in the top menu.
* Choose background image
* Click on the corners of specific parking space (and possibly adjust the points).
  If you want to adjust the rotation of the parking space mask (to improve the size of minimal bounding rectangle), you can do so by moving the slider above mask canvas.
  Then click on **Save Polygon** and continue with another one.
* Once you are done with marking all the areas of parking spaces, click on **Generate output**, choose the name for your mask and save it.

#### Labeling images

* Select **Labeler** in the top menu.
* Choose an image which you want to label.
* Choose a mask that fits your parking lot the best.
* By clicking on specific parking space you can change its color red/green.
  Mark those parking spaces which are being vacant with green color and occupied ones with red color.
* Click **Save labeled image** and continue by labeling another image.

#### Training models

TODO

### Capturing images and predicting occupancy

Script example for capturing and predicting occupancy of the parking lot

```bash
pushd path/to/PKSpace/
        img=`python scripts/capture.py --path=path/to/IMAGES_TO_PREDICT --rotate=180 --print_path=True`
        python scripts/predict.py --mask_path=path/to/mask.json --picture_path=path/to/$img --model_path=pkspace/models/MLP.pkl.2 --output=path/to/predictions/$img
popd
```


