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
			"label": _("Member"),
			"fieldname": "full_name",
			"fieldtype": "Data",
		},
		{
			"label": _("From date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
		},
		{
			"label": _("To date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
		},
		{
			"label": _("Email"),
			"fieldname": "email_address",
			"fieldtype": "Data",
		},
		{
			"label": _("Phone"),
			"fieldname": "phone",
			"fieldtype": "Phone",
		},
	]


def get_data() -> list[dict]:
	"""Return data for the report using raw SQL join between Library Member and Library Membership."""

	query = """
		SELECT
			lm.full_name,
			mship.from_date,
			mship.to_date,
			lm.email_address,
			lm.phone
		FROM
			`tabLibrary Member` lm
		INNER JOIN
			`tabLibrary Membership` mship ON lm.name = mship.library_member
	"""
	
	return frappe.db.sql(query, as_dict=True)
