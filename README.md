# css-js-cleaner
Css and JS cleaner (Remove Unused Code)

You can run this code by using python3
The PIP dependencies all come as standard so no need to install any libraries.

## How to use
Run the google coverage report on as many pages of "THE SAME" site that you wish.
https://developers.google.com/web/tools/chrome-devtools/coverage

Download the report for each page

Open the main.py and modify the following lines:
```
initial_file = "coverage-bing.json"
compare_files = ["coverage-search.json"]
domain_name = "https://www.bing.com"
```
`initial_file` can be any file of you choosing, I would recommend the largest file.
`compare_files` is all the other files that are not your initial file. If you only have the initial_file then set this value to `[]`.
`domain_name` is the domain name for the site you are optimising without any trailing forward slashes.

domain_name is used so you don't clean any files you don't have control over.

Now you have done.

Run `python3 main.py` or `python main.py` to run the code and you will see the cleaned files generated afterwards.