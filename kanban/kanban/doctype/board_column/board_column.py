# -*- coding: utf-8 -*-
# Copyright (c) 2015, Alec Ruiz-Ramon and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BoardColumn(Document):
	def get_docs_in_column(self):
		filters = {
	    	self.field_name: self.field_option
        }
		docs = frappe.client.get_list(self.dt, filters=filters,
									  limit_page_length=None)
		full_list = []
		for doc in docs:
			full_list.append(frappe.client.get(self.dt, doc['name']))

		return self.prepare_docs_for_board(full_list)

	def prepare_docs_for_board(self, doc_list):
		data = []
		display_fields = self.get_display_fields()
	    # need to take display_field: field_name pairs & replace field_name with
	    # the field's value in the document.
	    # then, create return packet of full doc, and displayed doc
		for doc in doc_list:
			card_fields = {}
			for k, v in display_fields.iteritems():
				card_fields[k] = doc[v]
			data.append({
				"doc": doc,
				"card_fields": card_fields
				})
		return data

	def get_display_fields(self):
	    """ Gets dict of display_field: doc_field pairs.
	    Gets Label:fieldname pairs from document spec'd in column,
	    and 'zips' with pairs of display_field:Label from board column"""

	    display_fields = [
	        "title_field", "first_subtitle", "second_subtitle",
	        "field_one", "field_two", "field_three"
	        ]
	    doc_fields = { field.label:field.fieldname for field in
	                   self.get_associated_doc_fields()}
	    col_dict = frappe.client.get(self)
	    board_fields = { k:v for k, v in col_dict.iteritems() if
	                     k in display_fields }
	    ret = {}
	    for k, v in board_fields.iteritems():
	        ret[k] = doc_fields[v]
	    return ret

	def get_associated_doc_fields(self):
	    meta = frappe.desk.form.meta.get_meta(self.dt)
	    return [field for field in meta.fields]
