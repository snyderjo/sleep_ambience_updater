require(rmarkdown)

find_pandoc()

render("weeklyReport.Rmd")
render("index.Rmd")