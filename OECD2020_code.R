#The code below was completed as an RA task for the FDI Climate Project
#at UCSC. The task was to compile two folders full of datasets, and one
#existing dataset into one comprehensive dataset. Averages of each value 
#column in the comprehensive dataset are then taken according to a crosswalk,
#yielding the final dataset to be written. 

#The first folder is EmRel10, and the second is Gross10; the existing datset is CO2,
#identified below. The crosswalk is also identified below.


#Load libraries

library(tidyverse) #for data wrangling
library(readxl) #to read excel files
library(haven) #to write dta files
library(reshape2) #to melt data
library(data.table) #to elongate rows


#Set window where datasets are kept/exported to

setwd("C:/Users/axvmo/Desktop/UCSC/FDI Climate Project/Data")


#The code block below creates a function that will be useful in
#manipulating each dataset from both the EmRel10 and Gross10 folders.

tidy <- function(path, iso3_code, data_ind){
  #Wrangles datasets from EmRel10 or Gross10 datset folders. Returns
  #a dataset that is ready to be stacked with datasets of their respective
  #folders.

  #:param path: the full path to the dataset in either EmRel10 or Gross10
  #:param iso3_code: the iso3 code of the country for which the data belongs to
  #:param data_ind: a string indicator for which folder the dataset is originating from;
  #                 "x1" for datasets in Gross10 and "x2" for datasets in EmRel10

  target_df <- set_names(excel_sheets(path)[-1:-3]) %>%
    map_df(read_excel, path = path, .id = "year") %>%
    rename_with(~ tolower(paste(data_ind, .x, sep = "_"))) %>%
    rename(year = paste(data_ind, "year", sep = "_"), Em_Gross_code = paste(data_ind, "...1", sep = "_")) %>%
    mutate(year = strtoi(year), iso3_code = iso3_code)
  return(target_df)
}


#The code block below manipulates CO2 to get it ready for merging.

CO2 <- set_names(excel_sheets("WIOD16 CO2 emissions with WIOD13 codes.xlsx")[-1:-2]) %>%
  map_df(read_excel, path = "WIOD16 CO2 emissions with WIOD13 codes.xlsx", .id = "iso3_code") %>%
  rename(CO2_code = ...1) %>%
  melt(id.vars = c("iso3_code", "CO2_code"), variable.name = "year") %>%
  rename(co2_emissions = value) %>%
  mutate(year = strtoi(year))


#The code block below establishes some preperation variables for
#merging, particularly loading and manipulating a crosswalk, and
#loading the path names of each dataset in EmRel10 and Gross10

translation_df <- read_excel("translation.xlsx") %>% select(CO2_code, Em_Gross_code)
crosswalk <- data.table(
  select(read_excel("crowsswalk_FDI_WIOD16-2.xlsx"), ECO_ACT, vars_2020)
  )[ , list(CO2_code = unlist(map(strsplit(vars_2020, ","), ~ str_trim(.x)))), by = ECO_ACT]
EmRel10_files <- list.files(path = "C:/Users/axvmo/Desktop/UCSC/FDI Climate Project/Data/EmRel10", full.names = TRUE)
Gross10_files <- list.files(path = "C:/Users/axvmo/Desktop/UCSC/FDI Climate Project/Data/Gross10", full.names = TRUE)


#The code block below compiles all the datasets from both Gross10
#and EmRel10 and merges them, then merging with CO2 to create 
#a comprehensive dataset. The value columns of this dataset are then 
#averaged according to the crosswalk, and the final dataset is written 
#as a .dta file.

OECD2020 <- merge(
  map_df(Gross10_files, ~ tidy(path = .x, iso3_code = str_extract(str_extract(.x, "_([A-Z]+)[.]"), "[A-Z]+"), data_ind = "x1")),
  map_df(EmRel10_files, ~ tidy(path = .x, iso3_code = str_extract(str_extract(.x, "_([A-Z]+)[.]"), "[A-Z]+"), data_ind = "x2")),
  id = c("year", "iso3_code", "Em_Gross_code")) %>%
  merge(translation_df, id = "Em_Gross_Code") %>%
  merge(CO2, id = "CO2_code", all.x = TRUE, no.dups = TRUE) %>%
  merge(crosswalk, id = "CO2_code") %>%
  group_by(iso3_code, year, ECO_ACT) %>%
  summarise(across(x1_coal_coke_crude:co2_emissions, ~mean(.x, na.rm = TRUE))) %>%
  data.frame()

write_dta(OECD2020, "OECD2020.dta")
