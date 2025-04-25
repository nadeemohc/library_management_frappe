# Copyright (c) 2025, Muhammed Nadeem and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta


def execute(filters: dict | None = None):
	"""Return columns and data for the report."""
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report."""
	return [
		{
			"label": _("Member"),
			"fieldname": "full_name",
			"fieldtype": "Link",
			"options": "Library Member",
		},
		{
			"label": _("From Date"),
			"fieldname": "from_date",
			"fieldtype": "Date",
		},
		{
			"label": _("To Date"),
			"fieldname": "to_date",
			"fieldtype": "Date",
		},
		{
			"label": _("Days Left"),
			"fieldname": "days_left",
			"fieldtype": "Data",
		},
	]


from datetime import datetime, timedelta
import frappe

def get_data(filters=None):
	days = int(filters.get("days") or 30)
	expiry_date = (datetime.today() + timedelta(days=days)).date()

	query = """
		SELECT
			mship.library_member as member,
			mem.full_name,
			mship.from_date,
			mship.to_date,
			DATEDIFF(mship.to_date, CURDATE()) AS days_left
		FROM
			`tabLibrary Membership` mship
		LEFT JOIN
			`tabLibrary Member` mem ON mship.library_member = mem.name
		WHERE
			mship.to_date <= %s
			AND mship.docstatus = 1
		ORDER BY
			mship.to_date ASC
	"""

	return frappe.db.sql(query, (expiry_date,), as_dict=True)
