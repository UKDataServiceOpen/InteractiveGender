install.packages("tidyverse")                                                       # Install and use tidyverse
library(tidyverse)

so_raw <- read.csv("Data/SO-2021.csv")                                              # Read in the raw files
gi_raw <- read.csv("Data/GI-2021.csv")

colnames(so_raw)                                                                    # Check stupid column names in raw files
colnames(gi_raw)


so <- plyr::rename(so|raw, c("Lower.Tier.Local.Authorities.Code" = "LA_code",        # rewrite the column names to be shorter, clearer
                         "Lower.Tier.Local.Authorities" = "LA_name",                 # The final column "Observations" doesn't need renamed
                         "Sexual.orientation..6.categories..Code" = "SO_code",       # NOTE: this rename explicitly uses `plyr` to avoid the
                         "Sexual.orientation..6.categories." = "SO_categories"))     # "can't rewrite columns that don't exist" problem.
 
gi <- plyr::rename(gi_raw, c("Lower.Tier.Local.Authorities.Code" = "LA_code",        # Repeat for the second file
                         "Lower.Tier.Local.Authorities" = "LA_name",
                         "Gender.identity..7.categories..Code" = "GI_code",
                         "Gender.identity..7.categories." = "GI_categories"))
 
write_csv(so, "Data/so_renamed.csv")                                               # Write out the nicely named files as .csv
write_csv(gi, "Data/gi_renamed.csv")


# so_clean <- read.csv("Data/so_renamed.csv")                                      # Check the write out went as intended
# gi_clean <- read.csv("Data/so_renamed.csv")
