endpoint = 'https://portal.gdc.cancer.gov/auth/api/cases'
verb = 'POST'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded'
}

formData = {
    'size': 3,
    'attachment': 'true',
    'format': 'JSON',
    'fields': 'case_id',
    'filters': {
        "op": "and",
        "content": [{
            "op": "in",
            "content": {
                "field": "cases.case_id",
                "value": ["4abbd258-0f0c-4428-901d-625d47ad363a","a8def1a0-a136-47f4-9ad9-60ebcf9b726b","53245616-e095-4616-89bb-6062669122da"]
            }
        }]
    },
    'pretty': 'true',
    'expand': 'demographic,diagnoses, diagnoses.treatments,exposures,family_histories,follow_ups,follow_ups.molecular_tests',
    'filename': 'clinical.cases_selection.json'
    'downloadCookieKey': '44a06c7ee',
    'downloadCookiePath': '/'
}
formString = 'size=3&attachment=true&format=JSON&fields=case_id&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.case_id%22%2C%22value%22%3A%5B%224abbd258-0f0c-4428-901d-625d47ad363a%22%2C%22a8def1a0-a136-47f4-9ad9-60ebcf9b726b%22%2C%2253245616-e095-4616-89bb-6062669122da%22%5D%7D%7D%5D%7D&pretty=true&expand=demographic%2Cdiagnoses%2Cdiagnoses.treatments%2Cexposures%2Cfamily_histories%2Cfollow_ups%2Cfollow_ups.molecular_tests&filename=clinical.cases_selection.2019-12-27.json&downloadCookieKey=44a06c7ee&downloadCookiePath=%2F'

# Next steps: 1) get Url calls to query all available case ids. 2) write call to see how many cases you can get data for at once 3) download!!