# Changelog
All notable changes to this project will be documented in this file.


## [0.2.1] - 2019-01-17

### Changed
- Evals and listeners are now called in separate threads, to avoid locks on the runtime.
- In **Selectors** changed the separator for the properties from '[' and ']' to '(' and ')' according to RFC3986

## [0.2.0] - 2019-01-10

### Changed
- Internal refactoring of the API
- **Admin** object added to management of YAKS

## [0.1.1] - 2018-12-21

### Changed
- **login** become a static method of YAKS and creates the YAKS API ( YAKS.login() returns a **YAKS** object)
- _put_; _update_; _remove_; _eval_; _workspace_ takes **str** or **Path**
- _get_; _subscribe_ takes  **str** or **Selector**
- _get_; _subscribe_ and _eval_; returns **str** as default for _paths_ the optional parameter _paths_as_string=False allow enable returns of YAKS types
- storage creation takes an id and a dictionary of properties with at least the property _is.yaks.storage.selector_ set with a valid **str**  or **Selector**

## [0.1.0] - 2018-12-20
### Added
- **Value** class for values
- **Path** class for paths
- **Selector** class for selectors
- _eval_ takes a function that accept a **Path** and other parameters (they are passed as kwargs, all values are string) and return a **Value**
- CHANGELOG.md
### Changed
- **login** has to be used for accessing YAKS
- **Access** is renamed as **Workspace**
- **delta_put** is renamed as **update**
- **close** is renamed as **logout**

- _put_; _update_; _remove_; _eval_; _workspace_ takes **Path**
- _get_; _subscribe_ takes **Selector**
- storage creation takes an id and a dictionary of properties with at least the property _is.yaks.storage.selector_ set with a valid **Selector**

### Removed
- **Storage** class



## [0.0.2] - 2018-11-14
### Added
- _subscribe_ with callback into **Access**
- _unsubscribe_ using subscriber id into **Access**

### Changed
- Nothing

### Removed
- Nothing


## [0.0.1] - 2018-11-09
### Added
- **YAKS** object used for connection and interaction with YAKS
- **Access** class for Accesses
- **Storage** class for Storages
- _create_access_ for access creation into YAKS
- _create_storage_ for storage creation into YAKS
- _put_; _delta_put_; _remove_; _get_ in **Access** for accessing the data
- _dispose_ for **Access** and **Storage**

### Changed
- Nothing

### Removed
- Nothing





#### Remarks

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).