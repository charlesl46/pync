# PyNC (PyNamingConvention)

## Description

The goal of this package is to set a naming convention for your python_modules/folders/python module vars and check if it's respected by your python_modules/folders/python module vars.

## Usage

The parser has for default params following : 

- folder names : `kebab-case` (`^[a-z]+(-[a-z]+)*$`)
- module names : `snake_case` (`^[a-z]+(_[a-z]+)*$`)
- module var names : `snake_case` (`^[a-z]+(_[a-z]+)*$`)

They can be edited using a `nc_config.json` file or through cli args :

```json
// nc_config.json

{
    "path" : ".",
    "fonc" : "^[a-z]+(-[a-z]+)*$",
    "finc" : "^[a-z]+(_[a-z]+)*$",
    "varsnc" : "^[a-z]+(_[a-z]+)*$",
    "authf" : ["__init__.py"],
    "verbose" : true,
    "fail_under" : 0.5
}
```

is equivalent to :

`pync -p . --fonc "^[a-z]+(-[a-z]+)*$" --finc "^[a-z]+(_[a-z]+)*$" --varsnc "^[a-z]+(_[a-z]+)*$" -v --fail-under 0.5`

> Beware that the authorized filenames arg (`authf`) can't be passed in cli, requires json config file to use different value than default, which is `["__main__.py","__init__.py"]`

> PyNC will spawn a `nc_cache.json` file to compare with your precedent run just like `pylint` does for example.