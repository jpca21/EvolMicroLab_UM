#### Updated at Jan 14, 2022
#### Script recommended to be used in RStudio

library(pheatmap)
#library(vegan) ### if you want to use PCoA from data
#library(funrar) ### if you want to use  `make_relative``

##################################################################################################################
data  <- read.table("matrix.tsv", 
                    header = T, sep = "\t", comment.char = "", check.names = F)
### backup
olddata <- data

### Optional: change the "-" character for a dot (if the names contain any "-")
#colnames(data) <- gsub('-', '.', colnames(data))

### rownames will be assigned to the cluster name
rownames(data) <- data$Group
### remove the first column
data <- data[,-1]

### Optional: if you don't need a colum
### this is for remove it (`uselessCol` is your target column)
#data$uselessCol <- NULL

### Transpose table (Genomes will have to be the rows)
tdata <- t(data)
tdata <- as.data.frame(tdata)

#### Now, we convert our dataset into a binary matrix (0 / 1)
binary_tdata <- as.matrix((tdata > 0) + 0) ### making binary
binary_tdata <- as.data.frame(binary_tdata)
binary_data  <- t(binary_tdata)

##################################################################################################################

##################################################################################################################
##### Now, let's use a list for descriptions for Sample Labels

##### Open datalabels (metadata.tsv need to have only two columns: the name i the original dataset
##### and the new label)

dataLabels  <- read.table("metadata.tsv", 
                          header = T, sep = "\t", comment.char = "")
colnames(dataLabels) <- c("NAME","LABEL")
### Optional: change the "-" character for a dot (if the names contain any "-")
dataLabels$NAME <- gsub('-', '.', dataLabels$NAME)

#### Change rownames, maing match with names in datalabels (for the binary trasposed matrix)
rownames(binary_tdata) <- gsub('-', '.', rownames(binary_tdata))
binary_tdata_v2 <- cbind(neoname = dataLabels$LABEL[ match(rownames(binary_tdata),dataLabels$NAME) ],
      binary_tdata)
rownames(binary_tdata_v2) <- binary_tdata_v2$neoname
binary_tdata_v2$neoname <- NULL


##################################################################################################################
#### SUPERHEATMAP (binary matrix, including new labels)
K <- pheatmap(binary_tdata_v2,
              border_color=NA,
              clustering_method="complete",
              show_rownames = T,
              show_colnames = F,
              fontsize_col = 1,
              fontsize_row = 10,
              annotation_legend=F,
              cutree_rows = 1,
              cutree_cols = 1)
K

##################################################################################################################
#### END
