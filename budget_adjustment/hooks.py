from . import __version__ as app_version

app_name = "budget_adjustment"
app_title = "Budget Adjustment"
app_publisher = "Chris"
app_description = "An ERPNext Application to reallocate budget from one or more accounts to other accounts. A budget adjustment voucher is submitted and it changes the original budget will be reflected."
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "christophernjogu@gmail.com"
app_license = "MIT"

# fixtures

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [["name", "in", (
            "Account-n1",
            "Account-n2",
            "Account-n3",
            "Account-account_numbers_",
            "Account-column_break_23",
            "Account-column_break_25",
            "Budget Account-number_of_changes",
            "Budget Account-used_amount",
            "Budget Account-free_balance"

        )]]
    },
    {
        "doctype": "Property Setter",
        "filters": [["name", "in", (
            "Account-n1",
            "Account-n2",
            "Account-n3",
            "Account-account_numbers_",
            "Account-column_break_23",
            "Account-column_break_25"
        )]]
    },
    {
        "doctype": "Workspace",
        "filters": [["name", "in", (
            "Budget Adjustment"
        )]]
    },
    {
        "doctype": "Report",
        "filters": [["name", "in", (
            "Budget Report Accounts",
            "Budget Report"
        )]]
    },
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/budget_adjustment/css/budget_adjustment.css"
# app_include_js = "/assets/budget_adjustment/js/budget_adjustment.js"

# include js, css files in header of web template
# web_include_css = "/assets/budget_adjustment/css/budget_adjustment.css"
# web_include_js = "/assets/budget_adjustment/js/budget_adjustment.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "budget_adjustment/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Budget": "public/js/doctype/budget.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "budget_adjustment.install.before_install"
# after_install = "budget_adjustment.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "budget_adjustment.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Budget": "budget_adjustment.overrides.budget.CustomBudget"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
    "Account": {
        "on_update": "budget_adjustment.budget_adjustment.doctype.account.events.on_update",
        "before_submit": "budget_adjustment.budget_adjustment.doctype.account.events.before_submit",
        "validate": "budget_adjustment.budget_adjustment.doctype.account.events.validate"
    },
    "Budget": {
        "on_change": "budget_adjustment.budget_adjustment.doctype.budget.events.on_change",
        "on_load": "budget_adjustment.budget_adjustment.doctype.budget.events.on_load"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"budget_adjustment.tasks.all"
# 	],
# 	"daily": [
# 		"budget_adjustment.tasks.daily"
# 	],
# 	"hourly": [
# 		"budget_adjustment.tasks.hourly"
# 	],
# 	"weekly": [
# 		"budget_adjustment.tasks.weekly"
# 	]
# 	"monthly": [
# 		"budget_adjustment.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "budget_adjustment.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "budget_adjustment.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "budget_adjustment.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"budget_adjustment.auth.validate"
# ]
