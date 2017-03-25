# Challenge

You're given a dataset of about 9000 receipts and invoices. Your goal is to extract the supplier
that's on the receipt. A supplier is the company that issued the receipt. E.g. Starbucks, Tesco,
etc. You don't need to be perfect, just not embarasingly wrong. For example - having a receipt from
"Startbucks London Limited." and extracing "Starbucks Ltd." is fine. Returning a supplier name
"Coffee: 11.55" - not OK.

You're given a dataset of receipts, described in a table below. Each receipt has an "image" - a PDF
or image file that's the actuall digital copy of the reciept. We've also done the hard work and
extracted the text out of those images. Finally, there's a large (4M+) supplier database that you
can use as a canonical reference. Receipts and the suppliers originate in the UK. See below for more
details about each artefact.

## Dataset

It's located in the file `receipts.csv`. It contains the following columns:

| Fields                     | Description |
|----------------------------|-------------|
| `id`                       | The ID of the receipt |
| `created_at`               | The date the receipt was uploaded in our DB |
| `currency_code`            | The currency. Ex: GBP, BGN, AUD |
| `total_amount`             | The total on the reciept (in the currency above) |
| `vat_amount`               | The VAT on the receipt (in the currency above)  |
| `date`                     | The date on the receipt (not necessarily the same as created_at) |
| `due_date`                 | In case the receipt is an invoice - by which date a payment is expected |
| `invoice_number`           | In case the receipt is an invoice - the invoice number on it |
| `received_via`             | How we got the receipt (E.g. via email, via web, etc.) |
| `supplier_name`            | The name of the supplier (free form text) |
| `text`                     | The text on the receipts. Obtained via OCR (tesseract and then Google Cloud Vision) |
| `ocr_method`               | The type of OCR used |
| `digital_item`             | If the receipt is a digital item (email, pdf) |
| `manual_review`            | Has the document been manually reviewed |
| `account_default_currency` | The default currency of the account |
| `payment_type`             | The type of payment used (E.g. credit card, cheque, cash, etc.) |
| `document_type`            | The type of document (E.g. receipt, invoice, ATM, etc.) |

## Images

Those are the digital copies of the receipts and invoices. Mostly JPG and PDF files. Located in the
`images/` directory. They are named according to the `id` column in the dataset.

Datathon case team remark: in file Extract.zip you will find a small sample of images for prototyping and initial idea generation.

## Texts

In the `texts/` directory you'll find the text on the receipts. Again, named using the `id`. There
are two types of files in there. One type is XML - those are extracted from PDFs. It does
contain not only the text, but the coordinates as well. The other version is JSON - this is
extracted from the images using OCR. It, too, contains coordinates. Note that for some files (namely
PDFs) you might get both versions - the reason being that some PDF files actually contain just a
scanned copy of the receipt and no (meaningful) text.

## Suppliers

A canonical list of about 4M mostly UK based suppliers is provided. It's best if your suggestion is
one of them in case the supplier is present in the list. If not - it's up to you what should be
returned.

| Fields | Description |
|--------|-------------|
| `id`     | A basic supplier ID |
| `name`   | The name of the supplier - this is the expected result |
| `country_code` | A 2 letter country code. Mostly GB where present |
| `created_at` | The date this supplier was added to the database |
| `company_number` | A unique (per country) company number - much like BULSTAT |
| `company_status` | Either an active company or one that's about to be striked off - i.e. not much recent activity |
| `country_of_origin` | Self explanatory. Not present for all records |
| `incorporation_date` | The date the company was created. Not present for all |
| `company_type` | Type of company - i.e. Private Limited Company. Not present for all |
| `address` | Address, where the company is operating from. In JSON format. Optional |
| `used_count` | How many times we've found a reciept for that company. Mosly missing right now |

# About Receipt Bank

Receipt Bank is a comapny with a mission to automate bookkeeping. If you have a business and have
spent any time entering, categorizing and storing reciepts - you'll know that it's anoying and a bad
way to spend time. The main customers of Receipt Bank are two groups - accountants, who deal with
small and medium sized businesses (1-250 people) and sole traders - a plummer working for
herself.

The Machine learning team @ Receipt Bank right now is about 6 people and we're currently focused on
solving the "Data extraction" problem. I.e. having a digital copy of a receipt - what's the Total on
that receipt. What's the VAT, the date is was issued on. Who's the company that issued it. So far
we've been attacking this problem by creating a classifier for each field (one for Total, one for
VAT, etc.). We're now starting to experiment with Neural Networks, but we're very early on that
front.
