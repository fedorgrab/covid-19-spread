const HOST_URL = "";

const http = axios.create({
  baseURL: `${HOST_URL}`,
});

async function graphqlRequest(query) {
  const requestBody = {"query": query};
  return await http.post("/graphql-api", requestBody);
}

async function getGeoSpread() {
  let response = await http.get("/static/corona_spread.geojson");
  return response.data;
}


async function getDailyUpdate() {
  let resp = await graphqlRequest(dailyUpdateRecordQuery);
  return resp.data.data.dailyUpdateRecords.edges[0].node;
}

const backend = {
  getGeoSpreadRequest: getGeoSpread,
  getDailyUpdateRequest: getDailyUpdate,
};
