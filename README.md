# scan_data_importer

## Requirements

* [Pipenv](https://github.com/pypa/pipenv)

## Setup

```
# setup virtual env
$ pipenv install

# activate env
$ pipenv shell
```

## Usage

### Import single map

```
$ python import_data.py [path] (-r [root])
```

### Import multiple maps

```
$ python import_data_multi.py [base_path] (-r [root])
```


## Update grrmlog_parser

```
$ pipenv update grrmlog_parser
```
