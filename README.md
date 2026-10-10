# tdd

```
curl -L "https://docs.google.com/uc?export=download&id=1AsXP_OGs1O_TDeXiZjk3fYV1SrG4vwXF" -o data/Agrofood_co2_emission.csv
curl -L "https://docs.google.com/uc?export=download&id=19YEPysdnK7VCXuAe9Og9pwYkNT5CbQzr" -o data/IMF_GDP.csv
```

In the presentation, I investigated the relationship between GDP and emission due to forest fires. I took country-specific annual emissions and GDP data and plotted them to investigate potential trends. I found that some countries did not have enough information about either emissions or GDP data to draw useful conclusions. Many countries, on the other hand, showed either no trend with emissions data or showed exponentially decreasing emissions with GDP. One such plot is shown here for Australia.\
\
![Australia GDP vs. Forest Fires](figures/Australia.png)\
\
Additionally, I noticed a trend where the more recent years have greater emissions regardless of GDP. These plots and results were generated using the framework in the following script using Denmark as an example:\
\
python src/scatter.py --co2_file test/data/test_co2.csv --gdp_file test/data/test_gdp.csv --country "Denmark" --output figures/denmark.png\
