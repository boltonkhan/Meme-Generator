# Meme_Generator
> Simple meme generator working as a CIL aplication and as a Flask-based web application

## Table of content
* [General Info](#general-info)
* [Technologies](#technoloies)
* [Setup](#setup)
* [Features](#screenshots)
* [Example Meme](#example-meme)
* [Project Status](#project-status)
* [Acknowledgements](#acknowledgemts)

## General Info
Simple meme generator which is the final project of Udacity 'Intermidiate Python' course. 
It was created just to better understand features provide by additional Python libraries and look how  to work with images,
files, external libraries, APIs, multiprocessing etc. in Python.

## Technologies Used
- All libraries needed to setup the project are listed in requirements.txt file ![requirements.txt_file_path](requirements.txt).
- Additionally, the app uses unsplash v1 API (https://unsplash.com/documentation).
- Python 3.9 (Anaconda distribution)
- https://getbootstrap.com/ ver. 4.3.1

## Setup
To run the app you need to use at least Phython 3.9. Additional required libraries are listed in * *"requirements.txt"* * file.
To use all features of the app is needed to have an active api key of the unsplash api. The api key should be stored in the valid json file with the structure:

`{
  api_key: "SECRET_KEY"
 }`
 
 Default location of the file is: *"./_config_files/unsplash_config.json"* Location can be override in the `UnsplashService` constructor using `config_path` parameter.
 Default catalog for created memes is *_data\memes*
 The catalog include tmp subcatalog too for temporary files (downloaded by users directly from url or using unsplash API).
 Temporary files are removed immidiately after the application is stopped. Generated memem are cleaned after 24 hours by default but it can be changed adjusting
 `older_than` parameter (in seconds) `remove_old_meme` function in "./common.py" file.
 App provides two types of user interface: CLI and web app. Content catalogs by default are the same but can be adjust separately for both interfaces.
 - `meme.py` provides CLI interface and content catalogs are represented by global variables: 
   - `data_storage` *"_data"* (all data: quotes, and images to create memes, created memes and temp files),
   - `default_dir` *"_data/memes"* stores all generated memes,
   - `tmp_dir` *"./_data/memes/tmp"*.
 - `app.py` provides web interface and data content files are stored in parameters:
   - `storage` *"./_data/memes"* by default, the catalog with the access of the Flask app for static content
   - `tmp` *"./_data/memes"/tmp* by default, catalog for temporary downloaded files 
   - `static_url` * ./_data/memes* by default, use by Flask to render static content 

## Features

The app provides two user interfaces:
  - CLI
  - web interface

There is a different set of features for both:
- CLI, to run it just run `meme.py` file using `python meme.py` command with an optional parameters
  - with no parameter: generate random meme using random font from *"./_data/_fonts"* catalog, random image from *./_data/photos* catalg and random quote from files in *./_data* catalog
    - if there is no file `_data\Quotestoparse\quotes_toscrap.csv` then with the first run app will try to scrap quotes from https://quotes.toscrape.com
  - `--path`, use image from local path
  - `--url`, use image downloded from the given address
  - `--unsplash`, use random image downloaded from unsplash API
  - `--goodread` use random quote scrapped from random page of https://www.goodreads.com/ service
  - `--enhance` use additional random enhancement for the picture (adjust sharpness, brightness, contrast, color)
  - `--body` and `--author` define your own quote
For more info use `python meme.py --help`
- Web interface
  - button random generates random meme from existing resources
  - button creator lets user provide url to the picture and define his own quote
  - button unsplash provides random picture from unsplash service and lets user define his own quote
  - each correct generated meme can be download using Download button
  
## Example Meme
![Example meme](https://github.com/boltonkhan/Meme-Generator/blob/bc009d85522363087c264997174fb1e6086078ce/_data/memes/7cVuJUuHVw.png)

## Project Status
_no longer being worked on_ 
This is only a practice project.

## Acknowledgements
- Original idea is provided by https://www.udacity.com/
