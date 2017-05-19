configapp
=========


JSON mask format
----------------
```
{
    "spots": [
        {"rotation": double angle,
         "points": [
            [double x_0, double y_0],
            [double x_1, double y_1],
            [...]
         ]
        }
        {...},
    ]
}
```

Prediction format is the same as mask format, but contains `occupied: 0/1`
property into each parking space.
