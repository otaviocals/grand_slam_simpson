##############################
#    Retrieving arguments    #
##############################

myArgs <- commandArgs(trailingOnly = TRUE)
slash <- myArgs[1]
data_folder <- myArgs[2]
r_scripts <- myArgs[3]
r_libs <- myArgs[4]
log_file <- myArgs[5]

setwd(data_folder)

#Loading libraries

package_list <- c("Rcpp","openxlsx","dplyr","reshape2")
suppressWarnings(suppressMessages(
	for( i in 1:length(package_list))
	{
		if (!require(package_list[i],character.only = TRUE,lib.loc=r_libs))
    			{
		      	install.packages(package_list[i],dep=TRUE,repos="http://cran.us.r-project.org",lib=r_libs)
			        if(!require(package_list[i],character.only = TRUE,lib.loc=r_libs)) stop("Package not found")
			}
	}           ))



###################
#    Read CSV     #
###################


grand_slam_data <- read.csv(paste0("data",slash,"grand_slam.csv"))

###################
# Processing Data #
###################

by_player <- group_by(grand_slam_data,Player1)
win_rate_simple <- summarize(by_player,win_rate=sum(as.integer(
                                    as.character(Win)=="True"))/
                                    (sum(as.integer(as.character(Win)=="True"))+
                                    sum(as.integer(as.character(Win)=="False"))))

by_league <- group_by(grand_slam_data,Tournament,Player1,)
win_rate_league <- summarize(by_league,win_rate=sum(as.integer(
                                    as.character(Win)=="True"))/
                                    (sum(as.integer(as.character(Win)=="True"))+
                                    sum(as.integer(as.character(Win)=="False"))))
win_rate_league <- dcast(win_rate_league,Player1~Tournament,value.var="win_rate")

###################
# Exporting Data  #
###################

workbook <- createWorkbook()
addWorksheet(workbook,"win_rate_simple")
writeDataTable(workbook,"win_rate_simple",win_rate_simple)
addWorksheet(workbook,"win_rate_league")
writeDataTable(workbook,"win_rate_league",win_rate_league)
saveWorkbook(workbook,paste0("proc_data",slash,"grand_slam_simpson_analysis.xlsx"),overwrite=TRUE)
