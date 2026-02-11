from app.services.pdf_converter import clean_cell_content

# 测试音标清理
test_input = 'eco-friendly [ˌiː.kəʊˈfrendli]'
result = clean_cell_content(test_input)
print(f"输入: {test_input}")
print(f"输出: {result}")

# 测试普通文本
test_input2 = '普通的中文内容'
result2 = clean_cell_content(test_input2)
print(f"输入: {test_input2}")
print(f"输出: {result2}")