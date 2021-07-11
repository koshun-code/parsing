import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time
import json


def get_data():

	cur_date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
			  

	with open(f"labirint_{cur_date}.csv", "w") as file:
		writer = csv.writer(file)

		writer.writerow(
			(
				"Название книги",
				"Автор",
				"Издательство",
				"Цена со скидкой",
				"Цена без скиндки",
				"Процент скидки",
				"Наличие на складе"
				)
			)

	headers = {
		"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	    "User-agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
	}
	url = 'https://www.labirint.ru/genres/2304/?display=table&page=1'
	response = requests.get(url=url, headers=headers)
	soup = BeautifulSoup(response.text, "lxml")

	pages_count = int(soup.find("div", class_= "pagination-numbers").find_all("a")[-1].text)
	
	books_data = []

	for page in range(1, pages_count + 1):
		url = f"https://www.labirint.ru/genres/2304/?display=table&page={page}"

		response = requests.get(url=url, headers=headers)
		soup = BeautifulSoup(response.text, "lxml")

		books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

		for bi in books_items:
			book_data = bi.find_all("td")

			try:
				book_title = book_data[0].find("a").text.strip()
			except:
				book_title = "There is not finding book"
			try:
				book_author = book_data[1].text.strip()
			except:
				book_author = "Not an Author"
			try:
				#book_publish = book_data[2].text
				book_publish = book_data[2].find_all("a")
				book_publish = ":".join([bp.text for bp in book_publish])
			except:
				book_publish = "Not a publisher"
			try:
				book_new_price = int(book_data[3]. find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))
			except:
				book_new_price = "Not a price"
			try:
				book_old_prince = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
			except:
				book_old_prince = "Don't have any old price"
			try:
				book_sale = round(((book_old_prince - book_new_price) / book_old_prince) * 100)
			except:
				book_sale = "Don't have any sale"
			try:
				book_status = book_data[-1].text.strip()
			except:
				book_status = "We don't know a status this book"


			books_data.append(
				{
					"book_title" : book_title,
					"book_author" : book_author,
					"book_publish" : book_publish,
					"book_new_price" : book_new_price,
					"book_old_prince" : book_old_prince,
					"book_sale" : book_sale,
					"book_status" : book_status,
				}
			)
			with open(f"labirint_{cur_date}.csv", "a") as file:
				writer = csv.writer(file)

				writer.writerow(
					(
						book_title,
						book_author,
						book_publish,
						book_new_price,
						book_old_prince,
						book_sale,
						book_status
					)
				)
		print(f"Обработанo {page}/{pages_count}")
		time.sleep(2)
	with open(f"labirint_{cur_date}.json", "w") as file:
		json:dump(books_data, file, indent=4, ensure_ascii=False)

def main():
	get_data()


if __name__ == '__main__':
	main()