import re
from pdfplumber import open as pdf_open

class PlankopfExtractor:
    def __init__(self):
        self.required_fields = {
            'Planschlüssel': None,
            'Stat.Pos': None,
            'Auftr. Nr.': None,
            'Index': None,
            'Fertigteil Position': None,
            'Stück': None,
            'Volumen (m3)': None,
            'Gewicht (to.)': None
        }

    def extract_from_pdf(self, pdf_path):
        """Extract plankopf data from PDF file"""
        try:
            with pdf_open(pdf_path) as pdf:
                last_page = pdf.pages[-1]
                text = last_page.extract_text()
                return self.parse_plankopf_text(text)
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None

    def parse_plankopf_text(self, text):
        """Parse text to extract required fields using patterns from actual PDF"""
        extracted_data = self.required_fields.copy()
        
        # Find the main measurements line
        measurements_pattern = r'(\d+-\d+)\s+(\d+)\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)'
        measurements_match = re.search(measurements_pattern, text)
        
        if measurements_match:
            extracted_data['Fertigteil Position'] = measurements_match.group(1)
            extracted_data['Stück'] = int(measurements_match.group(2))
            extracted_data['Volumen (m3)'] = float(measurements_match.group(6))
            extracted_data['Gewicht (to.)'] = float(measurements_match.group(7))

        # Extract Planschlüssel
        planschlussel_match = re.search(r'Plan\.Nr/Index/Status\s*(FT_XX_\d+-\d+_[a-z]_F)', text)
        if planschlussel_match:
            extracted_data['Planschlüssel'] = planschlussel_match.group(1)

        # Extract Index from the change history
        index_match = (extracted_data['Planschlüssel']).split('_')[-2]
        if index_match:
            extracted_data['Index'] = index_match

        # Updated Auftr.Nr pattern to match the actual format in the PDF
        auftr_nr_match = re.search(r'(?:Auftr\.Nr|mitBüro)\s*(\d{3}-\d{2})', text)
        if auftr_nr_match:
            extracted_data['Auftr. Nr.'] = auftr_nr_match.group(1)

        # Extract Stat.Pos
        stat_pos_match = re.search(r'stat\.Pos\s+([^\n]+)', text)
        if stat_pos_match:
            value = stat_pos_match.group(1).strip()
            extracted_data['Stat.Pos'] = value if value != '-' else None

        return extracted_data

    def format_output(self, data):
        """Format the extracted data as a table"""
        if not data:
            return "No data extracted"
            
        max_key_length = max(len(key) for key in data.keys())
        formatted_output = []
        
        for key, value in data.items():
            if value is None:
                value = '-'
            formatted_output.append(f"{key:<{max_key_length}} | {value}")
            
        return "\n".join(formatted_output)

def process_pdf(pdf_path):
    """Process a single PDF file"""
    extractor = PlankopfExtractor()
    data = extractor.extract_from_pdf(pdf_path)
    return extractor.format_output(data)

if __name__ == "__main__":
    pdf_path = "data\FT_XX_07-101_b_F.pdf"  # Update this path to your PDF
    result = process_pdf(pdf_path)
    print(result)