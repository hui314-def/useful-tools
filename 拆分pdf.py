import PyPDF2

def split_pdf(input_pdf, ranges, output_prefix):
    with open(input_pdf, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        for idx, page_range in enumerate(ranges):
            start, end = map(int, page_range.split('-'))
            writer = PyPDF2.PdfWriter()
            for page_num in range(start-1, end):
                writer.add_page(reader.pages[page_num])
            output_path = f"{output_prefix}_part{idx+1}.pdf"
            with open(output_path, 'wb') as outfile:
                writer.write(outfile)
            print(f"Saved: {output_path}")

if __name__ == "__main__":
    input_pdf = input("请输入PDF文件路径: ").strip()
    ranges_str = input("请输入拆分页数范围（如1-3,4-6）: ").strip()
    output_prefix = input("请输入输出文件前缀: ").strip()
    ranges = [r for r in ranges_str.split(',') if '-' in r]
    split_pdf(input_pdf, ranges, output_prefix)