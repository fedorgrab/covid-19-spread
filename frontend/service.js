const HOST_URL = "";

const http = axios.create({
  baseURL: `${HOST_URL}`,
});

async function graphqlRequest(query) {
  const requestBody = {"query": query};
  return await http.post("/graphql-api", requestBody);
}

async function getDetailedCountries() {
  let response = await http.get("/detailed-countries");
  return response.data;
}

async function getGeoSpread(country) {
  let response = await http.get(`/static/corona_${country}_spread.geojson`);
  return response.data;
}

async function getDailyUpdate() {
  let response = await graphqlRequest(dailyUpdateRecordQuery);
  return response.data.data.dailyUpdateRecords.edges[0].node;
}

async function getDayOneForCountry(country) {
  let response = await graphqlRequest(dayOneCountryQuery(country));
  return response.data.data.dayOneRecords.edges;
}

const backend = {
  getDetailedCountriesRequest: getDetailedCountries,
  getGeoSpreadRequest: getGeoSpread,
  getDailyUpdateRequest: getDailyUpdate,
  getDayOneForCountryRequest: getDayOneForCountry,
};
