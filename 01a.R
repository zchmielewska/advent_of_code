data <- readLines("./input/01/example")
data <- readLines("./input/01/data")

current_cals = 0
max_cals = 0

for (i in 1:length(data)) {
  value <- data[i]

  if (value == "") {
    if (current_cals > max_cals) {
      max_cals <- current_cals
    }
    current_cals <- 0
  } else {
    current_cals <- current_cals + as.integer(value)
  }

  print(current_cals)
}
