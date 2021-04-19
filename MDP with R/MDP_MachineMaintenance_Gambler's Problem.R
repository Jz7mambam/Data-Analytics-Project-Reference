library(MDPtoolbox)

#maintenance Action
t_maintenance=matrix(c( 0.6, 0.4,
                        1, 0),
                nrow=2,ncol=2,byrow=TRUE)

#no maintenance Action
t_no_maintenance=matrix(c(0.35, 0.65,
                          1, 0),
              nrow=2,ncol=2,byrow=TRUE)

#repair Action
t_repair=matrix(c(1, 0,
                  0.6, 0.4),  
                  nrow=2,ncol=2,byrow=TRUE)

#replace Action
t_replace=matrix(c(1, 0,
                   1, 0),  
                  nrow=2,ncol=2,byrow=TRUE)

#Combined Actions matrix
Actions=list(maintenance=t_maintenance, no_maintenance=t_no_maintenance, repair=t_repair, replace=t_replace)

#2. Defining the rewards and penalties

#maintenance Action
r_maintenance=matrix(c(70, -30,
                       -9999, -9999),
                nrow=2,ncol=2,byrow=TRUE)

#no_maintenance Action
r_no_maintenance=matrix(c(100, 0,
                          -9999, -9999),
              nrow=2,ncol=2,byrow=TRUE)

#recharge Action
r_repair=matrix(c(-9999, -9999,
                  40, -60),  
                  nrow=2,ncol=2,byrow=TRUE)

#replace Action
r_replace=matrix(c(-9999, -9999,
                   -10, -110),  
                nrow=2,ncol=2,byrow=TRUE)

Rewards = list(r_maintenance, r_no_maintenance, r_repair, r_replace)

#3. Solving the navigation
solver=mdp_finite_horizon(P=Actions, R=Rewards, discount=1, N=10)
solver2=mdp_finite_horizon(P=Actions, R=Rewards, discount=1, N=20)

#4. Getting the policy
print(solver$policy)
print(names(Actions)[solver$policy]) 

print(solver2$policy)
print(names(Actions)[solver2$policy])

#5. Getting the Values at each step
print(solver$V) 

print(solver2$V) 


##########Question 2######

M = 100 # Upper threshold
 # Number of value iterations
p = 0.6 # Probability of success 

# 1. Defining Transition Matrices for Actions

TransM = array(0, c(M*2-1, M*2-1, M-1))
#2*M-1

# Actions "Bet $a"
for (a in 1:(M-1)) {
  for (s in a:(M-1)) {
    TransM[s+1,s+1+a,a] = p
    TransM[s+1,s+1-a,a] = 1-p
  }
  TransM[1,1,a] = 1       # State $0 is absorbing 
}

for (a in 1:(M-1)) {
  for (s in M:(2*M-2)) {
    TransM[s+1,s+1,a] = 1 # States after 100 are absorbing
  }
}

#2. Defining the rewards
Rewards = array(0, c(2*M-1,M-1))
for (s in (M/2):(M-1)) {
  for (a in (M-s):(s)) {
    Rewards[s+1,a] = (s+a)*p
  }
}


#delta = 0.99 vs 0.9999
solver = mdp_policy_iteration(P=TransM, R=Rewards, discount=0.99)
solver2 = mdp_policy_iteration(P=TransM, R=Rewards, discount=0.9999)

#Getting the optimal solution
#for delta =0.99
cat("Optimal Actions:\n")
print(solver$policy)  
cat("\nOptimal Values:\n")
print(solver$V)

plot(0:(2*M-2), solver$policy, pch='+')

plot(0:(2*M-2), solver$V, pch='+')
#graphics.off()

#for delta =0.999
cat("Optimal Actions:\n")
print(solver2$policy)  
cat("\nOptimal Values:\n")
print(solver2$V)

plot(0:(2*M-2), solver2$policy, pch='+')

plot(0:(2*M-2), solver2$V, pch='+')


