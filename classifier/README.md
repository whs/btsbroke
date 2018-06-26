# BTS SkyTrain text classifier

This repository provides a Python-based Machine Learning model for classificating BTS SkyTrain's status from its Twitter text.

## Installation

```
pip install -r requirements.txt
```

Which, to be honest, only `scikit-learn` is needed.

## Usage

```python
>>> import bts_classifier
>>> tweet_text = "20.40 ขบวนรถไฟฟ้าขัดข้องที่สถานีบางหว้า ขบวนรถในสายสีลมจะล่าช้า ขออภัยในความไม่สะดวก"
>>> status = bts_classifier.classify(tweet_text)
>>> status
'disrupted'
```

The `status` after the classification can be any of these four values:
* `None` (with `NoneType`) indicates that the processed tweet is unrelated to train service status
* `'normal'` indicates that the train had returned to its normal service
* `'disrupted'` indicates that the train has paused its operation.
* `'delay'` indicates that although there is the train service, but passengers are warned to expect train delays.