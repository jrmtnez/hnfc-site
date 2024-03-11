# HNFC Site

This repository provides the frontend code for a fake news detection framework. This application is described in the article "Building a framework for fake news detection in the health domain".

## Installation

This section describes the installation process of this framework. This has been tested in Linux environments such as Debian and Ubuntu.

### Prerequisites

It is necessary to install a library to manage the database from Python:

```bash
$ sudo apt install libpq-dev
```

### Frontend installation

It is recommended that you use a separate Python 3.8 virtual environment for this application.

The required packages can be installed as follows:

```bash
$ pip install -r requirements.txt
```
The frontend is based on the [Django](https://www.django-rest-framework.org/tutorial/quickstart/) framework so the first step would be to install it according to the instructions indicated on their website. In our test environment we use [Apache](https://httpd.apache.org/) as the web server, instead of the development web server provided by Django.
Now we can download the source code and some additional data needed:

```bash
$ git clone https://github.com/jrmtnez/hnfc-site

```

## License and Disclaimer
Please see the LICENSE file for details. Downloading data indicates your acceptance of our disclaimer.

## Citation
```bibtex
@article{martinez-rico_building_2024,
	title = {Building a framework for fake news detection in the health domain},
	language = {en},
	author = {Martinez-Rico, Juan R and Araujo, Lourdes and Martinez-Romo, Juan},
	year = {2024}
}
```



