lines <- readLines("./input/11/example.txt", warn = FALSE)
lines <- readLines("./input/11/data.txt", warn = FALSE)
n <- (length(lines) + 1) / 7


show_items <- function(monkeys) {
  i <- 1
  for (monkey in monkeys) {
    print(paste0("Monkey ", i, ": ", paste(monkey$items, collapse = ", ")))
    i <- i+1
  }
}

# Monkeys at the start
monkeys <- vector("list", n)
current_monkey <- 1
for (line in lines) {
  monkeys[[current_monkey]]$inspections <- 0
  
  # New monkey
  if (line == "") {
    current_monkey <- current_monkey + 1
    monkeys[[current_monkey]] <- list()
  }
  
  # Starting items
  if (grepl("Starting items", line)) {
    items <- as.integer(unlist(strsplit(unlist(strsplit(line, ":"))[2], ",")))
    monkeys[[current_monkey]]$items <- items
  }
  
  
  # Operation
  if (grepl("Operation", line)) {
    body <- unlist(strsplit(unlist(strsplit(line, "-")), "= "))[[2]]
    args <- "old"
    operation <- eval(parse(text = paste0('f <- function(', args, ') { return(' , body , ')}')))
    monkeys[[current_monkey]]$operation <- operation
  }
  
  # Test
  if (grepl("Test", line)) {
    by <- as.integer(unlist(strsplit(line, " by "))[[2]])
    test <- eval(parse(text = paste0('f <- function(x) { return(x %% ', by ,' == 0 )}')))
    monkeys[[current_monkey]]$test <- test
    monkeys[[current_monkey]]$by <- by
  }
  
  # Throw
  if (grepl("If true:", line)) {
    to <- as.integer(unlist(strsplit(line, " monkey "))[[2]])
    monkeys[[current_monkey]]$true_to <- to + 1
  }
  if (grepl("If false:", line)) {
    to <- as.integer(unlist(strsplit(line, " monkey "))[[2]])
    monkeys[[current_monkey]]$false_to <- to + 1
  }
}


show_items(monkeys)

modulo <- 1
for (monkey in monkeys) {
  modulo <- modulo * monkey$by
  
}

# Play
round <- 1
while(round <= 10000) {
  for (i in 1:length(monkeys)) {
    monkey <- monkeys[[i]]
    for (item in monkey$items) {
      monkeys[[i]]$inspections <- monkeys[[i]]$inspections + 1
      worry_level <- monkey$operation(item) %% modulo
      test <- monkey$test(worry_level)
      
      # Throw item
      if (test) {
        monkeys[[monkey$true_to]]$items <- c(monkeys[[monkey$true_to]]$items, worry_level)
      } else {
        monkeys[[monkey$false_to]]$items <- c(monkeys[[monkey$false_to]]$items, worry_level)
      }
      monkeys[[i]]$items <- monkeys[[i]]$items[-1]
    }
    
  }
  round <- round + 1
}




inspections <- c()
for (monkey in monkeys) {
  inspections <- c(inspections, monkey$inspections)
}
ordered <- inspections[order(inspections, decreasing = TRUE)]
monkey_business <- ordered[1] * ordered[2]
print(monkey_business)


