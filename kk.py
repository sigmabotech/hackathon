import fitz

pdffile = r"data\03_Riegel\FT_XX_03-001_d_F.pdf"
doc = fitz.open(pdffile)
page = doc.load_page(0)  # number of page
pix = page.get_pixmap()
output = "outfile.png"
pix.save(output)
doc.close()