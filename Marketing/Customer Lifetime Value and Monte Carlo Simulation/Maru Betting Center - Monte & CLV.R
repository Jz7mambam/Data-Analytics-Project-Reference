
# Group Assignment 2 Hint 
# Maru Batting 
# prepared by Yanwen WANG
library(stringr)
library(ggplot2)
library(scales)
library(grid)
library(gridExtra)

# SET WORKING DIRECTORY
setwd("~/DEV/UBC/data/UBC_group/BAMA_520/assignment_2")
# READ DATA
maru.data<-read.csv("maru_data.csv")


#############################################################
# Answers to Part I
# CALCULATE ANNUAL MARGIN
maru.data$total.cost.per.hr<-maru.data$instructor.labor.cost.per.hr* maru.data$instructors.needed + maru.data$worker.labor.cost.per.hr* maru.data$workers.needed
maru.data$margin.hr<-maru.data$price.per.hr-maru.data$total.cost.per.hr
maru.data$annual.margin<-maru.data$margin.hr*maru.data$annual.hours


# answer to question 1 on page 5
# CALCULATE ACQUISITION COST
maru.data$acquisition.cost<-maru.data$contact.cost/maru.data$response.rate
maru.data$acquisition.cost


# answer to question 2
# BREAKEVEN WITHOUT DISCOUNTING
maxperiod = 6
period = seq(1,maxperiod)

cf = matrix(0,nrow=5,ncol=maxperiod)
npv = matrix(0,nrow=5,ncol=maxperiod)

for (t in 1:maxperiod){
  cf[,t] = maru.data$annual.margin*maru.data$retention.rate^(t-1)
  npv[,t] = rowSums(as.matrix(cf[,1:t])) - maru.data$acquisition.cost
}

# print out cash flow matrix 
cf
# print out npv to see since which period the npv>=0
npv
# you can try the following instead of eyeballing
apply(npv,1, function(x) which.max(x>=0))



# PROBLEM 3: COMPUTE CLV (ASSUMING INFINITE TIME HORIZON)
# Net CLV = (M * ( (1+i) / (1 + i - R))) - AC Using formula #1
# Create a new column with CLV assuming numbers from case
maru.data$clv <- (maru.data$annual.margin* ((1+maru.data$interest.rate) / (1 + maru.data$interest.rate - maru.data$retention.rate))) - maru.data$acquisition.cost



# PROBLEM 5: CHIYODA WARD
clv.littleleaguers.now<-maru.data[maru.data$X=="little leaguers",]$clv
clv.littleleaguers.chiyoda<-5000*(1+.1)/(1+.1-.65)-(600/.08)
clv.littleleaguers.now
clv.littleleaguers.chiyoda



# PROBLEM 6: ELITE BALLPLAYERS DISCOUNT
#clv_yr1 = 7500*20
clv_onward = ((7000-6000)*20*1.1)/(1.1-0.75); clv_onward
clv_elite = clv_onward + 500*20 - 50000; clv_elite



# PROBLEM 7: ELITE BALLPLAYERS BAT

acquisition_new = 12500 / 0.29 + 10000; acquisition_new
clv_new = (7500-6000)*20*1.1 / (1.1-0.6) - acquisition_new; clv_new
diff_clv = 16000 - clv_new; diff_clv

##########################################################
# Answers to Part II
# SENSITIVITY ANALYSIS (pls follow the hints below)

# creates scenario values
# try use seq() to create a series of number for parameters AC, M, and R
ac <- seq(from = 40000, to = 60000, by = 5000) #50000
am <- seq(from = 24000, to = 36000, by = 3000) #30000
rr <- seq(from = 0.48, to = 0.72, by = 0.06) #0.6

# try use expand.grid to create a full matrix for all the possible combinations of AC, M, and R
values <- expand.grid(ac=ac,am=am,rr=rr)
values$i <- 0.10

# computes CLV for all scenarios

values$clv <-values$am*(1+values$i)/(1+values$i-values$rr)
values$nclv <- values$clv - values$ac
# visualization using scatter.smooth, for example
scatter.smooth(x=values$ac, y=values$clv)
scatter.smooth(x=values$ac, y=values$nclv)
# you can use scatter.smoooth to plot out the relationships between, for example, AC and CLV

#computes CLV for all scenarios
#if(values$nclv<0){values$neg_nclv = 'neg'}else{values$neg_nclv = 0}

num_neg <- sum(values$nclv<0)
num_neg

clv_ll<-15714.28571-10000 #minus ac
num_less_ll <- sum((values$nclv - clv_ll) <0)

freq_ll <- num_less_ll/nrow(values); freq_ll

####variation in each of the three variables changes CLV
#### set up the steps
ac1 <- seq(from = 40000, to = 60000, by = 5000) # 50000
am1 <- seq(from = 24000, to = 36000, by = 3000)  # 30000
rr1 <- seq(from = 0.48, to = 0.72, by = 0.06) # 0.6

#ac <- seq(from = 45000, to = 55000, by = 1000) 
table_ac <- expand.grid(ac=ac1,am=30000,rr=0.6,i=0.1)
table_am <- expand.grid(ac=50000,am=am1,rr=0.6,i=0.1)
table_rr <- expand.grid(ac=50000,am=30000,rr=rr1,i=0.1)

###calculate nclv
table_ac$nCLV <- (table_ac$am* ((1+table_ac$i) / (1 + table_ac$i - table_ac$rr)))- table_ac$ac
table_am$nCLV <- (table_am$am* ((1+table_am$i) / (1 + table_am$i - table_am$rr)))- table_am$ac
table_rr$nCLV <- (table_rr$am* ((1+table_rr$i) / (1 + table_rr$i - table_rr$rr)))- table_rr$ac

#### plot the graph
plot(x=table_ac$ac, y=table_ac$nCLV, pch=20, type='l', main = 'Net CLV vs Acquisition Cost', xlab = 'Acquisition Cost', ylab = 'Net CLV')
plot(x=table_am$am, y=table_am$nCLV, pch=20, type='l', main = 'Net CLV vs Annual Margin', xlab = 'Annual Margin', ylab = 'Net CLV')
plot(x=table_rr$rr, y=table_rr$nCLV, pch=20, type='l', main = 'Net CLV vs Retention Rate', xlab = 'Retention Rate', ylab = 'Net CLV')



##########################################################
# Answers to Part III
elite.ballplayers<-maru.data[4 ,]
elite.ballplayers.subset<-subset(elite.ballplayers, select = c("acquisition.cost","annual.margin","retention.rate"))
elite.ballplayers.subset<-data.matrix(elite.ballplayers.subset)


#CLV for elite ballplayers calcuated using aggregate values
elite.ballplayers.clvaggregate<-maru.data$clv[4]


run_simulation = function(p) {
  # Set Seed for Random Number Generation
  set.seed(123456)
  
  #load("customers.rdata")
  #hist(customers)
  load("customers.rdata")
  hist(customers)
  customers = get(load("customers.rdata"))
  margin.mean<-mean(customers)
  margin.sd<-sd(customers)
  
  acquisition_cost = 50000
  interest_rate = 0.1
  
  
  d<- 0.1
  ac<-elite.ballplayers.subset[1]
  m<-elite.ballplayers.subset[2]
  r<-elite.ballplayers.subset[3]
  
  num.samples=10000
  
  d.vec<-rep(d, num.samples)
  ac.vec<-rep(ac, num.samples)
  m.vec<-rnorm(num.samples,margin.mean,margin.sd)
  
  # Next use Beta distribution to determine retention rate value
  
  # MEAN = 0.6, MEAN = p / (p + q)
  
  r_u = 0.6
  q = (p - r_u * p) / r_u
  r.vec = rbeta(num.samples, p, q)
  
  # Now insert the simulated retention rate into the CLV formula 
  clv.vec = m.vec * (1.1 / (1.1 - r.vec)) - acquisition_cost
  clv.vec = sort(clv.vec, decreasing = TRUE)
  #Create "Whale Plot" to depict value concentration
  # the key is to sort customers by their CLV
  # use plot()
  
  breaks = seq(min(clv.vec), max(clv.vec), by=length(clv.vec) / 500)
  clv_cut = cut(clv.vec, breaks, right=FALSE)
  clv_freq = table(clv_cut)
  cumfreq = c(0, cumsum(clv_freq)/length(clv_cut))
  
  
  monte_carlo_stats = str_interp("CLV Stats: Mean ${round(mean(clv.vec))}, Standard Deviation ${round(sd(clv.vec))}, Min ${round(min(clv.vec))}, Max ${round(max(clv.vec))}")
  
  print(monte_carlo_stats)
  
  whale_bins = seq(from = 0, to = num.samples, by = 100)
  whale_plot_data = x <- as.data.frame(matrix(nrow = length(whale_bins), ncol = 2))
  
  total_profit = sum(clv.vec)
  counter = 1
  for (i in whale_bins){
    cumulative_sum = sum(clv.vec[1:i])
    profit_percentage = cumulative_sum / total_profit
    percentage_customer = i / num.samples
    whale_plot_data$V1[counter] = percentage_customer
    whale_plot_data$V2[counter] = profit_percentage
    counter = counter + 1
    #print(str_interp("i: ${i} profit: ${profit_percentage} cumulative sum: ${cumulative_sum}"))
  }
  
  whale_plot = ggplot(data=whale_plot_data, aes(x=V1, y=V2)) + geom_line() + 
    labs(x = "Cumulative Percentage of Customers", y='Cumulative Profits(%)',
         title="Whale Plot of 10000 Customers", caption=monte_carlo_stats) + scale_y_continuous(breaks = seq(0, 1, by = 0.2))
  
  
  pdf_plot = ggplot(data=data.frame(r.vec), aes(x=r.vec)) + geom_histogram(bins = 30) + 
    labs(x = "Retention Rate", y='Count',
         title="Histogram of 10000 Customer Retentions",
         subtitle = str_interp("Beta Distribution with Alpha = ${p} Beta = ${q}"),
         caption = str_interp("Retention Rate Mean = ${round(mean(r.vec) * 100)}%"))
  
  pdf_plot_margin = ggplot(data=data.frame(m.vec), aes(x=m.vec)) + geom_histogram(bins = 30) + 
    labs(x = "Annual Margin", y='Count',
         title="Histogram of 10000 Customer Annual Margins",
         subtitle = str_interp("Normal Distribution with Mean = ${round(margin.mean)} SD = ${round(margin.sd)}"))
  
  
  cdf_plot = ggplot(data.frame(breaks, cumfreq), aes_string(x=breaks, y=cumfreq)) + geom_line() +
    labs(x = "CLV Values", y='Cumulative Percentage',
         title="Cumulative Distribution of Customers") + 
    scale_x_continuous(labels = comma)+ scale_y_continuous(breaks = seq(0, 1, by = 0.2))
  
  grid.arrange(whale_plot, cdf_plot, pdf_plot, pdf_plot_margin, nrow = 2)

}

run_simulation(156)
run_simulation(3)
run_simulation(0.3)

