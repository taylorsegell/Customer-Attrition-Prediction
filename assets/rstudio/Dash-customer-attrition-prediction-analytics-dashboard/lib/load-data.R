# Sample Materials, provided under license.
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2019, 2020. All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

# Load Data from CSV files

library(readr)
library(scales)

readDataset <- function(fileName) {read.csv(file.path(fileName))}

customer <- readDataset("customer.csv")
customer_summary <- readDataset("customer_summary.csv")
customer_history <- readDataset("customer_history.csv")
account <- readDataset("account.csv")
account_summary <- readDataset("account_summary.csv")

clients <- list(
  list(name="Leo Rakes", image="6M.jpg", risk="Medium"),
  list(name="Catalina Santos", image="9F.jpg", risk="Medium"),
  list(name="Thomas Owens", image="23M.jpg", risk="Low"),
  list(name="Liliana Hunnisett", image="10F.jpg", risk="Low"),
  list(name="Jeffery Smith", image="5M.jpg", risk="Low"),
  list(name="Jesica Abrams", image="22F.jpg", risk="Low"),
  list(name="Carla Warnes", image="25F.jpg", risk="Medium")
)
clientIds <- c(1103, 1195, 1116, 1115, 1114, 1021, 1049)
names(clients) <- clientIds

for(id in clientIds) {
  clients[[toString(id)]]$income <- dollar(customer[customer$CUSTOMER_ID == id,][[1,'ANNUAL_INCOME']])
}

colsToDrop <- c(
  "CUSTOMER_SUMMARY_FUNDS_UNDER_MANAGEMENT_mean",
  "CUSTOMER_SUMMARY_FUNDS_UNDER_MANAGEMENT_min",
  "CUSTOMER_SUMMARY_FUNDS_UNDER_MANAGEMENT_max",
  "CUSTOMER_SUMMARY_TOTAL_AMOUNT_OF_DEPOSITS_min",
  "CUSTOMER_SUMMARY_TOTAL_AMOUNT_OF_DEPOSITS_max",
  "CUSTOMER_SUMMARY_TOTAL_AMOUNT_OF_DEPOSITS_sum",
  "CUSTOMER_ANNUAL_INCOME",
  "CUSTOMER_NUMBER_OF_DEPENDENT_CHILDREN",
  "CUSTOMER_TENURE",
  "NUM_ACCOUNTS_WITH_RISK_TOLERANCE_MODERATE",
  "NUM_ACCOUNTS_WITH_RISK_TOLERANCE_HIGH",
  "NUM_ACCOUNTS_WITH_RISK_TOLERANCE_VERY_LOW",
  "NUM_ACCOUNTS_WITH_RISK_TOLERANCE_LOW",
  "CUSTOMER_SUMMARY_TOTAL_AMOUNT_OF_DEPOSITS_current_vs_6_months_ago",
  "CUSTOMER_SUMMARY_TOTAL_AMOUNT_OF_DEPOSITS_max_min_ratio"
)