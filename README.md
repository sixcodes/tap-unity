# tap-unity

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from Unity Acquisitions Report api
- Outputs the schema
- Incrementally pulls data based on the input state

---

## Running the tap

First you'll need to fill the `config.json` file with the following information:

```json
{
  "auth_token": "[auth token hash]",
  "organization_id": "[organization id code]",
  "split_by": "[split by field]",
  "granularity": "all|hour|day|week|month|quarter|year"
}
```
Remember that `split_by` and `fields` may vary according to the [Unity API](https://services.docs.unity.com/statistics/v1) and they are not required, if you don't specify them, the tap will use the default values which are:


With the `config.json` file filled out, you need to set a `state.json` file like the example below:

```json
{
  "last_record": "2018-01-01T00:00:00.000Z"
}
```

Now you can run the tap using:

```bash 
$ pip install .
$ tap-unity --config config.json --state state.json
```
