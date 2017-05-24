# Very simple R exercise: We use the built-in binom.test
# to determine whether the difference in the user acceptance
# rates for the artist recommendations from algorithms A and B
# is statistically significant.

# Invocation: R --no-save < hypothesis_test.R

a = 254
b = 189
total = a + b

binom.test(a, total)
binom.test(b, total)
