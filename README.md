This is the data collection follow-up to "Where are the numbers?"
https://medium.com/grace-hopper-2013/cb997a57252

Viewing Data
------------
The easiest way to view the collected data is this Google spreadsheet:
https://docs.google.com/spreadsheet/ccc?key=0AlZH8QBl60oodEJTdFA5TlZOcDJCMU02RkZoSHF5SHc#gid=0


Contributing Data
-----------------
Please read the [contributing guidelines](CONTRIBUTING.md).  Thank you for
helping us improve our data!

How does the spreadsheet get updated?
-------------------------------------

Right now, I manually run `update_script.py` to pull the numbers out 
of `data.txt` and submit them to the Google spreadsheet.

Something like this:

    python update_script.py -e women.in.software.eng@gmail.com -p [password] -d data.txt

You can pass it in to your own spreadsheet by supplying the Spreadsheet Key (`SS_KEY`):

    python update_script.py -e $GOOGLE_EMAIL_ADDRESS -p $PASSWORD -d data.txt -s $SS_KEY

Where `SS_KEY` is the key found in a Google Docs spreadsheet URL:

    https://docs.google.com/spreadsheet/ccc?key=$SS_KEY
    

Questions / Comments / Concerns?
--------------------------------
Please reach out to me on Twitter at <a
href="https://twitter.com/triketora">@triketora</a> or email me at
tracy at pinterest.com. Feedback on anything big or small is very
welcome :)
