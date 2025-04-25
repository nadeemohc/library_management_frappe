// Copyright (c) 2025, Muhammed Nadeem and contributors
// For license information, please see license.txt

frappe.query_reports["Currently Issued Books"] = {
	filters: [
		{
			"fieldname": "article",
			"label": __("Article"),
			"fieldtype": "Link",
			"options":"Article",
			"reqd": 0,
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			// "options": "",
			// "reqd": 0,
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			// "options": "",
			// "reqd": 0,
		},
		// {
		// 	"fieldname": "status",
		// 	"label": __("Status"),
		// 	"fieldtype": "Type",
		// 	"options": "Issued\nAvailable",
		// 	"reqd": 0,
		// },
	],
};
