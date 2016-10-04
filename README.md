#September 2016 Minnesota Legislature outside spending cartograms

This project visualizes the amount of outside spending by groups supporting
Republican and Democratic candidates for Minnesota’s House of Representatives
and Senate, as reported to the
[Minnesota Campaign Finance and Public Disclosure Board](http://www.cfboard.state.mn.us/).

Since Twin Cities metro-area legislative districts are generally much smaller
than Greater Minnesota districts, this project uses cartograms in which all districts
are the same size in order to allow for accurate visual comparisons across districts
and see any geographic patterns of spending.

The visualizations can be seen in the story
[Where all that political money is being spent in Minnesota](https://www.minnpost.com/politics-policy/2016/10/where-all-political-money-being-spent-minnesota).

##Data
The main data for this visualization came from the Campaign Finance Board, based
on reports filed by independent expenditure groups covering the period from January
2016 through September 20, 2016. MinnPost edited that spreadsheet by hand to
eliminate spending on candidates who lost in the primary and spending on candidates
who were not candidates in the district the spending was listed in. We then totaled
the spending in each district by groups supporting Democrats (and opposing Republicans)
and vice versa. The results of all this are in `data/sep-16-mnleg-ies.csv`.

Other files in `/data` are used to determine the names of candidates
running in each district and whether they are incumbents, which is provided as
supplemental information in the visualization.

##Development
This visualization uses [flask](http://flask.pocoo.org/) to process the data
and feed it into an HTML template. It was written using Python 3.

To get started, set up a virtual environment:

`virtualenv -p python3 venv`

and activate it:

`source venv/bin/activate`

Then install the requirements:

`pip install -r requirements.txt`

To run it locally:

`python carto.py`

In general, data processing tasks are found in `carto.py` and layout/visualization
is in `templates/index.html`.

The arrangement of the districts in the cartograms was made using the very awesome
[aRanger](http://code.minnpost.com/aranger/).
