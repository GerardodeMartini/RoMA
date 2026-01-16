from rembg import remove
from PIL import Image
import io

input_path = 'static/img/logo_raw.jpg'
output_path = 'static/img/logo_trans.png'

print(f"Processing {input_path}...")

try:
    with open(input_path, 'rb') as i:
        input_data = i.read()
        output_data = remove(input_data)
        
    with open(output_path, 'wb') as o:
        o.write(output_data)
        
    print(f"Successfully saved transparent logo to {output_path}")

except Exception as e:
    print(f"Error processing image: {e}")
