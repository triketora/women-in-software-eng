This is the data collection follow-up to "Where are the numbers?"
https://medium.com/grace-hopper-2013/cb997a57252

About the Data
--------------
This data is focused on the number of women in software engineering, defined by women that are focused on writing and building software and tools. 
It discounts front-end designers, sysadmins, support/sales engineers, QA and other technical positions. 


Viewing Data
------------
The easiest way to view the collected data is this Google spreadsheet:
https://docs.google.com/spreadsheet/ccc?key=0AlZH8QBl60oodEJTdFA5TlZOcDJCMU02RkZoSHF5SHc#gid=0


Contributing Data
-----------------

To contribute numbers for a company or team, whether your own or
another, you can either

1. Send the information to me via Twitter at <a href="https://twitter.com/triketora">@triketora</a> or email me 
at tracy at pinterest dot com. I am happy to anonymize contributions
if they are sensitive.

2. Submit a pull request amending data.txt (click this link to easily submit a pull request: https://github.com/triketora/women-in-software-eng/edit/master/data.txt), 

    in the git commit message include:
    * the contributor (the person providing the data, preferably with qualifications, and a contact method such as Twitter handle) and 
    * source (e.g. internal headcount, /about team page count, etc.). 

    The submitter of the PR does not have to be the contributor of the data. For example:

    https://github.com/triketora/women-in-software-eng/commit/e9d76a956512247fd5f8a9a2e220a4ca403b5452
    ```
    Adding Rent the	Runway.
    
    Contributor: Camille Fournier, VP Architecture at Rent the Runway,
        @skamille
    Source: internal headcount
    
    https://medium.com/grace-hopper-2013/cb997a57252#d4d8-b3d509275bf9
    Rent the Runway is 7 out of 32 if you just count dev + ops, 10 out of
    37 if you count QA, 11 out of 39 if you count all the people I manage.
    ```

    It may be helpful to add your entry somewhere besides the end of the list, since everyone submitting to the end of the file means merge conflict party.     

How does the spreadsheet get updated?
-------------------------------------

Right now, I manually run `update_script.py` to pull the numbers out 
of `data.txt` and submit them to the Google spreadsheet.

Something like this:

    python update_script.py -e women.in.software.eng@gmail.com -p [password] -d data.txt


Questions / Comments / Concerns?
--------------------------------
Please reach out to me on Twitter at <a href="https://twitter.com/triketora">@triketora</a> or email me at tracy 
at pinterest.com. Feedback on anything big or small is very welcome :) 
