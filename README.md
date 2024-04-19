# [executable.graphics](https://executable.graphics/)

A gallery of 4K Executable Graphics artworks from the demoscene.

## Building

The build script requires Python >= 3.9.

Ensure you have the following available on the system PATH:
* [ImageMagick](https://imagemagick.org/)
* [Inkscape](https://inkscape.org/) >= 1.0
* [libavif](https://github.com/AOMediaCodec/libavif) >= 1.0.0
* [WebP](https://developers.google.com/speed/webp/download)

Install the Python dependencies:
```
$ pip install -r requirements.txt
```

Build the site:
```
$ ./build-site.py
```

The site will be built and placed into a `gen/` folder.


## Contributing

The website is open-source, but it is not open-contribution.

I've made it publicly-visible so that certain trusted individuals can more easily contribute localization, but beyond that I'd largely like to keep the site as it is.

For the sake of my mental health, I'd like to avoid the cognitive overhead of people sending me requests or patches.
