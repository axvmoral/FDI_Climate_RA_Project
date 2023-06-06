FDI Climate Disaster Map Example
================
Axel V. Morales Sanchez

``` r
library(ggplot2) #to plot map
library(tidyverse) #to handle data
library(readxl) #to read excel file
library(countrycode) #to convert country codes
library(pracma) #for nice plot breaks
library(haven) #to read dta file
```

``` r
data <- read_dta("C:/Users/axvmo/Desktop/UCSC/FDI Climate Project/Data/mergedFDIClimateAnnual1956_112_processed_wdi.dta")
hydro.disasters.data <- data %>%
  select(iso, ofc, year, hydrological_m) %>%
  filter(ofc == 0) %>%
  group_by(iso) %>%
  summarise(lhydro.disasters = log(sum(hydrological_m)))
hydro.disasters.data$lhydro.disasters <- ifelse(hydro.disasters.data$lhydro.disasters == -Inf,
                                                0, hydro.disasters.data$lhydro.disasters)

mapdata <- map_data("world")
mapdata$iso <- countrycode(mapdata$region, origin = "country.name", destination = "iso3c")
plot.data <- left_join(mapdata, hydro.disasters.data, by = "iso")
plot.data <- plot.data %>% filter(iso != "ATA")
plot.min <- min(na.omit(hydro.disasters.data$lhydro.disasters))
plot.max <- max(na.omit(hydro.disasters.data$lhydro.disasters))
plot.breaks <- linspace(plot.min, plot.max, 8)
plot.labels <- format(plot.breaks, digits = 3)

map <- ggplot(plot.data, aes(x = long, y = lat, group = group)) +
  geom_polygon(aes(fill = lhydro.disasters), color = "black") +
  scale_fill_binned(name = "   Log Hydrological \n Disasters All Years",
                    labels = plot.labels,
                    breaks = plot.breaks,
                    low = "aquamarine", 
                    high = "slateblue4",
                    guide = "legend",
                    na.value = "lightgrey") + 
  theme(axis.title.x = element_blank(),
        axis.text.x = element_blank(), 
        axis.title.y = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        rect = element_blank(),
        legend.position = c(0.66,0.0258), 
        legend.direction = "horizontal",
        legend.key.height = unit(1.5, "mm"),
        legend.key.width = unit(3.5, "mm"),
        legend.title = element_text(size = 8),
        legend.text = element_text(size = 8)
  )
```

``` r
map
```

<img src="disaster_map_example_files/figure-gfm/display map-1.png" style="display: block; margin: auto;" />
