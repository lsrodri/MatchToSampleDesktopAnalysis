# Load necessary libraries
if (!require("ARTool")) {
  install.packages("ARTool")
}
library(ARTool)

# Load your data
data <- read.csv("data.csv") # Use the file name directly

# Convert Correctness to numeric (1 for True, 0 for False)
data$Correctness <- as.numeric(data$Correctness == "True")

# Ensure ReactionTime is numeric
data$ReactionTime <- as.numeric(data$ReactionTime)

# Convert Immersion and Modality to factors
data$Immersion <- as.factor(data$Immersion)
data$Modality <- as.factor(data$Modality)

# Aggregate average correctness and mean reaction time per participant, immersion, and condition
aggregated_data <- aggregate(cbind(avg_correctness = Correctness, avg_reaction_time = ReactionTime) ~ ParticipantID + Immersion + Modality, data, mean)

# Calculate error rate
aggregated_data$error_rate <- 1 - aggregated_data$avg_correctness

# Perform ART ANOVA for error rate
anova_error_rate <- art(error_rate ~ Immersion * Modality, data = aggregated_data)
anova_results_error_rate <- anova(anova_error_rate)

# Perform ART ANOVA for reaction time
anova_reaction_time <- art(avg_reaction_time ~ Immersion * Modality, data = aggregated_data)
anova_results_reaction_time <- anova(anova_reaction_time)

print(anova_results_error_rate)
print(anova_results_reaction_time)

# Write the results to CSV files
write.csv(anova_results_error_rate, "anova_results_error_rate.csv")
write.csv(anova_results_reaction_time, "anova_results_reaction_time.csv")

# Print a message indicating the results have been saved
cat("ANOVA results have been saved to 'anova_results_error_rate.csv' and 'anova_results_reaction_time.csv'.\n")
