import frappe
from frappe import _


def execute(filters: dict | None = None):
    """Return columns and data for the report.

    This is the main entry point for the report. It accepts the filters as a
    dictionary and should return columns and data. It is called by the framework
    every time the report is refreshed or a filter is updated.
    """
    columns = get_columns()
    data = get_data(filters)  # Pass filters to get_data function

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


from frappe.utils import getdate

def get_data(filters=None) -> list[dict]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a dict of field values.
	"""
	data = []

	query_filters = {
		"type": "issued",
		"docstatus": 1
	}

	if filters:
		if filters.get("article"):
			query_filters["article"] = filters["article"]
		if filters.get("name"):
			query_filters["library_member"] = filters["name"]

	# Fetch raw values from filters
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	# Convert them to datetime.date if provided
	if from_date:
		from_date = getdate(from_date)
	if to_date:
		to_date = getdate(to_date)

	transactions = frappe.get_all(
		"Library Transaction",
		fields=["article", "library_member", "date"],
		filters=query_filters
	)

	for txn in transactions:
		# Date filtering
		if from_date and txn.date < from_date:
			continue
		if to_date and txn.date > to_date:
			continue

		article = frappe.get_doc("Article", txn.article)
		member = frappe.get_value("Library Member", txn.library_member, "full_name")

		data.append({
			"article_name": article.article_name,
			"image": article.image,
			"full_name": member,
			"date": txn.date
		})

	return data
