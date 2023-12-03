import duckdb

#loading data
users = duckdb.read_csv('G:\\My Drive\\NYP\\loyalty\\2023-11-10_Users_NYPNL.csv')
loyalty_accounts = duckdb.read_csv('G:\\My Drive\\NYP\\loyalty\\2023-11-10_LoyaltyAccounts_NYPNL.csv')
loyalty_accounts2 = duckdb.read_csv('G:\\My Drive\\NYP\\loyalty\\2023-11-11_LoyaltyAccounts_NYPNL.csv')
loyalty_accounts.duckdb_columns()
merged_user_accounts = \
duckdb.sql('\
select * \
from users as u \
inner join loyalty_accounts2 as la \
on la.CustomerId = u.id \
')

#saving each loyalty category
normal_members = duckdb.sql(
    """
    select
    mua.tier,
    mua.Username
    from merged_user_accounts as mua
    where
    mua.tier = 'Member'
    """
)
gold_members = \
duckdb.sql(
    """
    select
    mua.*
    from merged_user_accounts as mua
    where
    mua.tier = 'Gold Member'
    """
)

silver_members = \
duckdb.sql(
    """
    select
    mua.*
    from merged_user_accounts as mua
    where
    mua.tier = 'Silver Member'
    """
)

members_gold_gift = duckdb.sql(
    """
    select
    mua.*
    from merged_user_accounts as mua
    where
    mua.CurrentTierMinimumAmountOfMoneySpent = 300 
    """
)
members_silver_gift = duckdb.sql(
    """
    select
    mua.*
    from merged_user_accounts as mua
    where
    mua.CurrentTierMinimumAmountOfMoneySpent = 150
    """
)

members_gold_gift.shape
members_silver_gift.shape

#Exporting to csv
# Specify output paths
normal_members_output = 'G:\\My Drive\\NYP\\loyalty\\2023-11-11_normal_members.csv'
gold_members_output = 'G:\\My Drive\\NYP\\loyalty\\2023-11-11_gold_members.csv'
silver_members_output = 'G:\\My Drive\\NYP\\loyalty\\2023-11-11_silver_members.csv'
merged_members_output = 'G:\\My Drive\\NYP\\loyalty\\2023-11-11_all_members.csv'
members_gold_gift_output = 'G:\\My Drive\\NYP\\loyalty\\2023-11-11_members_gold_gift.csv'
members_silver_gift_output = 'G:\\My Drive\\NYP\\loyalty\\2023-11-11_members_silver_gift.csv'

# Exporting to CSV
normal_members.to_csv(normal_members_output)
gold_members.to_csv(gold_members_output)
silver_members.to_csv(silver_members_output)
merged_user_accounts.to_csv(merged_members_output)
members_gold_gift.to_csv(members_gold_gift_output)
members_silver_gift.to_csv(members_silver_gift_output)

merged_user_accounts.columns