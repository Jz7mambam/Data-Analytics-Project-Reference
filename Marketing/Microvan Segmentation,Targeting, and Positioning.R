library(foreign)
library(dplyr)
library(data.table)
library(Hmisc)
library(tidyr)
library(haven)
library(REdaS)
library(grid)
library(psych)
library(gmodels)

mydata <- read_dta('microvan.dta')

vars <- mydata[3:32]

hist(vars,breaks=20)

z1 <- lm(mvliking ~ kidtrans + miniboxy + lthrbetr + secbiggr + safeimpt
         + buyhghnd + pricqual + prmsound + perfimpt + tkvacatn + noparkrm
         + homlrgst +envrminr + needbetw +suvcmpct + next2str +carefmny + shdcarpl
         + imprtapp + lk4whldr + kidsbulk + wntguzlr + nordtrps + stylclth + strngwrn + passnimp + twoincom
         + nohummer + aftrschl + accesfun, data = mydata)

summary(z1)

# Bartlett test of sphericity
bart_spher(mydata[,c('kidtrans','miniboxy','lthrbetr','secbiggr','safeimpt','buyhghnd','pricqual','prmsound','perfimpt',
                   'tkvacatn','noparkrm','homlrgst','envrminr','needbetw','suvcmpct','next2str','carefmny','shdcarpl',
                   'imprtapp','lk4whldr','kidsbulk','wntguzlr','nordtrps','stylclth','strngwrn','passnimp','twoincom',
                   'nohummer','aftrschl','accesfun')])

# Kaiser-Meyer-Olkin Measure of sampling adequacy
KMOS(mydata[,c('kidtrans','miniboxy','lthrbetr','secbiggr','safeimpt','buyhghnd','pricqual','prmsound','perfimpt',
               'tkvacatn','noparkrm','homlrgst','envrminr','needbetw','suvcmpct','next2str','carefmny','shdcarpl',
               'imprtapp','lk4whldr','kidsbulk','wntguzlr','nordtrps','stylclth','strngwrn','passnimp','twoincom',
               'nohummer','aftrschl','accesfun')])

# Factor Analysis: #Explain (Reduction of Variables) - since the construct starts from constructs of interests, we use factor analysis 
# to 'back out' measurements on the underlying factors
#------------------------------
# Determine the number of factors #
#------------------------------

#lthbetr - left-skewed tkvacatn-left skewed    noparkrm-right skewed / carefmny-bimodal / imprapp right skewed / accesfun bimodal / aftrschl-right-skewed

# Create a table of results for ease of interpretation
ev <- eigen(cor(mydata[,c('kidtrans','miniboxy','lthrbetr','secbiggr','safeimpt','buyhghnd','pricqual','prmsound','perfimpt',
                          'tkvacatn','noparkrm','homlrgst','envrminr','needbetw','suvcmpct','next2str','carefmny','shdcarpl',
                          'imprtapp','lk4whldr','kidsbulk','wntguzlr','nordtrps','stylclth','strngwrn','passnimp','twoincom',
                          'nohummer','aftrschl','accesfun')]))$values
e <- data.frame(Eigenvalue = ev, PropOfVar = ev / length(ev), CumPropOfVar = cumsum(ev / length(ev)))

round(e, 4)

# Draw a scree plot 
# Five Factors would suffice
p <- ggplot()
p <- p + geom_line(aes(x = 1:length(ev), y = ev))
p <- p + geom_point(aes(x = 1:length(ev), y = ev))
p <- p + geom_hline(yintercept = 1, colour = "red")
p <- p + labs(x = "Number", y = "Eigenvalues", title = "Scree Plot of Eigenvalues")
p <- p + scale_x_continuous(breaks = 1:length(ev), minor_breaks = NULL)
p <- p + theme_bw()
p

#------------------------------
# Extract solution #
#------------------------------

# Select number of factors
n <- length(which(ev > 1)) 
# This automatically selects the number of factors which have an eigenvalue > 1

# Extract and rotate principal components

pc <- principal(mydata[,c('kidtrans','miniboxy','lthrbetr','secbiggr','safeimpt','buyhghnd','pricqual','prmsound','perfimpt',
                          'tkvacatn','noparkrm','homlrgst','envrminr','needbetw','suvcmpct','next2str','carefmny','shdcarpl',
                          'imprtapp','lk4whldr','kidsbulk','wntguzlr','nordtrps','stylclth','strngwrn','passnimp','twoincom',
                          'nohummer','aftrschl','accesfun')], nfactors = n, rotate="varimax")

# Create a factor loadings table; Sort based on uniqueness
fl <- cbind.data.frame(pc$loadings[,], Uniqueness = pc$uniquenesses)
round(fl[order(pc$uniquenesses),], 4)

# Plot factor loadings
p <- ggplot(data = fl)
p <- p + geom_point(aes(x = RC1, y = RC2), shape = 1, size = 10)
p <- p + geom_text(aes(x = RC1, y = RC2, label = rownames(fl)))
p <- p + geom_hline(yintercept = 0)
p <- p + geom_vline(xintercept = 0)
p <- p + labs(x = "Factor 1", y = "Factor 2", title = "Factor Loadings")
p <- p + theme_bw()
p

# **xxx** marks secondary factor association (factor loadings > 0.35 for a second group)
#RC1: carefmny -0.7634; buyhghnd  0.8147; tkvacatn  0.6539; lthrbetr  0.7107; accesfun  0.6784; lifestyle-luxury-quality-affluent
#     pricqual  0.7823; passnimp -0.6475; stylclth  0.6036; twoincom  0.7562; prmsound  0.6819; imprtapp  0.5094
#RC2: miniboxy 0.8419; suvcmpct  0.8191; homlrgst -0.6794; noparkrm  0.8066; next2str -0.7429; Size/parking/space-saving practicality Seekers
#     secbiggr 0.7593; needbetw 0.7575; nohummer 0.7064;
#RC3: kidtrans 0.9330; nordtrps -0.8665; kidsbulk 0.8248; aftrschl 0.7754; **passnimp -0.3995** family activity/ kids-oriented 
#RC4: safeimpt 0.9075; perfimpt -0.8836; lk4whldr 0.8556; strngwrn 0.7354; safety
#RC5: envrminr -0.8666; shdcarpl 0.8665; wntguzlr -0.7628; **tkvacatn  0.4583;** **accesfun  0.3695** **stylclth 0.4262** environmental-friendliness

# Question 4, Regression with Factor Scores
q4df <- as.data.frame(pc$scores) 
q4df <- cbind(mydata$mvliking,q4df)
z2 <- lm(mydata$mvliking ~ RC1 + RC2 + RC3 + RC4 + RC5, data = q4df)
summary(z2)



#------------------------------
# Segmenting based on factor scores #
#------------------------------

# Print factor scores
pc$scores

# Hierarchical clustering to see number of clusters using dendrogram
d <- dist(pc$scores)
h <- hclust(d, method = "ward.D2")

# view dendogram
plot(h, xlab = "Respondent")

### Conduct k-means clustering on the factor scores

# First, standardize the input variables (z-scores)
z <- scale(pc$scores, center = TRUE, scale = TRUE)

###### 3 clusters #####

# Since the k-means algorithm starts with a random set of centers, setting the seed helps ensure the results are reproducible
set.seed(1)

# Apply K-means clustering with the selected numbers of centers
k3 <- kmeans(z, centers = 3, nstart=25)

# Display cluster sizes
k3$size

# Cluster means
# For ease of interpretation, convert standardized values back to original units
sapply(c("RC1", "RC2","RC3",'RC4','RC5'), function(n) k3$centers[, n]*sd(pc$scores[,n]) + mean(pc$scores[,n]))

# regression of of mvliking on the cluster id categorical variable
mydata <- cbind(mydata, threecluster = k3$cluster)
mydata$threecluster <- as.factor(mydata$threecluster)

summary(lm(mvliking ~ threecluster, data=mydata))

mydata1 <- data.table(mydata)
mydata1[, .(mean_mvliking = round(mean(mvliking), 1)), keyby=.(threecluster)]

#------------------------------
# Describing the segments #
#------------------------------

#######
# age
#######
hist(mydata$age)

agebreaks <- c(0,30,40,50,100)
agelabels <- c("Below 30","30-39","40-49","50-60")

mydata1[ , agegroups := cut(age, breaks = agebreaks, right = FALSE, labels = agelabels)]

CrossTable(x = mydata1$threecluster, y = mydata1$agegroups, expected = TRUE, prop.r = FALSE, prop.c = FALSE, prop.t = FALSE)

#######
# income
#######

hist(mydata$income)

incomebreaks <- c(0,50,100,500)
incomelabels <- c("Below $50,000","$50,000-$99,999","$100,000 and above")

mydata1[ , incomegroups := cut(income, breaks = incomebreaks, right = FALSE, labels = incomelabels)]

CrossTable(x = mydata1$threecluster, y = mydata1$incomegroups, expected = TRUE, prop.r = FALSE, prop.c = FALSE, prop.t = FALSE)

#######
# miles
#######

hist(mydata$miles)

milesbreaks <- c(0,15,20,100)
mileslabels <- c("Below 15,000 miles","15,000 - 19,999 miles","20,000 miles and above")

mydata1[ , milesgroups := cut(miles, breaks = milesbreaks, right = FALSE, labels = mileslabels)]

CrossTable(x = mydata1$threecluster, y = mydata1$milesgroups, expected = TRUE, prop.r = FALSE, prop.c = FALSE, prop.t = FALSE)

#######
# numkids
#######

hist(mydata$numkids)

numkidsbreaks <- c(0,1,2,3,10)
numkidslabels <- c("No kid","1 kid","2 kids","3 or 4 kids")

mydata1[ , numkidsgroups := cut(numkids, breaks = numkidsbreaks, right = FALSE, labels = numkidslabels)]

CrossTable(x = mydata1$threecluster, y = mydata1$numkidsgroups, expected = TRUE, prop.r = FALSE, prop.c = FALSE, prop.t = FALSE)

#######
# female
#######

hist(mydata$female)

CrossTable(x = mydata1$threecluster, y = mydata1$female, expected = TRUE, prop.r = FALSE, prop.c = FALSE, prop.t = FALSE)

#######
# educ
#######

hist(mydata$educ)

educbreaks <- c(1,2,3,4,5)
educlabels <- c("High School","Some College","Undergraduate Degree", "Graduate Degree")

mydata1[ , educgroups := cut(educ, breaks = educbreaks, right = FALSE, labels = educlabels)]

CrossTable(x = mydata1$threecluster, y = mydata1$educgroups, expected = TRUE, prop.r = FALSE, prop.c = FALSE, prop.t = FALSE)

#######
# recycle
#######

hist(mydata$recycle)

recyclebreaks <- c(1,3,4,6)
recyclelabels <- c("Below average","Average","Above average")

mydata1[ , recyclegroups := cut(recycle, breaks = recyclebreaks, right = FALSE, labels = recyclelabels)]

CrossTable(x = mydata1$threecluster, y = mydata1$recyclegroups, expected = TRUE, prop.r = FALSE, prop.c = FALSE, prop.t = FALSE)