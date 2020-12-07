# scan_data_importer

## Setup

```
$ cp .netrc.example .netrc
```

edit `.netrc` with your [github personal access token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token).

```
# setup virtual env
$ pipenv install


# reinstall grrmlog_parser
$ pipenv install git+https://github.com/scan-team/grrmlog_parser.git#egg=grrmlog_parser

# activate env
$ pipenv shell

# run
$ python test.py [path]
```

## Usage

### Import single map

```
$ python import_data.py [path] ([root])
```
