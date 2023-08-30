
# Guide

I appreciate there's a lot of files here, so I'll break it down. 

If you want to go about this chronologically:

1. **Main_Lang_NR** - here we import the raw data for gender identity and main language to create the first set of standalone interactive scatterplots. We focus on exploring the relationship between the non-response rate in local authorities and the %s of Non-English speakers.
2. **Religion_1** - we import data on the religious diversity of our LAs and append this data to our first scatterplot mentioned above.
3. **Religion_2** - we now use the religion dataset to build our second standalone interactive scatterplot, which focuses on a different relationship. Now we're interested in the relationship between the % of religious groups and their contribution to the non-response rate in our LAs.
4. **Sex** - focuses on calculating the male and female non-response rate to be included in Bokeh DataTables.
5. **Outputs** - finally, these files are where we take our interactive Bokeh graphs to the next level, i.e, we add drop-downs and hook up the notebook to a local server.
6. **main.py** - after outputs, we have our 'main.py' file which is located in the root folder of this repo. This is where we combine the outputs from SO and GI into one python script, which is hooked up to a local Bokeh server and then hosted remotely on Heroku. 

Anything suffixed by SO relates to sexual orientation, and GI to gender identity.
