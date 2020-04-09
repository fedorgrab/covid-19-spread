let map;
let isMobile = $(window).width() < 576;

function getMapProperties() {
  return {
    center: new google.maps.LatLng(MAP_CENTER.LAT, MAP_CENTER.LONG),
    zoom: 1.5,
    mapTypeControlOptions: {mapTypeIds: MAP_TYPE_IDS},
    disableDefaultUI: true,
    restriction: {latLngBounds: MAP_RESTRICTION_BOUNDS, strictBounds: false}
  }
}

function setMapStyle(mapStyle) {
  let name = "Coronavirus Spread Heat Map";
  const styledMapType = new google.maps.StyledMapType(
    mapStyle, {name: name}
  );
  map.mapTypes.set("styled_map", styledMapType);
  map.setMapTypeId("styled_map");
}


async function setWorldStats() {
  let worldStats = await backend.getDailyUpdateRequest();
  document.getElementById("world-total-confirmed").innerHTML = worldStats["casesConfirmed"];
  document.getElementById("world-total-deaths").innerHTML = worldStats["casesDeaths"];
  document.getElementById("world-total-recovered").innerHTML = worldStats["casesRecovered"];
  
  document.getElementById("world-today-confirmed").innerHTML = worldStats["casesConfirmedNew"];
  document.getElementById("world-today-deaths").innerHTML = worldStats["casesDeathsNew"];
  document.getElementById("world-today-recovered").innerHTML = worldStats["casesRecoveredNew"];
}

function mouseoverListener(event) {
  map.data.revertStyle();
  map.data.overrideStyle(event.feature, {strokeWeight: 2});
}

function mouseoutListener(event) {
  map.data.revertStyle();
}


async function clickListener(event) {
  textContent = includeTextContent(event.feature);
  let country = event.feature.getProperty("country");
  // if (!isMobile) {
  currentDayOne = await backend.getDayOneForCountryRequest(country);
  console.log("I AM BEFORE PLOT FUNC");
  plot(currentDayOne, siteColorTheme);
  // }
  document.getElementById("info-box").innerHTML = textContent;
}

async function setMapGeoData() {
  let worldGeoJson = await backend.getGeoSpreadRequest("world");
  map.data.addGeoJson(worldGeoJson);
  let detailedCountriesNames = await backend.getDetailedCountriesRequest();
  for (let i = 0; i < detailedCountriesNames.length; i++) {
    let geoJson = await backend.getGeoSpreadRequest(detailedCountriesNames[i]);
    map.data.addGeoJson(geoJson);
  }
}

async function initMap() {
  map = new google.maps.Map(
    document.getElementById("googleMap"), getMapProperties()
  );
  setMapStyle(MAP_STYLE_BLACK); // default site theme is black
  await setWorldStats();
  map.data.setStyle(getStyleProvincePolygon);
  await setMapGeoData();
  
  map.data.addListener('click', clickListener);
  map.data.addListener('mouseover', mouseoverListener);
  map.data.addListener('mouseout', mouseoutListener);
}
