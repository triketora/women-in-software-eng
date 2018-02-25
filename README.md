This is the data collection follow-up to "Where are the numbers?"
https://medium.com/grace-hopper-2013/cb997a57252

Viewing Data
------------
The easiest way to view the collected data is this Google spreadsheet:
https://docs.google.com/spreadsheet/ccc?key=0AlZH8QBl60oodEJTdFA5TlZOcDJCMU02RkZoSHF5SHc#gid=0


Contributing Data
-----------------
Please read the [contributing guidelines](CONTRIBUTING.md). Thank you for
helping to improve the data!

How does the spreadsheet get updated?
-------------------------------------

Right now, I manually run `update_script.py` to pull the numbers out
of `data.txt` and submit them to the Google spreadsheet.

Something like this:

    python2 update_script.py -d data.txt -s $SS_KEY

You can pass it in to your own spreadsheet by creating your own project in the
[Google Developers Console](https://console.developers.google.com/), generating
a client ID for a web application with redirect URI http://localhost:8080/,
saving those credentials into `client_secrets.json`, and running the script with
your own spreadsheet key `SS_KEY` specified, where `SS_KEY` is the key found in
a Google Docs spreadsheet URL:

    https://docs.google.com/spreadsheet/ccc?key=$SS_KEY


Questions / Comments / Concerns?
--------------------------------
Please reach out to me on Twitter at <a
href="https://twitter.com/triketora">@triketora</a> or contact me via my <a
href="https://triketora.com/contact/">website</a>. Feedback on anything big or
small is very welcome :)
