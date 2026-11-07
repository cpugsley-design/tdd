COUNTRIES = [
    "Australia",
    "Denmark",
    "Georgia",
    "Ireland",
    "United States of America"
]

CO2_FILE = "test/data/test_co2.csv"
GDP_FILE = "test/data/test_gdp.csv"

rule all:
    input:
        expand(
            "figures/workflow/{country}.png",
            country=COUNTRIES
        )

rule plot_country:
    input:
        co2=CO2_FILE,
        gdp=GDP_FILE,
        scatter="src/scatter.py",
        helper="src/fire_gdp.py"
    output:
        "figures/workflow/{country}.png"
    conda:
        "envs/plot.yml"
    shell:
        (
            "python {input.scatter:q} "
            "--co2_file {input.co2:q} "
            "--gdp_file {input.gdp:q} "
            "--country {wildcards.country:q} "
            "--output {output:q}"
        )