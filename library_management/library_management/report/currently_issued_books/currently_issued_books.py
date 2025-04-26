import frappe
from frappe import _
from frappe.query_builder import DocType
from frappe.utils import getdate


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



def get_data(filters=None):
    LibraryTransaction = DocType("Library Transaction")
    Article = DocType("Article")
    LibraryMember = DocType("Library Member")

    from_date = getdate(filters.get("from_date")) if filters.get("from_date") else None
    to_date = getdate(filters.get("to_date")) if filters.get("to_date") else None

    q = (
        frappe.qb.from_(LibraryTransaction)
        .join(Article).on(Article.name == LibraryTransaction.article)
        .join(LibraryMember).on(LibraryMember.name == LibraryTransaction.library_member)
        .select(
            Article.article_name.as_("article_name"),
            Article.image.as_("image"),
            LibraryMember.full_name.as_("full_name"),
            LibraryTransaction.date
        )
        .where(LibraryTransaction.type == "issued")
        .where(LibraryTransaction.docstatus == 1)
    )

    if filters.get("article"):
        q = q.where(LibraryTransaction.article == filters["article"])
    if filters.get("name"):
        q = q.where(LibraryTransaction.library_member == filters["name"])
    if from_date:
        q = q.where(LibraryTransaction.date >= from_date)
    if to_date:
        q = q.where(LibraryTransaction.date <= to_date)

    return q.run(as_dict=True)
