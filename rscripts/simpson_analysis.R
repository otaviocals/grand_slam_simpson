##############################
#    Retrieving arguments    #
##############################

myArgs <- commandArgs(trailingOnly = TRUE)
data_folder <- myArgs[1]
if(length(myArgs)>=2)
    {
        r_libs <- myArgs[2]
    }else{
        r_libs <- .libPaths()[1]
    }

setwd(data_folder)

if(Sys.info()['sysname']=="Windows")
    {
        slash <- "\\"
    }else{
        slash <- "/"
    }


#Loading libraries

package_list <- c("Rcpp","openxlsx","bindrcpp","dplyr","reshape2")
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

simpson_table <- win_rate_league[,2:5]

for (i in 1:4)
{
    simpson_table[,i] <- abs(win_rate_league[,i+1]-win_rate_simple[,2])>=0.5
}
simpson_table <- cbind.data.frame(as.character(win_rate_league[,1]),simpson_table)
colnames(simpson_table)[1] <- "Player1"

paradox_cases <- which(simpson_table[,2:5]==TRUE,arr.ind=TRUE)
paradox_cases <- cbind.data.frame(simpson_table[paradox_cases[,1],1],
                 colnames(simpson_table)[paradox_cases[,2]+1])
colnames(paradox_cases) <- c("Player","Tournament")
paradox_cases <- paradox_cases[order(paradox_cases$Player,paradox_cases$Tournament),]
rownames(paradox_cases) <- as.character(1:nrow(paradox_cases))


###################
# Printing Result #
###################


if(nrow(paradox_cases)>0)
    {
        cat("\n\nSimpson's Paradox detected in the following case:\n\n")
        print(paradox_cases)
        cat(paste0("\n\nTotal number of instaces: ",nrow(paradox_cases),"\n\n"))
    }else{
        cat("No occurrences of the Simpson's Paradox")
    }


###################
# Exporting Data  #
###################

workbook <- createWorkbook()
write.csv(win_rate_simple,paste0("proc_data",slash,"win_rate_simple.csv"))
addWorksheet(workbook,"grand_slam_data")
writeDataTable(workbook,"grand_slam_data",grand_slam_data)
addWorksheet(workbook,"win_rate_simple")
writeDataTable(workbook,"win_rate_simple",win_rate_simple)
write.csv(win_rate_league,paste0("proc_data",slash,"win_rate_league.csv"))
addWorksheet(workbook,"win_rate_league")
writeDataTable(workbook,"win_rate_league",win_rate_league)
write.csv(paradox_cases,paste0("proc_data",slash,"paradox_cases.csv"))
addWorksheet(workbook,"simpson_paradox")
writeDataTable(workbook,"simpson_paradox",paradox_cases)
saveWorkbook(workbook,paste0("proc_data",slash,"grand_slam_simpson_analysis.xlsx"),overwrite=TRUE)
