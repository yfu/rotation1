setwd("/Users/yfu/Dropbox/Courses/Rotation/results/2012-12-07/HaibTfbsGm12878Tcf12Pcr1xAlnRep0")
# How to plot p-values of hyper and binom:
dev.new()
binom = read.table("binom_p_value.txt", header=F)
hyper = read.table("hyper_p_value.txt", header=F)
binom.x = binom$V1
binom.y = binom$V2
hyper.x = hyper$V1
hyper.y = hyper$V2


# First plot
plot(hyper.x, log(hyper.y), ylim=c(-12, -3), pch=16, axe=FALSE, xlab="", ylab="", type="b", col="black", main="HaibTfbsGm12878Tcf12Pcr1xAlnRep0 GO:0019956
log p-values of binom and hyper")
axis(2, ylim=c(-12, -3), col="black")
mtext("log p-value of hyper", side=2, line=2.5)
box()
par(new=T)
log()

# Second plot
plot(binom.x, log(binom.y), pch=15, xlab="", ylab="", ylim=c(-75,0), axe=FALSE, type="b", col="red")
mtext("log p-value of binom", side=4, col="red", col.axis="red", line=2.5)

axis(4, ylim=c(-75, 0), col="red", col.axis="red")

axis(1, binom.x)

mtext("strength", side=1, col="black", line=2.5)

legend(0.25, -4, legend=c("p-value of binom", "p-value of hyper"), text.col=c("black", "red"), pch=c(16,15), col=c("black", "red"))

dev.new()

plot(binom.x, log(hyper.y/binom.y), pch=16, ylim=c(0, 70), axe=FALSE , type="b", col="black", main="HaibTfbsGm12878Tcf12Pcr1xAlnRep0 GO:0019956
log (p-value of hyper over p-value of binom)")

# x axis
axis(1, binom.x)
axis(2, 0:70)

mtext("Strength", side=1, col="black", line=2.5)
# mtext("log(hyper.y/binom.y)", side=2, col="black", line=2.5)
