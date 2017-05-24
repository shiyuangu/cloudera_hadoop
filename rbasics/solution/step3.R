# step 1
a <- c("a", "b", "c")

# step 2
b <- 1:3

# step 3
c <- list(a, b)

# step 4
names(c) <- c("letters", "numbers")

# step 5
sum(c$numbers)
