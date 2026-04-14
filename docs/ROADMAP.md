# Fixes 
1. fix issues with tables in lists pages of custom admin pages where datatables seems to be broken 
2. fix layout and other ui bugs issues in notifications list page
3. fix the `ResourceTypeSitemap` class in `website/sitamamp.py` to ensure no n+1 queries while maintaining the initial desired output
4. 
# Features to add
1.  Run through all routes in all urls and their respective views and ensure queries are 100% efficient and fast eliminating any n+1 issue and \
and adding efficient caching strategies that are easy to work with or modify in future and updating documentation
2. Adding comprehensive test cases for all apps covering all existing or potential issues and edge cases