These are notebooks, files and codes about analyzing and build an ML to predict Paris real estate prices
there is the main ipynb file that have the entire code
Power BI that have the main analysis
and a folder that have deployable steamlit version of the predictive ML model and files about parts of the data analysis and preprocessing steps
main steps include preprocessing, merging datasets using coordinates and geo related libraries, enabling star schema, categorical and numeric analysis, and build the ML model


Sources for datasets:

Main dataset taken from an official French government website:
https://explore.data.gouv.fr/fr/immobilier?onglet=tableau&filtre=tous (values dataset)

Other three datasets taken form official open data portal for Paris:

https://opendata.paris.fr/explore/dataset/plub_pprizone/information/ (Risk dataset)

https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/information/?disjunctive.nom_quartier&disjunctive.piece&disjunctive.epoque&disjunctive.meuble_txt&disjunctive.id_zone&disjunctive.annee+-+logement-encadrement-des-loyers.csv&disjunctive.annee (rent control)

https://opendata.paris.fr/explore/dataset/plub_elpv/information/?dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiU1VNIiwieUF4aXMiOiJzdF9hcmVhX3NoYXBlIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzA3MUYzMiJ9XSwieEF4aXMiOiJuX3NxX2NhIiwibWF4cG9pbnRzIjoyMCwic29ydCI6IiIsImNvbmZpZyI6eyJkYXRhc2V0IjoicGx1Yl9lbHB2Iiwib3B0aW9ucyI6e319fV0sInRpbWVzY2FsZSI6IiIsImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9&basemap=jawg.dark&location=12,48.85856,2.33309 (protected vegetated spaces)
