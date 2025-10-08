import streamlit as st
import requests as rq
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import plotly.express as px
import pycountry_convert as pc

st.set_page_config(page_title="Global GDP Stacked Bar Plot", layout="wide")
st.title("Global GDP by Country and Continent (IMF Table)")

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
response = rq.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table", {"class": "wikitable"})

df = pd.read_html(StringIO(str(tables[0])))[0]

df = df.rename(columns={"Country/Territory": "Country"})

source_columns = [c for c in df.columns if any(s in c for s in ["IMF", "United Nations", "World Bank"])]
gdp_source = st.selectbox("Select GDP source", source_columns)

df = df[["Country", gdp_source]].dropna()
df[gdp_source] = (
    df[gdp_source]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("—", "", regex=False)
    .str.replace("…", "", regex=False)
    .replace("", "0")
)
df[gdp_source] = pd.to_numeric(df[gdp_source], errors="coerce")
df = df.dropna(subset=[gdp_source])

def country_to_continent(country_name):
    exceptions = {
        "United States": "NA",
        "Russia": "EU",
        "South Korea": "AS",
        "North Korea": "AS",
        "Taiwan": "AS",
        "Vatican City": "EU",
    }
    try:
        if country_name in exceptions:
            continent_code = exceptions[country_name]
        else:
            country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
            continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_map = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "North America",
            "SA": "South America",
            "OC": "Oceania",
        }
        return continent_map.get(continent_code, "Other")
    except:
        return "Other"

df["Continent"] = df["Country"].apply(country_to_continent)

df[gdp_source] = df[gdp_source] / 1e6

fig = px.bar(
    df.sort_values(by=gdp_source, ascending=False).head(50),
    x="Continent",
    y=gdp_source,
    color="Country",
    title=f"Top 50 Countries by GDP ({gdp_source}) - Stacked by Continent",
    labels={gdp_source: "GDP (US$ trillion)"},
    hover_data={"Country": True, gdp_source: True, "Continent": True},
)

st.plotly_chart(fig, use_container_width=True)