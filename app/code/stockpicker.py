from selenium.webdriver import Firefox, PhantomJS


driver = PhantomJS()

url = ('https://www.google.com/finance?start=0&num=5000&q=%5B(exchange%20%3D'
       '%3D%20"{}")%20%26%20(last_price%20>%200.1)%20%26%20(last_price%20<'
       '%201500)%5D&restype=company&noIL=1')

driver.get(url.format('NYSE'))
nyse = (elem.text for elem in driver.find_elements_by_class_name('symbol'))

driver.get(url.format('NASDAQ'))
nasdaq = (elem.text for elem in driver.find_elements_by_class_name('symbol'))
print '\n'.join(list(nasdaq))