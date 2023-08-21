install.packages("tidyverse")                                                   # Install and use tidyverse
library(tidyverse)           
install.packages("rgeos")      
library(rgeos)                                                                  
library(rgdal) 
install.packages("maptools")      
library(maptools)


so_clean <- read.csv("Data/so_renamed.csv")                                      # Check the write out went as intended
gi_clean <- read.csv("Data/so_renamed.csv")
