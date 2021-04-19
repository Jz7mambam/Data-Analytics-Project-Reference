library(data.table)
library(pROC)
library(dplyr)
library(ggplot2)

setwd("~/DEV/UBC/data/UBC_group/BAMA_520/assignment_3")

pb_data <- fread('pilgrimBdata.csv')
pb_data

#create the table of all the cumulative profit
profit_total <- sum(pb_data$Profit99)
customer_id <- pb_data$ID
profit_customer <- pb_data$Profit99

whale.data <- data.table(cid = customer_id, i_profit= profit_customer, s_profit= profit_total)
str(whale.data)

sort.whale <- whale.data[order(whale.data$i_profit, decreasing = TRUE),]

tail(sort.whale)

sort.whale$c_profit <- cumsum(sort.whale$i_profit)
sort.whale$pc_profit <- sort.whale$c_profit/sort.whale$s_profit

n_rows <- nrow(sort.whale)
n_rows

sort.whale$pc_customer <- as.numeric(rownames(sort.whale))/n_rows 

#plot(pc_profit ~ pc_customer, data = sort.whale, main = 'Whale Curve', xlab = '% of customer', ylab = '% of cumulative profit',cex.lab = 0.8,cex.axis=0.8,cex.main = 0.9)

ggplot(data=sort.whale, aes(x=pc_customer, y=pc_profit)) + geom_line() + 
  labs(x = '% of customer', y='% of cumulative profit',
       title='Whale Curve') +  scale_y_continuous(labels = scales::percent) + 
  scale_x_continuous(labels = scales::percent)



#q2 a
q2.a <- sort.whale[round(pc_profit,4) == 1.00][i_profit >0]
q2.a

#q2 b
q2.b <-sort.whale[pc_profit == max(pc_profit)][i_profit != 0][,"pc_customer"]
q2.b

#q3

z1 <- lm(sort.whale$i_profit ~ 1)
summary(z1)
confint(z1)


#q4
#Mod1: Profit99 ~ Online99 + Age + Inc + Tenure99 + as.factor(District99)
m1 <- lm(pb_data$Profit99 ~ pb_data$Online99 + pb_data$Age99 + pb_data$Inc99 + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m1)
confint(m1)

#Mod2: Profit99 ~ Online99 + AgeMean + IncMean + Tenure99 + as.factor(District99)
pb_data$AgeMean <- ifelse(is.na(pb_data$Age99), mean(pb_data$Age99,na.rm = TRUE), pb_data$Age99)
pb_data$IncMean <- ifelse(is.na(pb_data$Inc99), mean(pb_data$Inc99,na.rm = TRUE), pb_data$Inc99)

m2 <- lm(pb_data$Profit99 ~ pb_data$Online99 + pb_data$AgeMean + pb_data$IncMean + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m2)

#Mod3: Profit99 ~ Online99 + AgeZero + IncZero + Tenure99 + as.factor(District99)

pb_data$AgeZero <- ifelse(is.na(pb_data$Age99),0,pb_data$Age99)
pb_data$IncZero <- ifelse(is.na(pb_data$Inc99),0,pb_data$Inc99)

m3 <- lm(pb_data$Profit99 ~ pb_data$Online99 + pb_data$AgeZero  + pb_data$IncZero + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m3)
#Mod4: Profit99 ~ Online99 + AgeMiss + AgeMean + IncMiss + IncMean + Tenure99 + as.factor(District99)

pb_data$AgeMiss <- ifelse(is.na(pb_data$Age99),1, 0)
pb_data$IncMiss <- ifelse(is.na(pb_data$Inc99),1,0)

#head(pb_data)

m4 <- lm(pb_data$Profit99 ~ pb_data$Online99 +  pb_data$AgeMean + pb_data$IncMean + pb_data$AgeMiss + pb_data$IncMiss  + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m4)
#Mod5: Profit99 ~ Online99 + AgeMiss + AgeZero + IncMiss + IncZero + Tenure99 + as.factor(District99)

m5 <- lm(pb_data$Profit99 ~ pb_data$Online99  + pb_data$AgeZero + pb_data$IncZero + pb_data$AgeMiss + pb_data$IncMiss + pb_data$Tenure99 + as.factor(pb_data$District99))


summary(m5)

#Mod6: Profit99 ~ Online99 + AgeMiss + AgeZero + IncMiss + I(log(IncZero+1)) + Tenure99 + as.factor(District99)

m6 <- lm(pb_data$Profit99 ~ pb_data$Online99  + pb_data$AgeZero + I(log(pb_data$IncZero +1)) + pb_data$AgeMiss + pb_data$IncMiss  + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m6)

##################
#consider 'Age' 'Income' as categorical data
m1.c <- lm(pb_data$Profit99 ~ pb_data$Online99 + as.factor(pb_data$Age99) + as.factor(pb_data$Inc99) + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m1.c)

m2.c <- lm(pb_data$Profit99 ~ pb_data$Online99 + as.factor(pb_data$AgeMean) + as.factor(pb_data$IncMean) + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m2.c)

m3.c <- lm(pb_data$Profit99 ~ pb_data$Online99 + as.factor(pb_data$AgeZero)  + as.factor(pb_data$IncZero) + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m3.c)

m4.c <- lm(pb_data$Profit99 ~ pb_data$Online99 + as.factor(pb_data$AgeMiss) + as.factor(pb_data$AgeMean) +as.factor(pb_data$IncMiss) +as.factor(pb_data$IncMean) + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m4.c)

m5.c <- lm(pb_data$Profit99 ~ pb_data$Online99 + as.factor(pb_data$AgeMiss) + as.factor(pb_data$AgeZero) +  as.factor(pb_data$IncMiss) + as.factor(pb_data$IncZero) + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m5.c)


m6.c <- lm(pb_data$Profit99 ~ pb_data$Online99 + as.factor(pb_data$AgeMiss) + as.factor(pb_data$AgeZero) +  as.factor(pb_data$IncMiss) +I(log(pb_data$IncZero +1)) + pb_data$Tenure99 + as.factor(pb_data$District99))

summary(m6.c)

##################



#question 6  
#Take Age and Income as continuous variables; use the dummy plus zero replacement approach to deal with missing data) 

z2 <- lm(pb_data$Profit00 ~ pb_data$Online99 + pb_data$AgeMiss + pb_data$IncMiss + pb_data$AgeZero + pb_data$IncZero)
summary(z2)

z2.c <- lm(pb_data$Profit00 ~ pb_data$AgeMiss + pb_data$IncMiss + pb_data$AgeZero + pb_data$IncZero)
summary(z2.c)

#z2 <- lm(pb_data$Profit00 ~ pb_data$Online99 + pb_data$Age99 + pb_data$Inc99 + pb_data$AgeZero + pb_data$IncZero)
#summary(z2)

#question 7 

stay_or_not <- ifelse(is.na(pb_data$Profit00),0, 1)
#str(stay_or_not)

z3 <- glm(stay_or_not ~ pb_data$Online99 +pb_data$AgeMiss + pb_data$IncMiss + pb_data$AgeZero + pb_data$IncZero, family = binomial(link="logit"))
summary(z3)

#remove online99 in z3_2
z3_2 <- glm(stay_or_not ~ pb_data$AgeMiss + pb_data$IncMiss + pb_data$AgeZero + pb_data$IncZero, family = binomial(link="logit"))
summary(z3_2)

# 

#stay_prob <- predict(z3,type="response")
pb_data$stay.pred <- predict(z3,type="response")
pb_data$stay.pred_2 <- predict(z3_2,type="response")

pb_data.roc <- roc(stay_or_not, pb_data$stay.pred, percent=T)
pb_data.roc_2 <- roc(stay_or_not, pb_data$stay.pred_2, percent=T)
#auc(pb_data.roc)
#plot(pb_data.roc,smooth=T)
coords(pb_data.roc,"best","specificity",transpose = F)
coords(pb_data.roc_2,"best","specificity",transpose = F)

pb_data$stay.pred.retained <- ifelse(pb_data$stay.pred>=0.7781521, 1, 0)
pb_data$stay.pred.retained_2 <- ifelse(pb_data$stay.pred>=0.7666629, 1, 0)
#pb_data$stay.pred.retained <- ifelse(pb_data$stay.pred>=0.7675995, 1, 0) # without online99
confusion_matrix_1 <- table(stay_or_not,pb_data$stay.pred.retained)
confusion_matrix_2 <- table(stay_or_not,pb_data$stay.pred.retained_2)

confusion_matrix_1
confusion_matrix_2

#data[, FlorenceProb := predict(mod2,type="response")]
head(pb_data)

#y variable: 
#stay_or_not: if  NA--> 0 (left the bank); not NA -->1 (stay with bank);

hit.rate <- (3442+21651)/(3442+21651+4745+1786)
hit.rate

hit_rate_2 = (3424 + 21728) / (3424 + 21728 + 4668 + 1814)
hit_rate_2








