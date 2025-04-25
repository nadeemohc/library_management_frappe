# Copyright (c) 2025, Muhammed Nadeem and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Article"),
			"fieldname": "article",
			"fieldtype": "Data",
		},
		{
			"label": _("image"),
			"fieldname": "image",
			"fieldtype": "Image",
		},
		{
			"label": _("Number of issues"),
			"fieldname": "no_of_issues",
			"fieldtype": "Int",
		},
	]


def get_data() -> list[dict]:
	"""Return data for the report."""
	return frappe.db.sql("""
		SELECT
			t.article,
			a.image,
			COUNT(*) AS no_of_issues
		FROM
			`tabLibrary Transaction` t
		LEFT JOIN
			`tabArticle` a ON t.article = a.name
		WHERE
			t.type = 'Issued' AND t.docstatus = 1
		GROUP BY
			t.article, a.image
		ORDER BY
			no_of_issues DESC
	""", as_dict=True)
