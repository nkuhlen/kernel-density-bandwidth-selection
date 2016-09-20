'
Programme to plot the countries included in the estimation of the world income
distributions. The list is obtained from data_preparation_pwt_71.py.
'

# Clear R-workspace
rm(list=ls())

source("project_paths.r")

library(rworldmap)

# Load names of included countries.
countries <- read.csv(
	paste(PATH_OUT_DATA, 'countries.csv', sep="/"), sep=',', header=FALSE
)

# Remove second series for China.
# countries <- countries[-(countries$V1=="CH2"),]

# Replace country isocodes which do not follow ISO 3166-1 alpha-3.
countries$V1 <- as.character(countries$V1)
countries$V1[countries$V1 == "ZAR"] <- "COD"
countries$V1[countries$V1 == "GER"] <- "DEU"
countries$V1[countries$V1 == "ROM"] <- "ROU"
countries$V1[countries$V1 == "CH2"] <- "CHN"

# Add a column of 1's used to mark included countries.
countries["indicator"] <- 1

# Join data frame to country map data.
map <- joinCountryData2Map(countries, joinCode = "ISO3", nameJoinColumn = "V1")

# Create map and save it to pdf.
pdf(paste(PATH_OUT_FIGURES, "fig_map_included_countries.pdf", sep="/"))
mapCountryData(
	map, nameColumnToPlot="indicator", catMethod = "categorical", mapTitle="",
	missingCountryCol = gray(.85), addLegend=FALSE, colourPalette='black2White'
)
dev.off()
