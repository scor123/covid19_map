#python function to ditect the top confirmed countries from the data set file
def find_top_confirmed(n = 15):

    import pandas as pd
    corona_df=pd.read_csv("dataset.csv")
    by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]
    return cdf

cdf=find_top_confirmed()
#creating pairs list which contains the country name and confirmed cases to print tem on the website
pairs=[(country,confirmed) for country,confirmed in zip(cdf.index,cdf['Confirmed'])]

#import pandas and folium, they are python library to create maps and mainpulate data
import folium
import pandas as pd
corona_df = pd.read_csv("dataset.csv")
corona_df=corona_df[['Lat','Long_','Confirmed']]
corona_df=corona_df.dropna()
#creating the map
m=folium.Map(location=[34.223334,-82.461707],
            tiles='Stamen toner',
            zoom_start=8)
#creating the red circles on the map
def circle_maker(x):
    folium.Circle(location=[x[0],x[1]],
                 radius=float(x[2]),
                 color="red",
                 popup='confirmed cases:{}'.format(x[2])).add_to(m)
corona_df.apply(lambda x:circle_maker(x),axis=1)

html_map=m._repr_html_()
#setting up the flask server
from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html",table=cdf, cmap=html_map,pairs=pairs)

if __name__=="__main__":
    app.run(debug=True)
