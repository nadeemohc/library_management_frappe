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
			"fieldname": "article_name",
			"fieldtype": "Data",
		},
		{
			"label": _("Article Image"),
			"fieldname": "image",
			"fieldtype": "Image",
		},
		{
			"label": _("Issued To"),
			"fieldname": "full_name",
			"fieldtype": "Data",
		},
		{
			"label": _("Issue Date"),
			"fieldname": "date",
			"fieldtype": "Date",
		}
	]


def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	data = []
	transctions = frappe.get_all(
		"Library Transaction",
		# filters={"type":"available", "docstatus":1},
		fields=["article", "library_member", "date"])
	print(transctions)
	for i in transctions:
		article = frappe.get_doc("Article", i.article)
		member = frappe.get_value("Library Member", i.library_member, "full_name")
		

		data.append({
			"article_name":article.article_name, 
			"image":article.image, 
			"full_name":member, 
			"date": i.date})

	return data