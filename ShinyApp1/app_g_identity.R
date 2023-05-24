### APP for Gender Identity ### 

Sys.setenv(SHINYSENDER_REMOTENAME="app_g_identity.R")

library(readr)
library(janitor)
library(ggmap)
library(mapview)
library(sf)
library(readxl)
library(tmap)
library(dplyr)
library(sp)
library(spdep)
library(ggplot2)
library(ggspatial)
library(shiny)
library(sf)
library(dplyr)
library(ggplot2)
library(leaflet)
library(shinydashboard)


## Read in cleaned and merged data
la_gi <- st_read("/Users/user/Documents/InteractiveGender/Shapefiles/gi_spatial.shp") %>%
  clean_names() %>%
  rename("gi_categories" = g_ctgrs)
head(la_gi)

# This line of code is important. This removes those invalid geometries (those with looped vertices), be patient it takes about 1-2 minutes to run. 
# st_is_valid(la_gi, reason = T)
# la_gi <- st_make_valid(la_gi)
# 
# # And remove NAs, mainly Welsh LAs
# sum(is.na(la_gi$geometry))
#la_gi <- na.omit(la_gi)


classification_description <- list(
              quantile = "Quantile: each class contains an equal number of location",
              sd = "Standard Deviation: shows you how much a location's attribute value varies from the mean",
              jenks = "Jenks: Clusters data into groups that minimize the within-group variance and maximize the between-group variance",
              cont = "Continous: maps the values of col to a smooth gradient",
              order = "Order: maps the order of values of col to a smooth gradient",
              log10 = "Logarthimic Clustering: uses a logarithmic transformation",
              hclust = "Hierachical Clustering: groups similar objects into a dendrogram by merging similar objects iteratively",
              bclust = "Bagged Clustering: A partitioning cluster algorithm such as kmeans is run repeatedly on bootstrap samples from the original data. The resulting cluster centers are then combined using the hierarchical cluster algorithm",
              kmeans = "K Means: Partitions n observations into k clusters in which each observation belongs to the cluster with the nearest mean (cluster centers or cluster centroid)")



ui <- navbarPage(
  "UK Census 2021", 
  
  # theme = bs_theme(),
  # windowTitle = "UK Census 2021",
  # header = list(
  #   tags$head(
  #     tags$style(
  #       ".navbar {position:relative;}", 
  #       ".navbar-brand img {position:absolute; top:0px; right:0px; height:50px; width:50px;}"
  #     ),
  #     tags$link(rel = "shortcut icon", href = "/Users/user/Documents/InteractiveGender/ukds_logo.png")
  #   )
  # ),
  # 
  
  navbarMenu("Gender Identity by Local Authority",
  tabPanel("Leaflet",
           sidebarLayout(
             sidebarPanel(
               # selectInput("gi_categories", "Choose a Gender Identity:", 
               #             choices = unique(la_gi$gi_categories), multiple = TRUE), 
               selectInput("gi_categories", "Choose a Gender Identity:", 
                           choices = unique(la_gi$gi_categories), selected = unique(la_gi$gi_categories)[1]),
               selectInput("urb_rur", "Choose an Area Type:", 
                           choices = c("All", unique(la_gi$urb_rur)), multiple = TRUE), 
               selectInput("reg_nam", "Choose a Region:", 
                           choices = c("All", unique(la_gi$reg_nam)), multiple = TRUE), 
               numericInput("num_breaks", "Number of Color Breaks", value = 5, min = 1) 
             ),
             mainPanel(
               leafletOutput("map"),
               tableOutput("summary_table")
             )
           )),
  
  tabPanel("tmap",
           sidebarLayout(
             sidebarPanel(
               # selectInput("gi_categories_tmap", "Choose a Gender Identity:", 
               #             choices = unique(la_gi$gi_categories), multiple = TRUE),
               selectInput("gi_categories", "Choose a Gender Identity:", 
                           choices = unique(la_gi$gi_categories), selected = unique(la_gi$gi_categories)[1]),
               selectInput("urb_rur", "Choose an Area Type:", 
                           choices = c("All", unique(la_gi$urb_rur)), multiple = TRUE),
               selectInput("reg_nam", "Choose a Region:", 
                           choices = c("All", unique(la_gi$reg_nam)), multiple = TRUE), 
               selectInput("class_tmap", "Choose Classification Method:",
                           choices = c("quantile", "sd", "jenks", "order", "cont", "log10", "hclust", "bclust", "kmeans")), 
               checkboxInput("base_map", "Show Base Map", value = FALSE),
               # numericInput("num_breaks_tmap", "Number of Color Breaks", value = 5, min = 1)
             ),
             mainPanel(
               tmapOutput("tmap"),
               textOutput("classification_description"), 
               hr(),
               tableOutput("summary_table_tmap")
               
             )
           ))
), 
  #,
  # navbarMenu("Sexual Orientation by Local Authority",
  #          tabPanel("Leaflet",
  #                   sidebarLayout(
  #                     sidebarPanel(
  #                       # selectInput("gi_categories", "Choose a Gender Identity:", 
  #                       #             choices = unique(la_so$gi_categories), multiple = TRUE), 
  #                       selectInput("so_categories", "Choose a Sexual Orientation:", 
  #                                   choices = unique(la_so$so_categories), selected = unique(la_so$so_categories)[1]),
  #                       selectInput("urb_rur_so", "Choose an Area Type:", 
  #                                   choices = c("All", unique(la_so$urb_rur)), multiple = TRUE), 
  #                       selectInput("reg_nam_so", "Choose a Region:", 
  #                                   choices = c("All", unique(la_so$reg_nam)), multiple = TRUE), 
  #                       numericInput("num_breaks_so", "Number of Color Breaks", value = 5, min = 1) 
  #                     ),
  #                     mainPanel(
  #                       leafletOutput("map_so"),
  #                       tableOutput("summary_table_so")
  #                     )
  #                   )),
  #     
  #         tabPanel("tmap",
  #              sidebarLayout(
  #                sidebarPanel(
  #                  # selectInput("gi_categories_tmap", "Choose a Gender Identity:", 
  #                  #             choices = unique(la_so$gi_categories), multiple = TRUE),
  #                  selectInput("so_categories", "Choose a Sexual Orientation:", 
  #                              choices = unique(la_so$so_categories), selected = unique(la_so$so_categories)[1]),
  #                  selectInput("urb_rur_so", "Choose an Area Type:", 
  #                              choices = c("All", unique(la_so$urb_rur)), multiple = TRUE),
  #                  selectInput("reg_nam_so", "Choose a Region:", 
  #                              choices = c("All", unique(la_so$reg_nam)), multiple = TRUE), 
  #                  selectInput("class_tmap_so", "Choose Classification Method:",
  #                              choices = c("quantile", "sd", "jenks", "order", "cont", "log10", "hclust", "bclust", "kmeans")), 
  #                  checkboxInput("base_map_so", "Show Base Map", value = FALSE),
  #                  # numericInput("num_breaks_tmap", "Number of Color Breaks", value = 5, min = 1)
  #                ),
  #                mainPanel(
  #                  tmapOutput("tmap_so"),
  #                  textOutput("classification_description"), 
  #                  hr(),
  #                  tableOutput("summary_table_tmap_so")
  #                  
  #                )
  #              ))

tabPanel("References",
         tags$ul(
           tags$li(tags$a(href="https://cran.r-project.org/web/packages/tmap/tmap.pdf", "Information on tmaps from cran website", target="_blank")),
           tags$li(tags$a(href="https://cran.r-project.org/web/packages/leaflet/index.html", "Information on leaflet package from cran website", target="_blank")),
           tags$li(tags$a(href="https://www.axismaps.com/guide/data-classification", "Definitions used for classification types", target="_blank")),
           tags$li(tags$a(href="https://www.spatialanalysisonline.com/HTML/classification_and_clustering.htm", "Definitions used for classification types 2", target="_blank"))
         )
) 

# navbarMenu(
#   a(href = "https://ukdataservice.ac.uk/", 
#     img(src = "/Users/user/Documents/InteractiveGender/ukds_logo.png", height = "50", width = "100")))



  )






server <- function(input, output, session) {
  
  # # Reactive expression for filtered data
  # gender_data <- reactive({
  #   df <- la_gi %>%
  #     filter(gi_categories == input$gi_categories,
  #            urb_rur %in% if (input$urb_rur != "All") input$urb_rur else unique(la_gi$urb_rur),
  #            reg_nam %in% if (input$reg_nam != "All") input$reg_nam else unique(la_gi$reg_nam)) # new line for filtering by region
  #   df
  # })
  
  # Reactive expression for filtered data - gi 
  gender_data <- reactive({
    req(input$gi_categories)  # this line will stop the code execution if input$gi_categories is NULL or empty
    
    df <- la_gi %>% 
      filter(gi_categories %in% input$gi_categories,
             (if ("All" %in% input$urb_rur) TRUE else urb_rur %in% input$urb_rur),
             (if ("All" %in% input$reg_nam) TRUE else reg_nam %in% input$reg_nam))
    
    df
  })
  
  output$map <- renderLeaflet({
    # Use the reactive gender_data() here
    df <- gender_data()
    
    # Check if the data frame is empty
    if(nrow(df) == 0) {
      return(NULL)
    }
    
    # Check if 'obsrvtn' is numeric and if there are any NA or NULL values
    if(!is.numeric(df$obsrvtn) || any(is.na(df$obsrvtn)) || any(is.null(df$obsrvtn))) {
      return(NULL)
    }
    
    # Create a color palette
    pal <- colorQuantile("YlOrRd", NULL, n = 5)
    
    # Check if we have enough unique values
    if(length(unique(df$obsrvtn)) > 1) {
      pal <- colorQuantile("YlOrRd", df$obsrvtn, n = 5)
    }
    
    m <- leaflet(df) %>%
      addProviderTiles(providers$OpenStreetMap) %>%
      addPolygons(fillColor = ~pal(obsrvtn),
                  fillOpacity = 0.8, 
                  color = "#BDBDC3", 
                  weight = 1,
                  label = ~paste(lad22nm, ": ", obsrvtn, " respondents"),
                  highlightOptions = highlightOptions(color = "white", weight = 2,
                                                      bringToFront = TRUE))
    
    
    m %>% addLegend(pal = pal, values = ~obsrvtn, title = "Number of Respondents",
                    position = "bottomright")
  })
  
  output$tmap <- renderTmap({
    if(is.null(input$class_tmap)) {
      return(NULL)
    }
    
    # Use the reactive gender_data() here
    df <- gender_data()
    
    # # Ensure the breaks input is numeric
    # breaks <- as.numeric(input$num_breaks_tmap)
    # 
    # # Check for NA or invalid values
    # if (is.na(breaks) || breaks <= 0) {
    #   breaks <- 5  # Default to 5 breaks if input is not valid
    # }
    
    # Ensure classification is a single string
    classification <- as.character(input$class_tmap)
    
    # Check if the df is empty or if the obsrvtn column is not numeric
    if(nrow(df) == 0 || !is.numeric(df$obsrvtn)) {
      return(NULL)
    }
    
    # Create the tmap object
    tm <- tm_shape(df) +
      tm_polygons("obsrvtn", 
                  style = classification, 
                  #n = breaks,
                  border.col = "black",
                  border.lwd = 2,
                  palette = "-Spectral",
                  title = "Observation") +
      tm_layout(title = paste("Gender Identity: ", input$gi_categories))
    
    # If the checkbox is checked, add the base map
    if(input$base_map) {
      tm <- tm + tm_basemap(server = "OpenStreetMap")
    }
    
    tm
  })
  
  output$classification_description <- renderText({
    classification_description[[input$class_tmap]]
  })
  
  output$summary_table <- renderTable({
    # Use the reactive gender_data() here
    df <- gender_data()
    
    # Check if the data frame is empty
    if(nrow(df) == 0) {
      return(NULL)
    }
    
    # Convert to a standard data frame
    df <- as.data.frame(df)
    
    summary_df <- df %>%
      rename(Urbanisation = urb_rur) %>%
      group_by(Urbanisation) %>%
      summarise(count = sum(obsrvtn, na.rm = TRUE), .groups = 'drop') %>%
      mutate(percentage = count / sum(count) * 100)
    
    summary_df 
  })
    
  output$summary_table_tmap <- renderTable({
      # Use the reactive gender_data() here
      df <- gender_data()
      
      # Check if the data frame is empty
      if(nrow(df) == 0) {
        return(NULL)
      }
      
      # Convert to a standard data frame
      df <- as.data.frame(df)
      
      summary_df <- df %>%
        rename(Urbanisation = urb_rur) %>%
        group_by(Urbanisation) %>%
        summarise(count = sum(obsrvtn, na.rm = TRUE), .groups = 'drop') %>%
        mutate(percentage = count / sum(count) * 100)
      
      summary_df
    })
  
  
  #### Reactive expression for filtered data - so #####
  # 
  # so_data <- reactive({
  #   la_so %>%
  #     filter(
  #       so_categories == input$so_categories,
  #       if ("All" %in% input$urb_rur_so) TRUE else urb_rur_so %in% input$urb_rur_so,
  #       if ("All" %in% input$reg_nam_so) TRUE else reg_nam_so %in% input$reg_nam_so
  #     )
  # })
  # 
  # output$map_so <- renderLeaflet({
  #   # Use the reactive so_data() here
  #   df2 <- so_data()
  #   
  #   # Check if the data frame is empty
  #   if(nrow(df2) == 0) {
  #     return(NULL)
  #   }
  #   
  #   # Check if 'obsrvtn' is numeric and if there are any NA or NULL values
  #   if(!is.numeric(df2$obsrvtn) || any(is.na(df2$obsrvtn)) || any(is.null(df2$obsrvtn))) {
  #     return(NULL)
  #   }
  #   
  #   # Create a color palette
  #   pal <- colorQuantile("YlOrRd", NULL, n = 5)
  #   
  #   # Check if we have enough unique values
  #   if(length(unique(df2$obsrvtn)) > 1) {
  #     pal <- colorQuantile("YlOrRd", df2$obsrvtn, n = 5)
  #   }
  #   
  #   m <- leaflet(df2) %>%
  #     addProviderTiles(providers$OpenStreetMap) %>%
  #     addPolygons(fillColor = ~pal(obsrvtn),
  #                 fillOpacity = 0.8, 
  #                 color = "#BDBDC3", 
  #                 weight = 1,
  #                 label = ~paste(lad22nm, ": ", obsrvtn, " respondents"),
  #                 highlightOptions = highlightOptions(color = "white", weight = 2,
  #                                                     bringToFront = TRUE))
  #   
  #   m %>% addLegend(pal = pal, values = ~obsrvtn, title = "Number of Respondents",
  #                   position = "bottomright")
  # })
  # 
  # output$tmap_so <- renderTmap({
  #   if(is.null(input$class_tmap_so)) {
  #     return(NULL)
  #   }
  #   
  #   # Use the reactive so_data() here
  #   df2 <- so_data()
  #   
  #   # # Ensure the breaks input is numeric
  #   # breaks <- as.numeric(input$num_breaks_tmap)
  #   # 
  #   # # Check for NA or invalid values
  #   # if (is.na(breaks) || breaks <= 0) {
  #   #   breaks <- 5  # Default to 5 breaks if input is not valid
  #   # }
  #   
  #   # Ensure classification is a single string
  #   classification <- as.character(input$class_tmap_so)
  #   
  #   # Check if the df2 is empty or if the obsrvtn column is not numeric
  #   if(nrow(df2) == 0 || !is.numeric(df2$obsrvtn)) {
  #     return(NULL)
  #   }
  #   
  #   # Create the tmap object
  #   tm <- tm_shape(df2) +
  #     tm_polygons("obsrvtn", 
  #                 style = classification, 
  #                 #n = breaks,
  #                 border.col = "black",
  #                 border.lwd = 2,
  #                 palette = "-Spectral",
  #                 title = "Observation") +
  #     tm_layout(title = paste("Sexual Orientation: ", input$so_categories))
  #   
  #   # If the checkbox is checked, add the base map
  #   if(input$base_map_so) {
  #     tm <- tm + tm_basemap(server = "OpenStreetMap")
  #   }
  #   
  #   tm
  # })
  # 
  # output$classification_description <- renderText({
  #   classification_description[[input$class_tmap_so]]
  # })
  # 
  # output$summary_table_so <- renderTable({
  #   # Use the reactive so_data() here
  #   df2 <- so_data()
  #   
  #   # Check if the data frame is empty
  #   if(nrow(df2) == 0) {
  #     return(NULL)
  #   }
  #   
  #   # Convert to a standard data frame
  #   df2 <- as.data.frame(df2)
  #   
  #   summary_df2 <- df2 %>%
  #     rename(Urbanisation2 = urb_rur_so) %>%
  #     group_by(Urbanisation2) %>%
  #     summarise(count = sum(obsrvtn, na.rm = TRUE), .groups = 'drop') %>%
  #     mutate(percentage = count / sum(count) * 100)
  #   
  #   summary_df2 
  # })
  # 
  # output$summary_table_tmap_so <- renderTable({
  #   # Use the reactive so_data() here
  #   df2 <- so_data()
  #   
  #   # Check if the data frame is empty
  #   if(nrow(df2) == 0) {
  #     return(NULL)
  #   }
  #   
  #   # Convert to a standard data frame
  #   df2 <- as.data.frame(df2)
  #   
  #   summary_df2 <- df2 %>%
  #     rename(Urbanisation2 = urb_rur_so) %>%
  #     group_by(Urbanisation2) %>%
  #     summarise(count = sum(obsrvtn, na.rm = TRUE), .groups = 'drop') %>%
  #     mutate(percentage = count / sum(count) * 100)
  #   
  #   summary_df2
  # })
    
}



shinyApp(ui, server)









