#!/bin/bash
python3 -m http.server -d gen/root/ & python3 -m http.server -d gen/throwback/ 8001
