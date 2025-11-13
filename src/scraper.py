"""
	Scraper.py

	Scraping script to retrieve job offers from a site

"""


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime


# Job offer specific page
BASE_URL = "https://www.apec.fr/candidat/recherche-emploi.html/emploi?typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687&page=0&motsCles=data%20science"
ROOT = "https://www.apec.fr"

# Departement options for filtering
LOCATIONS = {
	"Paris"		: "75",
	"Belfort"	: "90",
	# Other departments if necessary
}

choice = LOCATIONS.get("Paris", "75")
# URL Tail
tail = lambda dpt: "&lieux=" + choice

opts = Options()

# opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
# appear like a regular browser
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")


# Scraping function
def scrape_jobs() -> list:
	'''
		Returns a list of scraped job offers dictionnaries
	'''


	service = Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=service, options=opts)

	driver.get(BASE_URL + tail(choice))

	wait = WebDriverWait(driver, 20)

	# 1) Accept cookie banner / OneTrust if present (example tries common selectors)
	try:
		# Example: OneTrust accept button is often [id="onetrust-accept-btn-handler"] or similar
		accept_btn = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
		accept_btn.click()
	except Exception:
		# fallback: try to remove the cookie popup by setting the cookie (if needed)
		pass

	# 2) If the site shows the CGU modal in your uploaded HTML, try to click its 'ACCEPTER' button
	try:
		# Wait for modal button and click
		# The HTML you uploaded has a modal with a button that calls apecCguPopin.doAccepted()
		accepter = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'ACCEPTER')]")))
		# ensure the checkbox is checked first (if required)
		try:
			chk = driver.find_element(By.ID, "cguAcceptees")
			if not chk.is_selected():
				driver.execute_script("document.getElementById('cguAcceptees').click();")
		except Exception:
			pass
		accepter.click()
	except Exception:
		# modal not present or already accepted
		pass
	'''
	# 3) Wait for the Angular component to render. Inspect the DOM element that contains offers:
	try:
		# adjust selector to the actual list container the Angular app uses
		offers_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "container-result")) )
		# give Angular a moment to finish rendering
		time.sleep(5)
	except Exception:
		# fallback wait
		time.sleep(5)
	'''


	html = driver.page_source
	soup = BeautifulSoup(html, "html.parser")


	def text_for(ul, alt_value):
		"""Finds the <li> text corresponding to a given <img alt="...">"""
		if not ul:
			return None
		img = ul.select_one(f'li img[alt="{alt_value}"]')
		return img.find_parent("li").get_text(strip=True) if img else None


	def already_in(job, jobs) -> bool:
		'''
			Returns whether a job is already inside a list of job offers or not.

			Inputs:
				job: dict
					The job to check.
				jobs: list
					The list of jobs into which to check.

		'''
		for j in jobs:
			if j["Title"] == job["Title"] and j["Description"] == job["Description"]:
				return True
		
		return False


	# Now parse job cards depending on site DOM; example generic:
	jobs = []
	for card in soup.select(".card, .card-offer, .mb-20, .card--clickable, .card-offer--qualified"):
		
		tmp = card.find_parent("a")
		
		# Main informations
		link = tmp.get("href") if tmp else None
		title = card.select_one(".card-title")
		company = card.select_one(".card-offer__company")
		
		# Skip if this is clearly not a job (issue with 'Les informations légales...' message and other empty div tags)
		if not (company and title):
			continue

		description = card.select_one(".card-offer__description")
		
		# --- Details lists ---
		details_salary = card.select_one("ul.details-offer")
		details_main = card.select_one("ul.details-offer.important-list")
		
		salary = text_for(details_salary, "Salaire texte")
		contract = text_for(details_main, "type de contrat")
		pub_date = text_for(details_main, "date de publication")

		new_job = {
			"Title": title.get_text(strip=True) if title else None,
			"Company": company.get_text(strip=True) if company else None,
			"Description": description.get_text(strip=True) if description else None,
			"Salary": salary if salary else None,
			"Contract": contract if contract else None,
			"Publication date": datetime.strptime(pub_date, "%d/%m/%Y").date() if pub_date else None,
			"pub_date": datetime.strptime(pub_date, "%d/%m/%Y") if pub_date else None,
			"Link": ROOT + str(link) if link else ROOT
		}
		if not already_in(new_job, jobs):
			jobs.append(new_job)

	# Sorting the job offers in descending time order
	get_pub_date = lambda x: x["pub_date"]
	jobs.sort(key=get_pub_date, reverse=True)


	# print(f"Found {len(jobs)} jobs")
	# for j in jobs[:]:
	# 	print(j["Title"], "|", j["Company"], "|", j["Description"], "|", j["Salary"], "|", j["Contract"], "|", j["Publication date"])

	driver.quit()

	return jobs

