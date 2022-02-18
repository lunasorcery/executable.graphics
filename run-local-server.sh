#!/bin/bash
python3 -m http.server -d gen/root/ & python3 -m http.server -d gen/web1/ 8001
