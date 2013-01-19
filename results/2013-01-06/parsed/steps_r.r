setwd("/Users/yfu/Dropbox/Courses/Rotation/results/2013-01-06/parsed");
library(gplots);
## This will create heatmaps for bionomial p-values and
## hypergeometric p-values

binomp <- read.table(file="table_100_binomp.txt", header = TRUE);

hyperp <- read.table(file= "table_100_hyperp.txt", header=TRUE);

# Convert the data frames to matrices
b.matrix <- do.call(cbind, binomp);
# Assign the rownames (i.e. the names of the TFs)
rownames(b.matrix) <- rownames(binomp);
# Do the same to hypergeometric p value
h.matrix <- do.call(cbind, hyperp);
rownames(h.matrix) <- rownames(hyperp);

# Though all the GO temrs that I chose are the most common ones,
# some TFs still do not have enrichment in these TFs. As a result,
# in the heatmap of the original p-values, there are a lot of 1s
# and in the heatmap of the minus log p-values, there are a lot
# of Inf's. So I will replace these Inf's with the average of
# the whole matrix.

b.matrix.minus.log <- -log(b.matrix);
h.matrix.minus.log <- -log(h.matrix);


b.matrix.minus.log[is.infinite(b.matrix.minus.log)] <- NA;
b.matrix.minus.log[is.nan(b.matrix.minus.log)] <- NA;

b.matrix.minus.log[is.na(b.matrix.minus.log)] <- mean(b.matrix.minus.log[!is.na(b.matrix.minus.log)]);
h.matrix.minus.log[is.na(h.matrix.minus.log)] <- mean(h.matrix.minus.log[!is.na(h.matrix.minus.log)]);

h.matrix.minus.log[h.matrix.minus.log==0] <- mean(h.matrix.minus.log[!is.infinite(h.matrix.minus.log)])
b.matrix.minus.log[b.matrix.minus.log==0] <- mean(b.matrix.minus.log[!is.infinite(b.matrix.minus.log)])
# Use heatmap.2 from gplots instead.

# For the colors on both sides
# Use ColSideColors
# Sadly, that is not possible since I need a vector of length of 100...

pdf("binom_p_value_large.pdf", width = 7, height=20);
## heatmap.2(b.matrix.minus.log, trace="none", lhei=c(1,15), cexRow = 0.25)
heatmap.2(b.matrix.minus.log, cexRow = 0.25,cexCol = 0.25, col=redgreen, trace="none", lhei=c(1,15));
# Save the heatmap since I want to get the names of rows and columns later
a <- heatmap.2(b.matrix.minus.log, cexRow = 0.25,cexCol = 0.25, col=redgreen, trace="none", lhei=c(1,15));
dev.off();

# Prevent those very significant GO terms from masking other GO terms
# so, just select half of them. Sweet, huh?
pdf("biomial_p_value_large_exclusing the most significant 50 GO terms.pdf", width = 7, height= 20);
cols <- a$colInd;
cols <- cols[51:100];
# I'll remove the most significant 50 GO terms
b.go.terms.less.sig <- b.matrix.minus.log[,cols];
heatmap.2(b.go.terms.less.sig, cexRow = 0.25, cexCol = 0.45, col=redgreen, trace="none", lhei=c(1,15));
dev.off();

pdf("binom_p_value_normal.pdf");
heatmap.2(b.matrix.minus.log, col=redgreen, trace="none");
dev.off();

pdf("hyper_p_value_large.pdf", width = 7, height=20);
## heatmap.2(h.matrix.minus.log, trace="none", lhei=c(1,15), cexRow = 0.25)
heatmap.2(h.matrix.minus.log, cexRow = 0.25, cexCol = 0.25, col=redgreen, trace="none", lhei=c(1,15));
# Save the heatmaps since I want to get the names of rows and columns later
b <- heatmap.2(h.matrix.minus.log, cexRow = 0.25, cexCol = 0.25, col=redgreen, trace="none", lhei=c(1,15));
dev.off();

# Prevent those very significant GO terms from masking other GO terms
# Remove 50 most significant GO terms
pdf("hyper_p_value_large_excluding the most significant 50 GO terms.pdf", width = 7, height = 20);
cols <- b$colInd;
cols <- cols[51:100];
h.go.terms.less.sig <- h.matrix.minus.log[,cols];
heatmap.2(h.go.terms.less.sig, cexRow = 0.25, cexCol = 0.45, col=redgreen, trace="none", lhei=c(1,15));
dev.off();

pdf("hyper_p_value_normal.pdf");
heatmap.2(h.matrix.minus.log, col=redgreen, trace="none");
dev.off()

# Choose between the corresponding elements in the matrices the lower one
b.smaller.than.h = b.matrix.minus.log < h.matrix.minus.log;
b.larger.than.h = b.matrix.minus.log > h.matrix.minus.log;

min.minus.log = b.matrix.minus.log;
min.minus.log [b.smaller.than.h] = b.matrix.minus.log [b.smaller.than.h];
min.minus.log [b.larger.than.h] = h.matrix.minus.log [b.larger.than.h];

pdf("combined-min-minus-log.pdf", width = 7, height = 20);
heatmap.2(min.minus.log, cexRow = 0.25, cexCol = 0.25, col = redgreen, trace = "none", lhei=c(1,15));
dev.off();

# Choose between the corresponding elements in the matrices the higher one
max.minus.log = b.matrix.minus.log;
max.minus.log [b.larger.than.h] = b.matrix.minus.log [b.larger.than.h];
max.minus.log [b.smaller.than.h] = b.matrix.minus.log [b.smaller.than.h];

pdf("combined-max-minus-log.pdf", width = 7, height = 20);
heatmap.2(max.minus.log, cexRow = 0.25, cexCol = 0.25, col = redgreen, trace = "none", lhei = c(1,15));
dev.off();
