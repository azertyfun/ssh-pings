ssh-pings
=========

This is REST API that analyzes `journalctl` output to find `sshd` attempts to log as root.

You will need `python3`, `flask` and `flask-limiter` to run it. You will also need `ssh-pings-client` to visualize the output.

Documentation
-------------

### `/last`

Returns the last `root` login fail within the last hour and returns the following:
```JSON
{
    "timestamp": "<milliseconds since epoch for the last ping>",
    "origin": {
        "lat": <latitude>,
        "lon": <longitude>
    }
}
```

If no ping could be found within the last hour, `timestamp` will be the current time and `origin` will be `"unknown"`. `origin` can also be `"unknown"` if the `ip-api.com` API request fails.

### `/since/<timestamp>`

Returns the pings since `<timestamp>`, including the ping at `<timestamp>` if it exists.

If `<timestamp>` is older than an hour, it will return the following:

```JSON
{
    "error": "Invalid timestamp! Expected time since epoch in µs"
}
```

Otherwise, it will return the following:

```JSON
pings: [
    {
        "timestamp": "<milliseconds since epoch for the last ping>",
        "origin": {
            "lat": <latitude>,
            "lon": <longitude>
        }
    },
    {
        "timestamp": "<milliseconds since epoch for the last ping>",
        "origin": {
            "lat": <latitude>,
            "lon": <longitude>
        }
    },
    // ...
]
```

As for `/last`, `origin` can be `"unknown"` if `ip-api.com` fails. Furthermore, `pings` can be empty (`[]`) if no pings were found in the logs.
