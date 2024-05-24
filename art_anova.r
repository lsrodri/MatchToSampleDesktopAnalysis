# Load necessary libraries
if (!require("ARTool")) {
  install.packages("ARTool")
}
library(ARTool)

if (!require("ggplot2")) {
  install.packages("ggplot2")
}
library(ggplot2)

# Load your data
data <- read.csv("data.csv") # Use the file name directly

# Convert Correctness to numeric (1 for True, 0 for False)
data$Correctness <- as.numeric(data$Correctness == "True")

# Ensure ReactionTime is numeric
data$ReactionTime <- as.numeric(data$ReactionTime)

# Convert Immersion and Modality to factors
data$Immersion <- as.factor(data$Immersion)
data$Modality <- as.factor(data$Modality)

# Remove rows with missing values
data <- na.omit(data)

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

# Aggregate data for plotting
agg_data <- aggregate(cbind(avg_correctness = Correctness, avg_reaction_time = ReactionTime) ~ Immersion + Modality, data, mean)
agg_data$se_correctness <- aggregate(Correctness ~ Immersion + Modality, data, function(x) sd(x) / sqrt(length(x)))$Correctness
agg_data$se_reaction_time <- aggregate(ReactionTime ~ Immersion + Modality, data, function(x) sd(x) / sqrt(length(x)))$ReactionTime

# Calculate error rate and standard error for error rate
agg_data$error_rate <- 1 - agg_data$avg_correctness
agg_data$se_error_rate <- agg_data$se_correctness

# Interaction plot for reaction time
interaction.plot(data$Modality, data$Immersion, data$ReactionTime,
                 xlab = "Modality", ylab = "Mean Reaction Time", trace.label = "Immersion",
                 col = c("red", "blue"), lty = 1:2, pch = c(1, 2))

# Bar plot with error bars for reaction time
p1 <- ggplot(agg_data, aes(x = Modality, y = avg_reaction_time, fill = Immersion)) +
  geom_bar(stat = "identity", position = "dodge") +
  geom_errorbar(aes(ymin = avg_reaction_time - se_reaction_time, ymax = avg_reaction_time + se_reaction_time),
                position = position_dodge(0.9), width = 0.25) +
  labs(title = "Reaction Time by Modality and Immersion", y = "Mean Reaction Time", x = "Modality") +
  theme_minimal()

# Bar plot with error bars for error rate
p2 <- ggplot(agg_data, aes(x = Modality, y = error_rate, fill = Immersion)) +
  geom_bar(stat = "identity", position = "dodge") +
  geom_errorbar(aes(ymin = error_rate - se_error_rate, ymax = error_rate + se_error_rate),
                position = position_dodge(0.9), width = 0.25) +
  labs(title = "Error Rate by Modality and Immersion", y = "Mean Error Rate", x = "Modality") +
  theme_minimal()

# Print the plots to ensure they display
print(p1)
print(p2)
