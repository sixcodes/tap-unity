# tap-unity

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from unity api
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

---

## Running the tap

```
$ pip install .
$ tap-unity --config config.json # fill the config.json with the requested information
```


Copyright &copy; 2018 Stitch
