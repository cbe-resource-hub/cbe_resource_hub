# Fixes 
1. fixing the datatables bug on some list pages
2. ensure details text area field is responsive on smaller screens, ie its scrollable horizontally lke responsive HTML tables do. 
3. fix the error
    ```terminaloutput
   
   Error fetching command 'dbbackup': The settings DBBACKUP_STORAGE and DBBACKUP_STORAGE_OPTIONS have been deprecated in favor of using Django Storages configuration. Please refer to the documentation for more details.
   Command 'dbbackup' skipped
   Error fetching command 'dbrestore': The settings DBBACKUP_STORAGE and DBBACKUP_STORAGE_OPTIONS have been deprecated in favor of using Django Storages configuration. Please refer to the documentation for more details.
   Command 'dbrestore' skipped
   Error fetching command 'listbackups': The settings DBBACKUP_STORAGE and DBBACKUP_STORAGE_OPTIONS have been deprecated in favor of using Django Storages configuration. Please refer to the documentation for more details.
   Command 'listbackups' skipped
   Error fetching command 'mediabackup': The settings DBBACKUP_STORAGE and DBBACKUP_STORAGE_OPTIONS have been deprecated in favor of using Django Storages configuration. Please refer to the documentation for more details.
   Command 'mediabackup' skipped
   Error fetching command 'mediarestore': The settings DBBACKUP_STORAGE and DBBACKUP_STORAGE_OPTIONS have been deprecated in favor of using Django Storages configuration. Please refer to the documentation for more details.
   Command 'mediarestore' skipped

   ```
4. fix the filter logic on the resources list page where the htmx keeps pushing new filter query params to  existing ones/
instead of updating accordingly creating something like which is mysteriously processed fine based on updated params in the backend
```http request
http://localhost:8000/resources/?q=&level=&area=55&resource_type=&q=&level=&area=55&resource_type=exam&q=&level=&area=82&resource_type=exam
```
5.


# Features to add
1. adding sidebar to the custom admin dashboard on the right
2. adding custom admin logic for files management just like in WordPress
3. adding custom admin logic for seo management just like in slug redirects and seo model 
4. Initializing pytest correctly and adding comprehensive test cases 
5. adding custom admin pages and logics to manage CRUD for partners, also show the partners if they exist as barners if they have the (show_as_burner) flag turned on, on website showed professionally \
like ads in a minimalistic way that's non-intrusive and doesn't destroy ux, also there should be a public page lising them 
6. add validators file type based on file magic and signature not just file name for ResourceItem model and enhance existing validators 
7. A robust notification system preferably in its own app that exposes tasks (function) that can be called when events happen \
to que/send and email via **CELERY** to the admin, when important events happen like signup, contact form submission, resource item upload etc., notifications, \
notifications should be fault-tolerant with retry logic, but be safe such that they don't max out the SMTP limits
8. 